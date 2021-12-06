import {MutationTree} from "vuex"
import {UserState, User} from "@/store/user/types";
export const mutations: MutationTree<UserState> = {
	SET_USER(state, user: User) {
		state.user = user;
	},
	deleteUser(state) {
		state.user = null;
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
}
