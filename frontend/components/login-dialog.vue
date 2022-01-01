<template>
  <v-dialog v-model="visible" max-width="500px">
    <v-card>
      <v-card-title>Log in</v-card-title>
      <v-card-text>
        <v-container fluid>
					<v-text-field
						v-model="email"
						:error-messages="emailErrors"
						label="E-mail"
						required
						@blur="$v.email.$touch()"
					></v-text-field>
					<v-text-field
						v-model="password"
						:error-messages="passwordErrors"
						label="Password"
						required
						@blur="$v.password.$touch()"
						type="password"
						@keyup.enter="login"
					></v-text-field>

					<router-link
						to="/passwordreset" 
						tabindex="-1"
						@click="visible = false"
					>
						<div @click="visible = false">I forgot my password</div>
					</router-link><br />

        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
				<!--<v-btn class="mr-4 mt-3" @click="login()"> submit </v-btn> -->
				<v-btn class="blue--text darken-1" text @click="close()">Cancel</v-btn>
        <v-btn class="blue--text darken-1" text @click="login()" :loading="loading" :disabled="loading">Login</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],

  validations: {
    email: { required, email },
    password: { required },
  },

  data () {
    return {
      visible: false,
      loading: false,
      email: '',
      password: '',
    }
  },

  methods: {
    open() {
      this.visible = true
    },
    close () {
      this.visible = false
    },
    async login() {
      this.loading = true
			await this.$store.dispatch('auth/login', {email: this.email, password: this.password} )
			if (this.$store.state.auth.currentUser){
				this.visible = false
			}      
			this.loading = false
    },
  },

  computed: {
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.required && errors.push("Password is required.");
      return errors;
    },
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Must be valid e-mail");
      !this.$v.email.required && errors.push("E-mail is required");
      return errors;
    },
  },

	watch: {
		visible(newvalue, oldvalue) {
			if (newvalue === true && !this.$store.state.auth.csrftoken){
				this.$store.dispatch('auth/getCsrf')		
			}
		}
	},
}
</script>
