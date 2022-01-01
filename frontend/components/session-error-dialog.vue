<template>
  <v-dialog v-model="$store.state.auth.sessionError" max-width="500px">
    <v-card>
      <v-card-title>Log in</v-card-title>
      <v-card-text>
        <v-container fluid>
					<p>The application is open in another window. Click "Use Here" to use whatsapp in this window.</p>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn class="blue--text darken-1" text @click="userHere()" :loading="loading" :disabled="loading">Use Here</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>

export default {
  data () {
    return {
      loading: false,
			checkSession: false 
		}
  },

  methods: {
    async userHere() {
      this.loading = true
			await this.$store.dispatch('auth/checkAuthenticated')
			if (this.$store.state.auth.currentUser){
				this.$store.commit('auth/toggleSessionError')	
			}      
			this.loading = false
    },
		async checkSessionDelay(){ 
			setTimeout(() => {
				this.checkSession = true
			}, 10000);
		}
  },

	created(){
		if (process.browser){
			this.checkSessionDelay()
			console.log('>> checkSessionDelay()')
		}
	},

	watch: {
		checkSession(newvalue, oldvalue) {
			if (newvalue === true){
				/** this.$store.dispatch('auth/')		 */
				console.log('>> api get >checkSessionDelay')
				this.checkSession = false
				this.checkSessionDelay()
			}
		}
	},
}
</script>
