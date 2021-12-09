interface menuItem {
	title: string;
	icon: string;
	to: string;
}

export interface RootState {
	menuItems: menuItem[],
	alert: {
		alertMessage: string,
		alertType: string
		showAlert: boolean,
	},
}

export const state = ():RootState  => ({
    menuItems: [
      { title: "Home", icon: "mdi-home", to: "/" },
      { title: "About", icon: "mdi-help-box", to: "/about" },
    ],
		alert: {
			alertMessage: '',
			alertType: 'info',
			showAlert: false
		}
});

import {MutationTree} from "vuex"
export const mutations: MutationTree<RootState> = {
	setAlert(state, payload ){
		state.alert = {alertMessage: payload.message, alertType: payload.alertType, showAlert: payload.showAlert}	
	}
}

import {ActionTree, Commit} from "vuex"
export const actions: ActionTree<RootState, RootState> = {
	setAlert({commit}: {commit: Commit}, payload: {alertMessage: string, alertType: string, showAlert?: boolean, timeout?: number}){
		payload['showAlert'] = true
		payload['timeout'] =  payload['timeout'] ? payload['timeout'] : 2500  // <<<<<<<<< Default value
		commit('setAlert', payload)
		setTimeout(() => {
			commit('setAlert', {alertMessage: '', alertType: 'info', showAlert: false})
		}, payload.timeout);
	}
}
