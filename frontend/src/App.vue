<template>
  <v-app>
    <v-navigation-drawer v-model="$store.state.drawer" app>
      <v-card class="pa-4" color="blue darken-4" tile>
        <v-avatar size="70" class="mb-2">
          <img src="https://cdn.vuetifyjs.com/images/john.jpg" alt="John" />
        </v-avatar>
        <div class="white--text text-subtitle-1 font-weight-bold">
          Pedro Henrique
        </div>
      </v-card>

      <v-list nav dense>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.to"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar color="blue darken-4" dark app>
      <v-app-bar-nav-icon
        @click="$store.state.drawer = !$store.state.drawer"
      ></v-app-bar-nav-icon>

      <v-toolbar-title>Title</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn
        depressed
        color="primary"
        v-if="!$store.state.user.user"
        to="/login"
      >
        Login
      </v-btn>

      <div class="text-center" v-else>
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" dark v-bind="attrs" v-on="on">
              {{ $store.state.user.user.first_name }}
            </v-btn>
          </template>
          <v-list>
            <v-list-item to="/myaccount">
              <v-list-item-title>My Account</v-list-item-title>
            </v-list-item>
            <v-list-item @click="logout">
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import { doesHttpOnlyCookieExist } from "@/store/functions";
export default Vue.extend({
  name: "App",
  data: () => ({}),
  methods: {
    logout() {
      axios({
        method: "post",
        url: "/api/user/logout",
      })
        .then(() => {
          this.$store.commit("deleteUser");
          this.$router.push("/login");
          /* if (this.$route.path !== "/") { */
            /* this.$router.push("/login"); */
          /* } */
        })
        .catch(() => {
          console.log("logout error");
        });
    },
  },
  computed: {
    menuItems() {
      let user = this.$store.state.user.user;
      let menu = this.$store.state.menuItems;
      if (user) {
        /* return MenuItems array with 'About' menuItems in the end. */
        return menu
          .slice(0, 1)
          //this error doesn't really exist
          .concat(user.modules)
          .concat(menu.slice(1, 2));
      } else {
        return this.$store.state.menuItems;
      }
    },
  },
  created() {
    if (doesHttpOnlyCookieExist("sessionid")) {
      this.$store.dispatch("checkAuthenticated");
    }
		
    if (document.cookie.includes("csrftoken")){		
      this.$store.commit("setCsrf")	
    }
  },
});
</script>
