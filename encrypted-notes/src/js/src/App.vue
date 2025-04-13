<template>

  <nav>
    <div class="nav-wrapper teal">
      <a href="#" class="brand-logo center">Encrypted notes</a>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <li><a @click="logOut">Log out</a></li>
      </ul>
    </div>
  </nav>

  <main id="app" class="container">

    <login-form v-if="loggedOut" @logged-in="loggedInHandler($event)"/>

    <template v-else>
      <create-note-form @save-note="saveNote($event)"/>
      <note-component
          v-for="note in notes"
          :key="note.noteId"
          :text="note.text"
          :noteId="note.noteId"
          @delete-note="deleteNote($event)"
          @update-note="updateNote($event.noteId, $event.text)"/>
    </template>
  </main>
</template>

<script>

import * as l from "./logic";
import M from 'materialize-css';
import LoginForm from './components/LoginForm.vue';
import CreateNoteForm from './components/CreateNoteForm';
import NoteComponent from "@/components/NoteComponent";

export default {
  name: 'App',
  components: {
    NoteComponent,
    LoginForm, CreateNoteForm
  },
  data() {
    return {
      sessionKey: null,
      sessionToken: null,
      notes: []
    }
  },
  computed: {
    loggedOut() {
      return !(this.sessionKey && this.sessionToken);
    }
  },
  created() {
    M.AutoInit();
  },
  methods: {
    loggedInHandler(sessionData) {
      this.sessionToken = sessionData.sessionToken;
      this.sessionKey = sessionData.sessionKey;
      this.refreshNoteList();
    },
    saveNote(text) {
      console.log('saving note: ');
      console.log(text);
      l.saveNote(text, this.sessionKey, this.sessionToken)
          .then(this.refreshNoteList)
          .catch(this.handleStatusCode);
    },
    deleteNote(noteId) {
      console.log(`delete ${noteId}`);
      l.deleteNote(noteId, this.sessionToken)
          .then(() => {
            this.notes = this.notes
                .filter(value => value.noteId !== noteId);
          })
          .catch(this.handleStatusCode);
    },
    refreshNoteList() {
      l.getNotes(this.sessionKey, this.sessionToken)
          .then(value => this.notes = value)
          .catch(this.handleStatusCode);
    },
    updateNote(noteId, text) {
      l.updateNote(noteId, text, this.sessionKey, this.sessionToken)
          .then(this.refreshNoteList)
          .catch(this.handleStatusCode);
    },
    logOut() {
      this.sessionToken = null;
      this.sessionKey = null;
      this.notes = [];
      M.toast({html: 'You\'ve been logged out'});
    },
    handleStatusCode(code) {
      if (code === 403) {
        this.logOut();
      } else {
        M.toast({html: `Server returned ${code}`});
      }
    }
  }
}
</script>

<style>
</style>
