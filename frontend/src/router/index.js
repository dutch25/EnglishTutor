import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import IPA from '../views/IPA.vue';
import Verb from '../views/Verb.vue';
import Register from '@/Auths/Register.vue';
import Login from '@/Auths/Login.vue';

const routes = [
  { path: '/', name: 'Login', component: Login },
  { path: '/ipa', name: 'IPA', component: IPA },
  { path: '/verb', name: 'Verb', component: Verb },
  { path: '/register', name: 'Register', component: Register },
  { path: '/home', name: 'Home', component: Home },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
