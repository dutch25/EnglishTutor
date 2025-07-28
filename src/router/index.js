import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import IPA from '../views/IPA.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/ipa', name: 'IPA', component: IPA },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
