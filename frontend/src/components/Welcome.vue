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
				return this.$store.state.user.user
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
			if (this.$store.state.user.user){
				this.message = `Welcome ${this.$store.state.user.user.first_name}!`
			} else {
				this.message = "Please login to access modules." 
			}
		}	
	}
</script>

<style>

</style>
