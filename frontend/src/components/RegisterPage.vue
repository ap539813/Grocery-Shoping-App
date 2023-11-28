<template>
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-left">
        <span id="manager-username">Register User</span>
      </div>
      <div class="navbar-right">
        <button @click="goToHome">Home</button>
      </div>
    </nav>
  <div class="register-page">
    <input type="text" v-model="username" placeholder="Username" />
    <input type="email" v-model="email" placeholder="Email" />
    <input type="password" v-model="password" placeholder="Password" />
    <input type="checkbox" v-model="isManager" id="managerCheckbox" />
    <label for="managerCheckbox">Register as manager</label>
    <button @click="register">Register User</button>
  </div>
</template>

<script>
export default {
  data() {
      return {
          username: '',
          email: '',
          password: '',
          isManager: false  // To track the checkbox state
      };
  },
  methods: {
    goToHome() {
        this.$router.push({ name: 'Home'});
        },
      async register() {
          try {
              let response = await fetch("http://127.0.0.1:5000/register", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json"
                  },
                  credentials: 'include',
                  body: JSON.stringify({
                      username: this.username,
                      password: this.password,
                      email: this.email,
                      isManager: this.isManager
                  })
              });

              let data = await response.json();
              alert(data.message);

              
              this.username = '';
              this.password = '';
              this.email = '';
              this.isManager = false;

          } catch (error) {
              console.error("There was an error during registration:", error);
              alert("There was an error during registration.");
          }
      }
  }
}
</script>

<style scoped>
/* Add styling for the login page here */
.register-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}
</style>
