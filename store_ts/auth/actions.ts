import {ActionTree, Commit} from "vuex"
import {RootState} from "@/store/types"
import {UserState, User} from "@/store/auth/types";
import axios from "axios";

export default (): ActionTree<UserState, RootState> => ({
	setUser({commit}: {commit: Commit}, user: User) {
		commit("SET_USER", user);
	},
	checkAuthenticated({commit, state}: {commit: Commit, state: UserState}) {
		axios.get("/api/user/checkauth").then((response) => {
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
		axios.get("/api/user/getcsrf").then(() => {
			console.log("Csrftoken recived");
			commit("setCsrf");
		});
	},
})
