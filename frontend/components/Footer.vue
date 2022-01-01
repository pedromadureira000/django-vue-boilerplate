<template>
  <v-footer color="blue-grey darken-4" class="white--text">
		<div class="col">
			<address>
					62 99337-8753
					<br/>
					<a href="mailto:contato@phsolucoesweb.com.br" class="white--text">contato@phsolucoesweb.com.br</a>
			</address>
		</div>
		<v-spacer />
		<span>PH - Soluções Web&nbsp;</span>
		<span>- {{date.getFullYear()}}</span><br/>
  </v-footer>
</template>

<script>
export default {
	data() {
		return {
			date: new Date
		}
	},
}
</script>
<style scoped>
.v-footer {
	z-index: 42;
} 
</style>
