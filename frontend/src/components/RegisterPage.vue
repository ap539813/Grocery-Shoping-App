<template>
    <div class="register-page">
      <input type="text" v-model="username" placeholder="Username" />
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
        password: '',
        isManager: false  // To track the checkbox state
      };
    },
    methods: {
      async register() {
        if(this.isManager) {
          console.log('Manager registered:', this.username, 'Manager password', this.password);
        } else {
          console.log('User registered:', this.username, 'User password', this.password);
        }
        try {
            let response = await fetch("http://localhost:5000/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                    isManager: this.isManager
                })
            });

            let data = await response.json();
            console.log(data.message);

        } catch (error) {
            console.error("There was an error during registration:", error);
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
  