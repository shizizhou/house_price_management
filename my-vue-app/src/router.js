import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/home.vue';
import Login from './views/login.vue';
import Register from './views/register.vue';
import CreateProperty from './views/createProperty.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/create', component: CreateProperty }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;