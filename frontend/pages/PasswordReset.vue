<template>
  <div class="ma-4">
    <h2>Password reset</h2>
    <p>
      Forgotten your password? Enter your email address below, and we’ll email
      instructions for setting a new one.
    </p>
    <form class="ma-4 form">
      <v-text-field
        v-model="email"
        :error-messages="emailErrors"
        label="E-mail"
        required
        @blur="$v.email.$touch()"
      ></v-text-field>
      <v-btn class="mr-4 mt-3" @click="passwordReset"> submit </v-btn>
    </form>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],
	layout: 'resetpassword', 
  validations: {
    email: { required, email },
  },
  data() {
    return {
      email: "",
    };
  },
  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Must be valid e-mail");
      !this.$v.email.required && errors.push("E-mail is required");
      return errors;
    },
  },
  methods: {
    passwordReset() {
			this.$store.dispatch('auth/passwordReset', this.email)
    }
  },
};
</script>

<style></style>
