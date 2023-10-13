<template>
  <h1>Manager Login</h1>
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
      async login() {
        try {
          const response = await fetch('http://127.0.0.1:5000/login-manager', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password
            })
          });
          
          const data = await response.json();
          
          if (data.status === 'success') {
            alert('Manager login successful!');
            this.$router.push({ name: 'ManagerDashboard' });
          } else {
            alert('Login failed!');
          }
        } catch (error) {
          console.error("There was an error logging in:", error);
        }
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
  