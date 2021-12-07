interface menuItem {
	title: string;
	icon: string;
	to: string;
}

class User {
	first_name!: string;
	last_name!: string;
	email!: string;
	modules!: menuItem[];
}

interface UserState {
	currentUser: User | null,
	csrftoken: string
}

export const state = (): UserState => ({
	currentUser: null,
	csrftoken: ""
})  

// ---------------------------/actions
import {ActionTree, Commit} from "vuex"
import {RootState} from "@/store/index"

export const actions: ActionTree<UserState, RootState> = {
	setUser({commit}: {commit: Commit}, user: User) {
		commit("SET_USER", user);
	},
	checkAuthenticated({commit, state}: {commit: Commit, state: UserState}) {
		this.$axios.get("/api/user/checkauth").then((response) => {
			console.log("the user is already authenticated");
			commit("SET_USER", response.data);
		}).catch(() => {
			console.log("not Authenticated")
			if (state.currentUser) {
				commit("deleteUser");
			}
		});
	},
	getCsrf({commit}: {commit: Commit}) {
		this.$axios.get("/api/user/getcsrf").then(() => {
			console.log("Csrftoken recived");
			commit("setCsrf");
		});
	},
}


// ---------------------------/mutations
import {MutationTree} from "vuex"

export const mutations: MutationTree<UserState> = { 
	SET_USER(state, user: User) {
		state.currentUser = user;
	},
	deleteUser(state) {
		state.currentUser = null;
	},

	setCsrf(state) {
		let name = "csrftoken"
		let cookieValue = "";
		if (document.cookie && document.cookie !== "") {
			const cookies = document.cookie.split(";");
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === name + "=") {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		state.csrftoken = cookieValue;
	},
	setCsrfOnServer(state, token: string){
		state.csrftoken = token
	}
}
