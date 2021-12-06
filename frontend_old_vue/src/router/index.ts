import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";
import Login from "@/views/Login.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/myaccount",
    name: "My account",
    component: () =>
      import(/* webpackChunkName: "myaccount" */ "../views/Myaccount.vue"),
  },
  {
    path: "/passwordreset",
    name: "Password reset",
    component: () =>
      import(
        /* webpackChunkName: "passwordreset" */ "../views/PasswordReset.vue"
      ),
  },
  {
    path: "/password/reset/confirm/:uid/:token",
    name: "Password reset confirm",
    component: () =>
      import(
        /* webpackChunkName: "passwordresetconfirm" */ "../views/PasswordResetConfirm.vue"
      ),
  },
  // ----------/ Modules
  {
    path: "/reports",
    name: "Reports",
    component: () =>
      import(/* webpackChunkName: "reports" */ "../views/Reports.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: '/',
  routes,
});

export default router;
