<template>
  <div class="ma-4">
      <h3 class="mt-4">Change Password</h3>
      <form @submit.prevent="passwordResetConfirm">
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
            @keyup.enter="passwordResetConfirm"
          />
        </div>
        <v-btn color="primary" type="submit">Save</v-btn>

        <h4 class="mt-3">{{ message }}</h4>
      </form>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import {
  required,
  sameAs,
  minLength,
  maxLength,
} from "vuelidate/lib/validators";
import axios from "axios";

export default {
  mixins: [validationMixin],
  validations: {
    password: {
      required,
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    password_confirm: {
      password_confirm: sameAs("password"),
    },
  },
  data() {
    return {
      password: "",
      password_confirm: "",
      message: ""
    };
  },
  computed: {
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.required && errors.push("Password is required.");
      !this.$v.password.maxLength && errors.push("This field must have up to 20 characters.");
      !this.$v.password.minLength && errors.push("This field must have at least 6 characters.");
      return errors;
    },
    passConfirmErrors() {
      const errors = [];
      if (!this.$v.password_confirm.$dirty) return errors;
      /* !this.$v.password_confirm.required && errors.push("Password is required."); */
      !this.$v.password_confirm.password_confirm && errors.push("Password must be iqual.");
      return errors;
    },
  },
  methods: {
    passwordResetConfirm() {
      axios({
        method: "post",
        url: "/api/user/passwordreset/users/reset_password_confirm/",
        data: { new_password: this.password, token: this.$route.params.token, uid: this.$route.params.uid},
      })
        .then(() => {
          this.message = "The password was been changed"
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
