<template>
  <div class="user-login-page">
    <input type="text" v-model="username" placeholder="Username" />
    <input type="password" v-model="password" placeholder="Password" />
    <button @click="login">Login Admin</button>
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
              let response = await fetch("http://127.0.0.1:5000/login_admin", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                      username: this.username,
                      password: this.password
                  })
              });

              let data = await response.json();

              if (response.status === 200) {
                  console.log('Login successful:', data.message);
                  this.$router.push({ name: 'AdminDashboard' });
              } else {
                  console.log('Login failed:', data.message);
                  alert(data.message);
              }
              
          } catch (error) {
              console.error("There was an error during login:", error);
              alert("There was an error during login.");
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
