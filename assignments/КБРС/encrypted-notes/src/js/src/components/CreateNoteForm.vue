<template>
  <textarea
      v-model="text"
      id="note-text-textarea"
      placeholder="Blah blah blah"
      class="materialize-textarea"/>
  <button @click="$emit('saveNote', text)" class="btn">Save</button>
</template>
<script>
export default {
  name: 'CreateNoteForm',
  data() {
    return {
      text: ''
    }
  },
  emits: ['saveNote']
}
</script>