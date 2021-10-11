'use strict';

import axios from 'axios';
import forge from 'node-forge';

async function getSessionKeyEncrypted(userId, keyPair) {
    const response = await axios.post('/api/login', {
        userId: 1,
        publicKeyPem: publicKeyPem(keyPair)
    });
    return response.data.encryptedSessionKey;
}

function generateKeyPair() {
    return Promise.resolve().then(() => {
        return forge.pki.rsa.generateKeyPair({bits: 2048});
    })
}

function decryptSessionKey(encryptedSessionKey, keypair) {
    const encryptedBytes = forge.util.decode64(encryptedSessionKey);
    const sessionKeyBytes = keypair.privateKey.decrypt(encryptedBytes);
    return forge.util.encode64(sessionKeyBytes);
}

function privateKeyPem(keyPair) {
    if (keyPair === null) return null;
    return forge.pki.privateKeyToPem(keyPair.privateKey);
}

function publicKeyPem(keyPair) {
    if (keyPair === null) return null;
    return forge.pki.publicKeyToPem(keyPair.publicKey);
}

async function getEncryptedNoteAndIv(noteId, userId) {
    const response = await axios.get('/api/note', {
        params: {
            noteId: noteId,
            userId: userId
        }
    });

    return response.data;
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

function encryptNote(note, iv, sessionKey) {
    const keyBytes = forge.util.decode64(sessionKey);
    const cipher = forge.cipher.createDecipher('AES-CFB', keyBytes);
    cipher.start({iv: forge.util.decode64(iv)});
    cipher.update(forge.util.createBuffer(note, 'utf8'));
    cipher.finish();
    return forge.util.encode64(cipher.output.data);
}

// const kp = await generateKeyPair();
// const sessionKeyEncrypted = await getSessionKeyEncrypted(1, kp);
// console.log(sessionKeyEncrypted)
// const decryptedSessionKey = await decryptSessionKey(sessionKeyEncrypted, kp);
// console.log(decryptedSessionKey);
// let {encryptedNote, iv} = await getEncryptedNoteAndIv(2, 1);
// console.log(encryptedNote, iv);
// const decryptedNote = decryptNote(encryptedNote, iv, decryptedSessionKey)
// console.log(decryptedNote);
// const onceAgainEncryptedNotes = encryptNote(decryptedNote, iv, decryptedSessionKey);
// console.log(onceAgainEncryptedNotes);
// const newIv = generateIv();
// console.log(newIv);
// const encryptedWithAnotherIv = encryptNote(decryptedNote, newIv, decryptedSessionKey);
// console.log(encryptedWithAnotherIv);

export {
    getSessionKeyEncrypted, generateKeyPair, decryptSessionKey,
    privateKeyPem, publicKeyPem, getEncryptedNoteAndIv, decryptNote, generateIv, encryptNote
};