<template>
  <v-app>
		<v-navigation-drawer v-model="drawer" app> 
      <v-card class="pa-3" color="blue-grey darken-4" tile>
				<!--
        <v-avatar size="70" class="mb-2">
          <img src="https://cdn.vuetifyjs.com/images/john.jpg" alt="John" />
        </v-avatar>
        <div class="white--text text-subtitle-1 font-weight-bold">
          Pedro Henrique
        </div>
				-->
				<v-btn @click.prevent="$store.dispatch('auth/checkAuthenticated')">test</v-btn>
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
    <v-app-bar color="blue-grey darken-4" dark app>
      <v-app-bar-nav-icon
        @click="drawer = !drawer"
      ></v-app-bar-nav-icon>

      <v-toolbar-title>Title</v-toolbar-title>

      <v-spacer></v-spacer>

			<v-btn 
				v-if="!logged_user"
				text
				dark
				ripple
				class="ma-0 ml-5"
				depressed
				@click="open_login_dialog($event)"
			>Login</v-btn>

			<v-menu v-else offset-y>
				<template v-slot:activator="{ on }">
					<v-btn icon v-on="on" class="ma-0 ml-5">
						<v-avatar size="45px">
							<img src="https://graph.facebook.com/4/picture?width=300&height=300">
						</v-avatar>
					</v-btn>
				</template>
				<v-card class="no-padding">
					<v-list two-line>
						<v-list-item>
							<v-list-item-avatar>
								<v-avatar>
									<img src="https://graph.facebook.com/4/picture?width=400&height=400">
								</v-avatar>
							</v-list-item-avatar>
							<v-list-item-content>
								<v-list-item-title>{{logged_user.first_name}} {{logged_user.last_name}}</v-list-item-title>
								<v-list-item-subtitle>{{logged_user.email}}</v-list-item-subtitle>
							</v-list-item-content>
						</v-list-item>
					</v-list>

					<v-divider />
					
					<v-list>
            <v-list-item to="/myaccount">
              <v-list-item-title>My Account</v-list-item-title>
            </v-list-item>
            <v-list-item @click="logout">
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
					</v-list>
				</v-card>
			</v-menu>
    </v-app-bar>

    <v-main>
      <nuxt/>
    </v-main>


    <login-dialog ref="login_dialog" />

		<v-alert v-if='$store.state.alert.showAlert' :type='$store.state.alert.alertType' style="width: 50%;" class="alert_message">
		{{$store.state.alert.alertMessage}}
		</v-alert>

  </v-app>
</template>

<script>
import loginDialog from '~/components/login-dialog.vue'

export default {
	name: "default",
	middleware: ['fwdcookies', 'auth'],
  components: {
    loginDialog
  },

	data: () => ({
    drawer: null,
	}),

  methods: {
    open_login_dialog (evt) {
      this.$refs.login_dialog.open()
      evt.stopPropagation()
    },
    logout() {
			this.$store.dispatch('auth/logout')
    },
  },

  computed: {
		logged_user(){
			return this.$store.state.auth.currentUser
		},
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
};
</script>

<style scoped>
.alert_message{
	position: fixed;
	left: 50%;
	top: 93%;
	transform: translate(-50%, -50%);
  opacity: 0.8;
}
.v-application .pa-3 {
	padding: 14px !important;
}
</style>
