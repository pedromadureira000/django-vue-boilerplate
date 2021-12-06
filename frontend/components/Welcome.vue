<template>
	<div class="ma-4"><p class="ma-2">{{message}}</p></div>
</template>

<script>
export default {
		data: () => ({
			message: "Please login to access modules..." 
		}),
		computed: {
			user() {
				return this.$store.state.auth.currentUser
			},
		},
		watch: {
			user(newValue, oldValue){
				console.log(`old value = ${oldValue}. New value = ${newValue}`  )
				if (newValue) {
					this.message = `Welcome ${newValue.first_name}!`
				} else {
					this.message = "See you later!" 
				}
			}	
		},
		created() {
			if (this.$store.state.auth.currentUser){
				this.message = `Welcome ${this.$store.state.auth.currentUser.first_name}!`
			} else {
				this.message = "Please login to access modules." 
			}
		}	
	}
</script>

<style>

</style>
