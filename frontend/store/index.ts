interface menuItem {
	title: string;
	icon: string;
	to: string;
}

export interface RootState {
	menuItems: menuItem[];
}

export const state = ():RootState  => ({
    menuItems: [
      { title: "Home", icon: "mdi-home", to: "/" },
      { title: "About", icon: "mdi-help-box", to: "/about" },
    ],
});

// import {MutationTree} from "vuex"
// export const mutations: MutationTree<RootState> = {
	// toggleDrawer(state){
		// state.drawer = !state.drawer
	// }
// }

