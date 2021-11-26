<template>
  <form class="ma-4 form">
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
    <router-link to="/passwordreset" tabindex="-1">I forgot my password</router-link><br />

    <v-btn class="mr-4 mt-3" @click="login"> submit </v-btn>
    <h4 class="mt-3">{{ message }}</h4>
  </form>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";
import axios from "axios";
export default {
  mixins: [validationMixin],

  validations: {
    email: { required, email },
    password: { required },
  },

  data: () => ({
    email: "",
    password: "",
    message: "",
  }),

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

  methods: {
    login() {
      axios({
        method: "post",
        url: "/api/user/login",
        data: { email: this.email, password: this.password },
        headers: { "X-CSRFToken": this.$store.state.user.csrftoken },
      })
        .then((response) => {
          this.$store.dispatch("setUser", response.data);
          this.$store.commit("setCsrf");
          this.$router.push("/");
        })
        .catch(() => {
          this.message = "Login Failed";
          setTimeout(() => {
            this.message = "";
          }, 1500);
        });
    },
  },
  beforeCreated() {
    /* check if the user exists, if true, redirect to / */
    if (this.$store.state.user.user) {
      this.$router.push("/");
    }
  },
  created() {
    if (!document.cookie.includes("csrftoken")) {
      this.$store.dispatch("getCsrf");
    }
  },
};
</script>
<style>
.form {
  width: 500px;
}
</style>
