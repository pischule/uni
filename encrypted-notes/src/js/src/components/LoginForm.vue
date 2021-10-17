<template>

  <label>Username</label>
  <input id="username" type="text" v-model="username"/>
  <label>Password</label>
  <input id="password" type="password" v-model="password"/>
  <button @click="logIn" class="btn">Log in</button>
</template>
<script>
import * as l from "@/logic";

export default {
  data() {
    return {
      username: 'admin',
      password: 'admin',
      keyPair: null,
    }
  },
  created() {
    l.generateKeyPair()
        .then((keyPair) => {
          this.keyPair = keyPair;
        })
  },
  methods: {
    logIn() {
      l.getSessionKeyResponse(this.username, this.password, this.keyPair)
          .then(response => {
            console.log('logged in');
            console.log(response);
            this.$emit('loggedIn', response)
          })
          .catch(console.log);
    },
  },
  emits: ['loggedIn']
}
</script>