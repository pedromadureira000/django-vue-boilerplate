export const state = () => ({
    menuItems: [
      { title: "Home", icon: "mdi-home", to: "/" },
      { title: "About", icon: "mdi-help-box", to: "/about" },
    ],
});

export const mutations = {
	toggleDrawer(state){
		state.drawer = !state.drawer
	}
}

