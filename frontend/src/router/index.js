import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import IPA from '../views/IPA.vue';
import Verb from '../views/Verb.vue';
import Listening from '../views/ListeningTest.vue';
import Sentence from '../views/SentenceTest.vue';
import Conversation from '../views/ConversationPractice.vue';
import Whisper from '../views/Whisper.vue';



const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/ipa', name: 'IPA', component: IPA },
  { path: '/verb', name: 'Verb', component: Verb },
  { path: '/listening', name: 'Listening', component: Listening },
  { path: '/sentence', name: 'Sentence', component: Sentence },
  { path: '/conversation', name: 'Conversation', component: Conversation },
  { path: '/Whisper', name: 'Whisper', component: Whisper }

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
