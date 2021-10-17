<template>
  <div v-if="readMode" class="card blue-grey darken-1">
    <div class="card-content white-text">
      <p>{{ text }}</p>
    </div>
    <div class="card-action">
      <a @click="readMode=!readMode">Edit</a>
      <a @click="$emit('deleteNote', noteId)">Delete</a>
    </div>
  </div>
  <div v-else class="card blue-grey darken-1">
    <div class="card-content white-text">
      <textarea class="materialize-textarea white-text" v-model="updatedText"/>
    </div>
    <div class="card-action">
      <a @click="updateNote">Save</a>
      <a @click="readMode=!readMode">Cancel</a>
    </div>
  </div>
</template>
<script>
import M from 'materialize-css';

export default {
  props: ['text', 'noteId'],
  emits: ['deleteNote', 'updateNote'],
  data() {
    return {
      readMode: true,
      updatedText: this.text
    }
  },
  methods: {
    updateNote() {
      this.$emit('updateNote', {noteId: this.noteId, text: this.updatedText});
      this.readMode = !this.readMode;
    },
  },
  triggerInput() {
    this.$nextTick(() => {
      this.$refs.resize.$el.dispatchEvent(new Event("input"));
    });
  },
  watch: {
    readMode() {
      // Wait until the template has updated
      this.$nextTick(() => {
        [...document.querySelectorAll('textarea')].forEach(textarea => {
          M.textareaAutoResize(textarea)
        });
      });
    }
  }
}
</script>