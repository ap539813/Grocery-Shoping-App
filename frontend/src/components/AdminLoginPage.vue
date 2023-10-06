<template>
    <div class="user-login-page">
      <input type="text" v-model="username" placeholder="Username" />
      <input type="password" v-model="password" placeholder="Password" />
      <button @click="login">Login User</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      login() {
        // Handle the registration logic here
        console.log('User registered:', this.username);
      }
    }
  }
  </script>
  
  <style scoped>
  /* Add styling for the login page here */
  .user-login-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
  </style>
  