import { createRouter, createWebHistory } from 'vue-router';
import HomePageComponent from './components/HomePageComponent.vue';
import RegisterPage from './components/RegisterPage.vue';
import UserLoginPage from './components/UserLoginPage.vue';
// import ManagerLoginPage from './components/ManagerLoginPage.vue';
// import AdminLoginPage from './components/AdminLoginPage.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePageComponent },
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/login/user', name: 'LoginUser', component: UserLoginPage },
  // { path: '/login/manager', name: 'LoginManager', component: ManagerLoginPage },
  // { path: '/login/admin', name: 'LoginAdmin', component: AdminLoginPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
