'use strict';

import axios from 'axios';
import forge from 'node-forge';

// const prefix = 'http://localhost:8080';
const prefix = '';

async function getSessionKeyResponse(username, password, keyPair) {
    const response = await axios.post(`${prefix}/api/session-key/`, {
        username: username,
        password: password,
        publicKeyPem: publicKeyPem(keyPair.publicKey)
    });
    console.log('response: ');
    console.log(response.data);
    const encryptedSessionKey = response.data.encryptedSessionKey;
    const sessionToken = response.data.sessionToken;
    const sessionKey = decryptSessionKey(encryptedSessionKey, keyPair);
    console.log(`encrypted session key: ${encryptedSessionKey}`);
    console.log(`decrypted session key: ${sessionKey}`);
    return {
        sessionKey: sessionKey,
        sessionToken: sessionToken,
    };
}

function generateKeyPair() {
    return Promise.resolve().then(() => {
        const keyPair = forge.pki.rsa.generateKeyPair({bits: 2048});
        console.log('keypair generated')
        console.log(`public key: \n${publicKeyPem(keyPair.publicKey)}`);
        console.log(`private key: \n${privateKeyPem(keyPair.privateKey)}`);
        return keyPair;
    })
}

function decryptSessionKey(encryptedSessionKey, keypair) {
    if (encryptedSessionKey === null || keypair === null) return null;
    const encryptedBytes = forge.util.decode64(encryptedSessionKey);
    const sessionKeyBytes = keypair.privateKey.decrypt(encryptedBytes);
    return forge.util.encode64(sessionKeyBytes);
}

function privateKeyPem(privateKey) {
    if (privateKey === null) return null;
    return forge.pki.privateKeyToPem(privateKey);
}

function publicKeyPem(publicKey) {
    if (publicKey === null) return null;
    return forge.pki.publicKeyToPem(publicKey);
}

function generateIv() {
    return forge.util.encode64(forge.random.getBytesSync(16));
}

function decryptNote(encryptedNote, iv, sessionKey) {
    const encryptedBytes = forge.util.decode64(encryptedNote);
    const keyBytes = forge.util.decode64(sessionKey);
    const cipher = forge.cipher.createDecipher('AES-CFB', keyBytes);
    cipher.start({iv: forge.util.decode64(iv)});
    cipher.update(forge.util.createBuffer(encryptedBytes));
    cipher.finish();
    return cipher.output.toString();
}

function encryptNote(text, iv, sessionKey) {
    const keyBytes = forge.util.decode64(sessionKey);
    const cipher = forge.cipher.createCipher('AES-CFB', keyBytes);
    cipher.start({iv: forge.util.decode64(iv)});
    cipher.update(forge.util.createBuffer(text, 'utf8'));
    cipher.finish();
    return forge.util.encode64(cipher.output.data);
}

async function saveNote(text, sessionKey, sessionToken) {
    console.log('save note');
    const iv = generateIv();
    const encryptedNote = encryptNote(text, iv, sessionKey);
    console.log("sending:");
    console.log({
        encryptedNote: encryptedNote,
        iv: iv
    });
    const response = await axios.post(`${prefix}/api/note/`, {
            encryptedNote: encryptedNote,
            iv: iv
        },
        {headers: {'Authorization': sessionToken}})
    console.log('receiving:');
    console.log(response.data);
    return response.data;
}

async function updateNote(noteId, text, sessionKey, sessionToken) {
    const iv = generateIv();
    const encryptedNote = encryptNote(text, iv, sessionKey);
    const response = await axios.put(`${prefix}/api/note/${noteId}`, {
            encryptedNote: encryptedNote,
            iv: iv
        },
        {headers: {'Authorization': sessionToken}});
    console.log('updateNote')
    console.log(response.data);
    return response.data;
}

async function deleteNote(noteId, sessionToken) {
    return await axios.delete(`${prefix}/api/note/${noteId}`, {
        headers: {
            'Authorization': sessionToken
        }
    });
}

async function getNotes(sessionKey, sessionToken) {
    const response = await axios.get(`${prefix}/api/note/`,
        {headers: {'Authorization': sessionToken}});
    const encryptedNotes = response.data;
    console.log('encrypted notes:');
    console.log(encryptedNotes);
    return encryptedNotes.map(note => {
        return {
            'noteId': note.noteId,
            'text': decryptNote(note.encryptedNote, note.iv, sessionKey)
        }
    });
}

// if (prefix !== '') {
//     // const kp = await generateKeyPair();
//     // const sessionKeyResponse = await getSessionKeyResponse('admin', 'admin', kp);
//     // const text = '123';
//     // console.log(sessionKeyResponse);
//     // const saved = await saveNote(text, sessionKeyResponse.sessionKey, sessionKeyResponse.sessionToken);
//     const result = encryptNote('123', 'TzCPfbR9peAO0wMdMTtXkQ==', 'MP1WdsrMxpV1hNVLWZ2RgA==');
//     const decr = decryptNote(result, 'TzCPfbR9peAO0wMdMTtXkQ==', 'MP1WdsrMxpV1hNVLWZ2RgA==');
//     console.log(result);
//     console.log(decr);
// }

export {
    getNotes, getSessionKeyResponse, generateKeyPair, decryptSessionKey, saveNote, updateNote, deleteNote,
    decryptNote, generateIv, encryptNote
};