import { createApp, reactive } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';


const app = createApp(App)
  .use(router)
  .mount('#app');

app.user = reactive({ loggedIn: false, userType: null });