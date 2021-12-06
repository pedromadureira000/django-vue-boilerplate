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
      <h4 class="mt-3">{{message}}</h4>
    </form>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";
import axios from "axios";

export default {
  mixins: [validationMixin],
  validations: {
    email: { required, email },
  },
  data() {
    return {
      email: "",
      message: "",
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
      axios({
        method: "post",
        url: "/api/user/passwordreset/users/reset_password/",
        data: { email: this.email },
      })
        .then((response) => {
          this.message = "Email has been sent."
          setTimeout(() => {
            this.message = "";
          }, 1500);
        })
        .catch(() => {
          this.message = "Server error. The email was not been sent.";
          setTimeout(() => {
            this.message = "";
          }, 1500);
        });
    }
  },
};
</script>

<style></style>
