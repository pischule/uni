<template>
  <div id="app" class="container">
    <h2>Защищенный блокнот</h2>

    <p>Публичный ключ</p>
    <pre>{{ publicKey }}</pre>
    <p>Приватный ключ</p>
    <pre>{{ privateKey }}</pre>
    <button class="btn" @click="getSessionKey">Получить сеансовый ключ</button>

    <div v-if="encryptedSessionKey">
      <p>Зашифрованный сеансовый ключ:</p>
      <code style="overflow-wrap: break-word"> {{ encryptedSessionKey }} </code>
      <p>Расшифрованный сеансовый ключ:</p>
      <code style="overflow-wrap: break-word"> {{ decryptedSessionKey }} </code>
      <p></p>

      <label for="fileId">ID файла</label>
      <input id="fileId" v-model="fileId" type="number" placeholder="1">
      <button class="btn" @click="getFile">Получить файл</button>

      <div v-if="encryptedFile">
        <p>Зашифрованный файл:</p>
        <code style="overflow-wrap: break-word"> {{ encryptedFile }}</code>
        <p>IV:</p>
        <code style="overflow-wrap: break-word"> {{ iv }}</code>
        <p>Содержимое файла:</p>
        <p>{{ decryptedFile }}</p>
      </div>
    </div>
  </div>
</template>

<script>

import * as M from 'materialize-css';
import * as forge from 'node-forge';

export default {
  name: 'App',
  components: {},
  data() {
    return {
      keypair: null,
      encryptedSessionKey: null,
      userId: 1,
      fileId: 1,
      encryptedFile: null,
      iv: null
    }
  },
  computed: {
    publicKey() {
      return forge.pki.publicKeyToPem(this.keypair.publicKey);
    },
    privateKey() {
      return forge.pki.privateKeyToPem(this.keypair.privateKey);
    },
    sessionKey() {
      return this.keypair.privateKey.decrypt(forge.util.decode64(this.encryptedSessionKey));
    },
    decryptedSessionKey() {
      return forge.util.encode64(this.sessionKey);
    },
    decryptedFile() {
      let encryptedBytes = forge.util.decode64(this.encryptedFile);
      let cipher = forge.cipher.createDecipher('AES-CFB', this.sessionKey);
      cipher.start({iv: forge.util.decode64(this.iv)});
      cipher.update(forge.util.createBuffer(encryptedBytes));
      cipher.finish();
      return cipher.output.toString();
    }
  },
  methods: {
    getSessionKey() {
      fetch("/api/login", {
        method: 'POST',
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          userId: this.userId,
          publicKeyPem: this.publicKey
        })
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('Какие-то проблемы с сетью');
            }
            return response.json();
          })
          .then(json => {
            this.encryptedSessionKey = json.encryptedSessionKey;
          })
          .catch(err => {
            M.toast({html: err});
          });
    },
    getFile() {
      fetch(`/api/note?noteId=${this.fileId}&userId=${this.userId}`, {
        method: 'GET',
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        }
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('Файл не найден');
            }
            return response.json();
          })
          .then(json => {
            this.encryptedFile = json.encryptedText;
            this.iv = json.iv;
          })
          .catch(err => {
            this.fileContents = null;
            M.toast({html: err});
          });
    }
  },
  created() {
    this.keypair = forge.pki.rsa.generateKeyPair({bits: 2048});
  }
}
</script>

<style>
</style>
