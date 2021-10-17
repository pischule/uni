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
    }
  },
  created() {
    M.textareaAutoResize($('#textarea1'));
  }
}
</script>