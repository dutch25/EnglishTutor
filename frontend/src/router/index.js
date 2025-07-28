import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import IPA from '../views/IPA.vue';
import Verb from '../views/Verb.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/ipa', name: 'IPA', component: IPA },
  { path: '/verb', name: 'Verb', component: Verb },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
