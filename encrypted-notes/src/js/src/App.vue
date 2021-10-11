<template>
  <div id="app" class="container">
    <h2>Защищенный блокнот</h2>

    <p>Публичный ключ</p>
    <pre style="overflow-wrap: break-word">{{ publicKey }}</pre>
    <p>Приватный ключ</p>
    <pre style="overflow-wrap: break-word">{{ privateKey }}</pre>
    <button class="btn" @click="getSessionKey">Получить сеансовый ключ</button>

    <div v-if="encryptedSessionKey">
      <p>Зашифрованный сеансовый ключ:</p>
      <code style="overflow-wrap: break-word"> {{ encryptedSessionKey }} </code>
      <p>Расшифрованный сеансовый ключ:</p>
      <code style="overflow-wrap: break-word"> {{ decryptedSessionKey }} </code>
      <p></p>

      <label for="noteId">ID файла</label>
      <input id="noteId" v-model="noteId" type="number" placeholder="1">
      <button class="btn" @click="getNote">Получить файл</button>

      <div v-if="encryptedNote">

        <div class="card blue-grey darken-1">
          <div class="card-content white-text">
            <span class="card-title">Зашифрованный файл</span>
            <code style="overflow-wrap: break-word"> {{ encryptedNote }}</code>
            <span class="card-title">IV</span>
            <code style="overflow-wrap: break-word"> {{ iv }}</code>
          </div>
        </div>

        <div class="card teal darken-1">
          <div class="card-content white-text">
            <span class="card-title">Расшифрованный файл</span>
            <p>{{ decryptedNote }}</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>

import * as l from "./logic";

export default {
  name: 'App',
  components: {},
  data() {
    return {
      userId: 1,
      keyPair: null,
      iv: null,
      noteId: 1,
      encryptedNote: null,
      encryptedSessionKey: null
    }
  },
  computed: {
    publicKey() {
      return l.publicKeyPem(this.keyPair);
    },
    privateKey() {
      return l.privateKeyPem(this.keyPair);
    },
    decryptedSessionKey() {
      return l.decryptSessionKey(this.encryptedSessionKey, this.keyPair);
    },
    decryptedNote() {
      return l.decryptNote(this.encryptedNote, this.iv, this.decryptedSessionKey);
    }
  },
  methods: {
    getSessionKey() {
      l.getSessionKeyEncrypted(1, this.keyPair)
          .then((value) => this.encryptedSessionKey = value);
    },
    getNote() {
      l.getEncryptedNoteAndIv(this.noteId, this.userId)
          .then(value => {
            this.encryptedNote = value.encryptedNote;
            this.iv = value.iv;
          });
    },
    getPrevNote() {
      this.noteId -= 1;
      this.getNote();
    },
    getNextNote() {
      this.noteId += 1;
      this.getNote();
    }
  },
  created() {
    l.generateKeyPair()
        .then((keyPair) => {
          this.keyPair = keyPair;
        });
  }
}
</script>

<style>
</style>
