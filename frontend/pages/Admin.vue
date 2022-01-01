<template>
  <div class="ma-3">
    <h3>Create User</h3>
    <form @submit.prevent="createUser">
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
        <v-text-field
          label="Email"
          type="email"
          v-model="email"
          :error-messages="emailErrors"
          required
          @blur="$v.email.$touch()"
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
      <v-btn
        color="primary"
        type="submit"
        :loading="loading"
        :disabled="loading"
        >Submit</v-btn
      >
    </form>

    <h3 class="mt-6">Edit User</h3>
    <v-list dense>
      <v-list-item v-for="user in users" :key="user.id">
        <template v-slot:default>
          <v-avatar size="45px" class="mr-9">
            <img src="~assets/images/default_user.jpg" />
          </v-avatar>
          <v-list-item-content>
            <v-list-item-title
              >{{ user.first_name }} {{ user.last_name }}</v-list-item-title
            >
          </v-list-item-content>
          <v-list-item-content>
            <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action>
            <user-edit-menu :user="user" @user-deleted="deleteUser(user)" />
          </v-list-item-action>
          <v-list-item-content> </v-list-item-content>
        </template>
      </v-list-item>
    </v-list>
  </div>
</template>

<script>
import {
  required,
  sameAs,
  minLength,
  maxLength,
  email,
} from "vuelidate/lib/validators";
import { validationMixin } from "vuelidate";

export default {
  middleware: ["authenticated", "admin"],
  components: {
    "user-edit-menu": require("@/components/admin/user-edit-menu.vue").default,
  },
  mixins: [validationMixin],

  data() {
    return {
      first_name: null,
      last_name: null,
      email: null,
      password: null,
      password_confirm: null,
      loading: false,
      users: [],
    };
  },

  async fetch() {
    let users = await this.$store.dispatch("auth/fetchUsersByAdmin");
    this.users.push(...users);
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
    email: {
      required,
      email,
    },
    password: {
      required,
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    password_confirm: {
      password_confirm: sameAs("password"),
    },
    userInfoGroup: [
      "first_name",
      "last_name",
      "email",
      "password",
      "password_confirm",
    ],
  },

  methods: {
    async createUser() {
      this.$v.userInfoGroup.$touch();
      if (this.$v.userInfoGroup.$invalid) {
        this.$store.dispatch(
          "setAlert",
          { message: "Please fill the form correctly.", alertType: "error" },
          { root: true }
        );
      } else {
        this.loading = true;
        let data = await this.$store.dispatch("auth/createUser", {
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          password: this.password,
        });
        if (data) {
          this.users.push(data);
        }
        this.loading = false;
      }
    },
    deleteUser(userToDelete) {
      this.users = this.users.filter((user) => user != userToDelete);
    },
  },

  computed: {
    firstNameErrors() {
      const errors = [];
      if (!this.$v.first_name.$dirty) return errors;
      !this.$v.first_name.required && errors.push("First name is required.");
      !this.$v.first_name.maxLength &&
        errors.push("This field must have up to 10 characters.");
      return errors;
    },
    lastNameErrors() {
      const errors = [];
      if (!this.$v.last_name.$dirty) return errors;
      !this.$v.last_name.required && errors.push("Last name is required.");
      !this.$v.last_name.maxLength &&
        errors.push("This field must have up to 10 characters.");
      return errors;
    },
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Must be valid e-mail");
      !this.$v.email.required && errors.push("E-mail is required");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.required && errors.push("Password is required.");
      !this.$v.password.maxLength &&
        errors.push("This field must have up to 20 characters.");
      !this.$v.password.minLength &&
        errors.push("This field must have at least 6 characters.");
      this.password === this.current_password &&
        errors.push(
          "The password should not be equal to the current password."
        );
      return errors;
    },
    passConfirmErrors() {
      const errors = [];
      if (!this.$v.password_confirm.$dirty) return errors;
      !this.$v.password_confirm.password_confirm &&
        errors.push("Password must be iqual.");
      return errors;
    },
  },
};
</script>
<style scoped>
.v-application .mb-3 {
  margin-bottom: 0px !important;
}
</style>
