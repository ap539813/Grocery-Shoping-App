<template>
  <div class="homepage container">
    <!-- Use a single column for all buttons -->
    <div class="row justify-content-center">
      <div class="col-md-6"> <!-- Adjust the column size as needed -->
        <router-link to="/register" class="d-block mb-2">
          <button class="btn custom-register w-100">Register</button>
        </router-link>
        <router-link to="/login/user" class="d-block mb-2">
          <button class="btn btn-primary w-100">Login User</button>
        </router-link>
        <router-link to="/login/manager" class="d-block mb-2">
          <button class="btn btn-primary w-100">Login Manager</button>
        </router-link>
        <router-link to="/login/admin" class="d-block mb-2">
          <button class="btn btn-primary w-100">Login Admin</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePageComponent',
}
</script>

<style scoped>
.custom-register {
  background-color: #32a852; 
  border-color: #32a852;
  color: #ffffff;
}

.custom-register:hover {
  background-color: #2b8e47;
  border-color: #2b8e47;
  color: #ffffff; 
}

.router-link {
  display: block;
  margin-bottom: 20px
}
</style>
