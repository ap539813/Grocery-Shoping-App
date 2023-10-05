<template>
    <div class="homepage">
      <button @click="register">Register</button>
      <button @click="loginUser">Login User</button>
      <button @click="loginManager">Login Manager</button>
      <button @click="loginAdmin">Login Manager</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePageComponent',
    methods: {
      register() {
        // Handle registration logic here
        console.log('Register button clicked');
      },
      loginUser() {
        // Handle user login logic here
        console.log('Login User button clicked');
      },
      loginManager() {
        // Handle manager login logic here
        console.log('Login Manager button clicked');
      },
      loginAdmin() {
        // Handle manager login logic here
        console.log('Login Admin button clicked');
      }
    }
  }
  </script>
  
  <style scoped>
  /* Style your buttons and homepage here */
  .homepage {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
  </style>
  