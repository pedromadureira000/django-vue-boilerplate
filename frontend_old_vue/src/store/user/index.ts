import Vue from "vue";
import Vuex, {Module} from "vuex";
import {RootState} from "@/store/types"
import {UserState} from "@/store/user/types";
import {mutations} from "@/store/user/mutations";
import {actions} from "@/store/user/actions";


Vue.use(Vuex);

const state: UserState = {
	user: null,
	csrftoken: ""
}
export const user: Module<UserState, RootState> = {
	state, mutations, actions
};
