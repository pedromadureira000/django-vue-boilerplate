<template>
  <div>
    <div class="ma-3">
      <h3>Update Account Information</h3>
      <form @submit.prevent="infoSubmit">
        <div class="mb-3">
          <v-text-field
            label="First Name"
            v-model="first_name"
            :error-messages="firstNameErrors"
            required
            @blur="$v.first_name.$touch()"
          />
        </div>
        <div class="mb-3">
          <v-text-field
            label="Last Name"
            v-model="last_name"
            :error-messages="lastNameErrors"
            required
            @blur="$v.last_name.$touch()"
          />
        </div>
        <div class="mb-3">
          <v-text-field label="Email" type="email" v-model="email" disabled />
        </div>
        <v-btn color="primary" type="submit">Save</v-btn>
      </form>

      <h3 class="mt-4">Change Password</h3>
      <p class="caption">After change your password you will be logged out.</p>

      <form @submit.prevent="passwordSubmit">
        <div class="mb-3">
          <v-text-field
            type="password"
            label="Current password"
            v-model="current_password"
            :error-messages="currentPassErrors"
            required
            @blur="$v.current_password.$touch()"
          />
        </div>
        <div class="mb-3">
          <v-text-field
            type="password"
            label="Password"
            v-model="password"
            :error-messages="passwordErrors"
            required
            @blur="$v.password.$touch()"
          />
        </div>
        <div class="mb-3">
          <v-text-field
            type="password"
            label="Password Confirm"
            v-model="password_confirm"
            :error-messages="passConfirmErrors"
            required
            @blur="$v.password_confirm.$touch()"
          />
        </div>
        <v-btn color="primary" type="submit">Save</v-btn>
      </form>
    </div>
  </div>
</template>

<script>
import {
  required,
  sameAs,
  minLength,
  maxLength,
} from "vuelidate/lib/validators";
import { validationMixin } from "vuelidate";

export default {
	middleware: ['authenticated'],
  mixins: [validationMixin],

  data() {
    return {
			first_name: this.$store.state.auth.currentUser.first_name,
			last_name: this.$store.state.auth.currentUser.last_name,
			email: this.$store.state.auth.currentUser.email,
      current_password: "",
      password: "",
      password_confirm: "",
    };
  },

  validations: {
    first_name: {
      required,
      maxLength: maxLength(10),
    },
    last_name: {
      required,
      maxLength: maxLength(10),
    },
    current_password: {
      required,
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    password: {
      required,
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    password_confirm: {
      password_confirm: sameAs("password"),
    },
    profileGroup: ["first_name", "last_name"],
    passwordUpdateGroup: ["current_password","password", "password_confirm"],
  },

  methods: {
    infoSubmit() {
			if (
				this.first_name === this.$store.state.auth.currentUser.first_name &&
				this.last_name === this.$store.state.auth.currentUser.last_name
			){ this.$store.dispatch('setAlert', {message: "You must change some field to update profile.", alertType: 'warning'}, { root: true }) }
			else {
				this.$store.dispatch('auth/profileUpdate', {
					first_name: this.first_name,
					last_name: this.last_name,
				})
			}	
    },
    passwordSubmit() {
			this.$store.dispatch('auth/updatePassword', {password: this.password, current_password: this.current_password})
    },
  },
  computed: {
    firstNameErrors() {
      const errors = [];
      if (!this.$v.first_name.$dirty) return errors;
      !this.$v.first_name.required && errors.push("First name is required.");
      !this.$v.first_name.maxLength && errors.push("This field must have up to 10 characters.");
      return errors;
    },
    lastNameErrors() {
      const errors = [];
      if (!this.$v.last_name.$dirty) return errors;
      !this.$v.last_name.required && errors.push("Last name is required.");
      !this.$v.last_name.maxLength && errors.push("This field must have up to 10 characters.");
      return errors;
    },
    currentPassErrors() {
      const errors = [];
      if (!this.$v.current_password.$dirty) return errors;
      !this.$v.current_password.required && errors.push("Password is required.");
      !this.$v.current_password.maxLength && errors.push("This field must have up to 20 characters.");
      !this.$v.current_password.minLength && errors.push("This field must have at least 6 characters.");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.required && errors.push("Password is required.");
      !this.$v.password.maxLength && errors.push("This field must have up to 20 characters.");
      !this.$v.password.minLength && errors.push("This field must have at least 6 characters.");
      this.password === this.current_password && errors.push("The password should not be equal to the current password.")
      return errors;
    },
    passConfirmErrors() {
      const errors = [];
      if (!this.$v.password_confirm.$dirty) return errors;
      /* !this.$v.password_confirm.required && errors.push("Password is required."); */
      !this.$v.password_confirm.password_confirm && errors.push("Password must be iqual.");
      return errors;
    },
  }
}
</script>
<style scoped>
.v-application .mb-3 {
    margin-bottom: 0px !important;
}
</style>
