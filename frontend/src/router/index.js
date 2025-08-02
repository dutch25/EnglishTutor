import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import IPA from "../views/IPA.vue";
import Verb from "../views/Verb.vue";
import Register from "@/Auths/Register.vue";
import Login from "@/Auths/Login.vue";
import Listening from "../views/ListeningTest.vue";
import Sentence from "../views/SentenceTest.vue";
import Conversation from "../views/ConversationPractice.vue";
import Whisper from "../views/Whisper.vue";
import Dictionary from '../views/Dictionary.vue';
import Saved from '../views/Saved.vue';

const routes = [
  { path: "/", name: "Login", component: Login },
  { path: "/register", name: "Register", component: Register },

  // ✅ Các route cần login
  {
    path: "/home",
    name: "Home",
    component: Home,
    meta: { requiresAuth: true },
  },
  { path: "/ipa", name: "IPA", component: IPA, meta: { requiresAuth: true } },
  {
    path: "/verb",
    name: "Verb",
    component: Verb,
    meta: { requiresAuth: true },
  },
  {
    path: "/listening",
    name: "Listening",
    component: Listening,
    meta: { requiresAuth: true },
  },
  {
    path: "/sentence",
    name: "Sentence",
    component: Sentence,
    meta: { requiresAuth: true },
  },
  {
    path: "/conversation",
    name: "Conversation",
    component: Conversation,
    meta: { requiresAuth: true },
  },
  {
    path: "/whisper",
    name: "Whisper",
    component: Whisper,
    meta: { requiresAuth: true },
  },
  {
    path: "/dictionary",
    name: "Dictionary",
    component: Dictionary,
    meta: { requiresAuth: true },
  },
  {
    path: "/saved",
    name: "Saved",
    component: Saved,
    meta: { requiresAuth: true },
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ✅ Navigation Guard
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem("token"); // kiểm tra token

  if (to.meta.requiresAuth && !isLoggedIn) {
    next("/"); // nếu chưa login → quay về Login
  } else if (to.path === "/" && isLoggedIn) {
    next("/home"); // nếu đã login mà vào "/" → redirect sang Home
  } else {
    next();
  }
});

export default router;
