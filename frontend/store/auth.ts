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
import {ActionTree, Commit, Dispatch} from "vuex"
import {RootState} from "@/store/index"
 // @ts-ignore: This module is dynamically added in nuxt.config.js
import api from '~api'

export const actions: ActionTree<UserState, RootState> = {

// ------/API
	
	async checkAuthenticated({commit, state}: {commit: Commit, state: UserState}) {
		try {
			let data: any = await api.checkAuthenticated()
			console.log(data)
			commit("SET_USER", data);
		} catch (error) {
			console.log(error);
		}	
	},

	getCsrf({commit}: {commit: Commit}) {
		try {
			let data: any = api.getCsrf() 
			console.log("Csrftoken recived");
			commit("setCsrf");
			
		} catch (error) {
			console.log(error)	
		}
	},

	async login({commit, dispatch, state}: {commit: Commit, dispatch: Dispatch, state: UserState}, payload: any){
		payload['csrftoken'] = state.csrftoken
		try {
			let data = await api.login(payload)
			console.log(data)
			commit("SET_USER", data);
			commit("setCsrf");
			dispatch('setAlert', {message: "Logged in with success.", alertType: 'success'}, { root: true })
		} catch(e){
			console.log('error when trying to login: ', e)
			dispatch('setAlert', {message: "Login Failed", alertType: 'error'}, { root: true })
			// return 'not ok'
		}
	},
	
	async logout({commit, dispatch}: {commit: Commit, dispatch: Dispatch}){
		try {
		let data = await api.logout()
		console.log(data)
		commit("deleteUser");
		dispatch('setAlert', {message: "Logged out in with success.", alertType: 'success'}, { root: true })
		this.$router.push('/')
		} catch (error) {
			console.log('error when trying to log out: ', error )
			//>>>>>>>>>>>>>>>>>>>>>>TODO<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		}
	},

	async profileUpdate({commit, dispatch}: {commit: Commit, dispatch: Dispatch,}, payload: any){
		try {
		let data = await api.updateProfile(payload)
		console.log('>>',data)
		commit('SET_USER', data )
		dispatch('setAlert', {message: "Your profile has been updated.", alertType: 'success'}, { root: true })
		}
		catch(e){
			console.log('error in profileUpdate action: ', e);
			dispatch('setAlert', {message: "Something get wrong when trying to update profile.", alertType: 'error'}, { root: true })
		}
	},

	async updatePassword({commit, dispatch}: {commit: Commit, dispatch: Dispatch,}, payload: any){
		try {
			let data = await api.updatePassword(payload)
			console.log('>>>>>>>>>>', data)
			commit('deleteUser')
			dispatch('setAlert', {message: "Your password has been updated.", alertType: 'success'}, { root: true })
			setTimeout(() => {
				this.$router.push('/')
			}, 600);
		}
		catch(e){
			console.log('error in updatePassword action: ', e);
			dispatch('setAlert', {message: "Something get wrong when trying to update password.", alertType: 'error'}, { root: true })
		}
	},

	async passwordReset({commit, dispatch}: {commit: Commit, dispatch: Dispatch,}, payload: any){
		try {
			await api.passwordReset(payload)
			dispatch('setAlert', {message: "Email has been sent", alertType: 'success'}, { root: true })
		}
		catch(e){
			dispatch('setAlert', {message: "Something get wrong, the email was not been sent.", alertType: 'error'}, { root: true })
		}
	},

	async passwordResetConfirm({dispatch}: {dispatch: Dispatch,}, payload: any){
		try {
			let data: any = await api.passwordResetConfirm(payload)
			if (data['error']){
				if (data.message === 'Invalid token for given user.'){
					dispatch('setAlert', {message: "This link is invalid." , alertType: 'error'}, { root: true })
				} else {
					dispatch('setAlert', {message: data.message , alertType: 'error'}, { root: true })
				}
			} else{
				dispatch('setAlert', {message: "The password was been changed", alertType: 'success'}, { root: true })
			}
		}
		catch(e){
			console.log('>>>>>>>>>>', e)	
			dispatch('setAlert', {message: "Something get wrong, the password was not been changed.", alertType: 'error'}, { root: true })
		}
	}
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
