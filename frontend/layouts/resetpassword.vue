<template>
  <v-app>
    <v-app-bar color="blue-grey darken-4" dark app>

      <v-toolbar-title>Password Reset</v-toolbar-title>

      <v-spacer></v-spacer>

    </v-app-bar>

    <v-main>
      <nuxt/>
    </v-main>


		<v-alert v-if='$store.state.alert.showAlert' :type='$store.state.alert.alertType' style="width: 50%;" class="alert_message">
		{{$store.state.alert.alertMessage}}
		</v-alert>

		<le-footer/>
  </v-app>
</template>

<script>
import footer from '~/components/Footer.vue';

export default {
	name: "resetpassword",
  components: {
    leFooter: footer
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
