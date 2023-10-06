<template>
  <div class="homepage">
    <router-link to="/register">
      <button>Register</button>
    </router-link>
    <router-link to="/login/user">
      <button>Login User</button>
    </router-link>
    <router-link to="/login/manager">
      <button>Login Manager</button>
    </router-link>
    <router-link to="/login/admin">
      <button>Login Admin</button>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'HomePageComponent',
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
