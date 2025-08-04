import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import IPA from "../views/IPA.vue";
import Verb from "../views/Verb.vue";
import Register from "@/Auths/Register.vue";
import Login from "@/Auths/Login.vue";
import Listening from "../views/ListeningTest.vue";
import Sentence from "../views/SentenceTest.vue";
import Whisper from "../views/Whisper.vue";
import Dictionary from '../views/Dictionary.vue';
import Profile from '../views/Profile.vue';
import EditProfile from "../views/EditProfile.vue";
import ForgotPassword from "../views/ForgotPassword.vue";
import Saved from '../views/Saved.vue';
import Feedback from '../views/Feedback.vue';

const routes = [
  { path: "/", name: "Login", component: Login },
  { path: "/register", name: "Register", component: Register },

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
    path: "/profile",
    name: "Profile",
    component: Profile,
    meta: { requiresAuth: true },
  },
  {
    path: "/edit-profile",
    name: "EditProfile",
    component: EditProfile,
    meta: { requiresAuth: true },
  },
  {
    path: "/forgot-password",
    name: "ForgotPassword",
    component: ForgotPassword,
    meta: { requiresAuth: false },
  },
  {
    path: "/saved",
    name: "Saved",
    component: Saved,
    meta: { requiresAuth: true },
  },
  {
    path: "/feedback",
    name: "Feedback",
    component: Feedback,
    meta: { requiresAuth: true },
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem("token"); 

  if (to.meta.requiresAuth && !isLoggedIn) {
    next("/"); 
  } else if (to.path === "/" && isLoggedIn) {
    next("/home");
  } else {
    next();
  }
});

export default router;
