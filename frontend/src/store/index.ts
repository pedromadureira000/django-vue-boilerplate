import Vue from "vue";
import Vuex, {StoreOptions} from "vuex";
import {RootState} from "@/store/types";
import {user} from "@/store/user"

Vue.use(Vuex);

const store: StoreOptions<RootState> = {
	state: {
		drawer: false,
		menuItems: [
			{title: "Home", icon: "mdi-home", to: "/"},
			{title: "About", icon: "mdi-help-box", to: "/about"},
		],
	},
	modules: {user},
};

export default new Vuex.Store<RootState>(store);
