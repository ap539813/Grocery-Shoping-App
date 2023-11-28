<template>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="navbar-brand">
        <span>Register User</span>
      </div>
      <div class="ml-auto">
        <button class="btn btn-outline-primary" @click="goToHome">Home</button>
      </div>
    </nav>
  
    <div class="container mt-5">
      <div class="form-group">
        <input type="text" class="form-control" v-model="username" placeholder="Username" />
      </div>
      <div class="form-group">
        <input type="email" class="form-control" v-model="email" placeholder="Email" />
      </div>
      <div class="form-group">
        <input type="password" class="form-control" v-model="password" placeholder="Password" />
      </div>
      <div class="form-check">
        <input type="checkbox" class="form-check-input" v-model="isManager" id="managerCheckbox" />
        <label class="form-check-label" for="managerCheckbox">Register as manager</label>
      </div>
      <button class="btn btn-primary" @click="register">Register User</button>
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
body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            text-align: center;
            margin-top: 50px;
        }

        .container {
            background-color: white;
            padding: 20px 30px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 400px;
            margin: 0 auto;
            border-radius: 8px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
        }

        .form-group input {
            width: 100%;
            padding: 10px 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 16px;
            box-sizing: border-box;
        }

        button {
            background-color: #008CBA;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            margin: 4px 2px;
            cursor: pointer;
            font-size: 16px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }

        button:hover {
            background-color: #006c99;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: #333;
            color: white;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
            position: fixed; 
            top: 0; 
            left: 0;  
            width: 100%; 
            z-index: 1000;
            box-sizing: border-box; 
            padding-right: 15px;
        }

        .navbar-left, .navbar-right {
            display: flex;
            align-items: center;
        }

</style>
