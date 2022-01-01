<template>
  <v-app>
		<v-navigation-drawer v-model="drawer" app> 
      <v-card class="pa-3" color="blue-grey darken-4" tile>
				<v-btn @click.prevent="$store.dispatch('auth/checkAuthenticated')">test</v-btn>
      </v-card>

      <v-list nav dense>
        <v-list-item
          v-for="item in currentMenuItems"
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
							<img src="~assets/images/default_user.jpg">
						</v-avatar>
					</v-btn>
				</template>
				<v-card class="no-padding">
					<v-list two-line>
						<v-list-item>
							<v-list-item-avatar>
								<v-avatar>
									<img src="~assets/images/default_user.jpg">
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

    <login-dialog ref="login_dialog"/>

    <session-error-dialog/>

		<v-alert v-if='$store.state.alert.showAlert' :type='$store.state.alert.alertType' style="width: 50%;" class="alert_message">
		{{$store.state.alert.alertMessage}}
		</v-alert>

		<le-footer/>
  </v-app>
</template>

<script>
import footer from '~/components/Footer.vue';
import loginDialog from '~/components/login-dialog.vue'
import sessionErrorDialog from '~/components/session-error-dialog.vue'

export default {
	name: "default",
	middleware: ['fwdcookies', 'auth'],
  components: {
    loginDialog,
		sessionErrorDialog,
    leFooter: footer
  },

	data: () => ({
    drawer: null,
		defaultMenuItems: [
			{ title: "Home", icon: "mdi-home", to: "/" },
			{ title: "About", icon: "mdi-help-box", to: "/about" },
		],
		allUserModules: [
			{"name": "reports", "title": "Reports", "icon":"mdi-clipboard-list-outline", "to": "/reports"},
			{"name": "admin", "title": "Admin", "icon":"mdi-account-tie", "to": "/admin"}	
		]
	}),

  methods: {
    open_login_dialog(evt) {
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
		currentMenuItems() {
			let user = this.$store.state.auth.currentUser;
			if (user) {
				/* return defultMenuItems array concatenated with user modules with 'About' in the end. */
				return this.defaultMenuItems
					.slice(0, 1)
					.concat(this.allUserModules.filter(module => this.$store.state.auth.currentUser.modules.includes(module.name)))
					.concat(this.defaultMenuItems.slice(1, 2));
			} else {
				return this.defaultMenuItems;
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
	z-index: 999;
}
.v-application .pa-3 {
	padding: 14px !important;
}
</style>
