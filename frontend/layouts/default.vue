<template>
  <v-app>
		<v-navigation-drawer v-model="drawer" app> 
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
        @click="drawer = !drawer"
      ></v-app-bar-nav-icon>

      <v-toolbar-title>Title</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn
        depressed
        color="primary"
        v-if="!$store.state.auth.currentUser"
        to="/login"
      >
        Login
      </v-btn>

      <div class="text-center" v-else>
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" dark v-bind="attrs" v-on="on">
              {{ $store.state.auth.currentUser.first_name }}
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
      <nuxt/>
    </v-main>
  </v-app>
</template>

<script>
export default {
	name: "default",
	middleware: ['auth'],
	data: () => ({
    drawer: null,
	}),
  methods: {
    logout() {
      this.$axios({
        method: "post",
        url: "/api/user/logout",
      })
        .then(() => {
          this.$store.commit("auth/deleteUser");
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
      let user = this.$store.state.auth.currentUser;
      let menu = this.$store.state.menuItems;
      if (user) {
        /* return MenuItems array with 'About' menuItems in the end. */
        return menu
          .slice(0, 1)
          .concat(user.modules)
          .concat(menu.slice(1, 2));
      } else {
        return this.$store.state.menuItems;
      }
    },
  },
	mounted(){
	console.log('mounted')
	},
	created(){
	console.log('created')
	}
};
</script>
