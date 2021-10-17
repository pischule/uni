<template>
  <textarea v-model="text" id="note-text-textarea" class="materialize-textarea"></textarea>
  <button @click="$emit('saveNote', text)" class="btn">Save</button>
</template>
<style>
textarea.materialize-textarea {
  height: 10rem;
}
</style>
<script>
export default {
  name: 'CreateNoteForm',
  date() {
    return {
      text: ''
    }
  },
  emits: ['saveNote']
}
</script>