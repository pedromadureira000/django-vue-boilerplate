export default {
	setUser({commit}, user) {
		commit("SET_USER", user);
	},
	checkAuthenticated({commit, state}) {
		this.$axios.$get("/api/user/checkauth").then((data) => {
			console.log('checkAuthenticated action!')
			commit("SET_USER", data);
		}).catch(() => {
			console.log("not Authenticated")
			if (state.currentUser) {
				console.log('deleteUser mutation')
				commit("deleteUser");
			}
		});
	},
	// checkAuthenticated({commit, state}) {
		// this.$axios.$get("/api/user/checkauth").then((response) => {
			// console.log("the user is already authenticated");
			// commit("SET_USER", response.data);
		// }).catch(() => {
			// console.log("not Authenticated")
			// if (state.currentUser) {
				// commit("deleteUser");
			// }
		// });
	// },
	getCsrf({commit}) {
		this.$axios.$get("/api/user/getcsrf").then(() => {
			console.log("Csrftoken recived");
			commit("setCsrf");
		});
	},
}
