export default { 
	SET_USER(state, user) {
		state.currentUser = user;
		console.log("this is currentUser: ", state.currentUser)

	},
	deleteUser(state) {
		console.log('deleteUser')
		state.currentUser = null;
	},

	setCsrf(state) {
		let name = "csrftoken"
		let cookieValue = "";
		if (document.cookie && document.cookie !== "") {
			const cookies = document.cookie.split(";");
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				//Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === name + "=") {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		state.csrftoken = cookieValue;
	},
	setCsrfOnServer(state, token){
		state.csrftoken = token
		// console.log('asdfasdf?: ', state.csrftoken)
	}
}

