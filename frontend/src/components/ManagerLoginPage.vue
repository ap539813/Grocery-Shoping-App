<template>
  <!-- Navigation Bar -->
  <nav class="navbar">
      <div class="navbar-left">
        <span id="manager-username">Login Manager</span>
      </div>
      <div class="navbar-right">
        <button @click="goToHome">Home</button>
      </div>
    </nav>
  <!-- <h1>Manager Login</h1> -->
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
      goToHome() {
        this.$router.push({ name: 'Home'});
        },
      async login() {
        try {
          const response = await fetch('http://127.0.0.1:5000/login-manager', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
              username: this.username,
              password: this.password
            })
          });
          
          const data = await response.json();
          
          if (data.status === 'success') {
            alert('Manager login successful!');
            // this.$router.push({ name: 'ManagerDashboard' });
            this.$router.push({ name: 'ManagerDashboard', query: { username: this.username } });
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
  