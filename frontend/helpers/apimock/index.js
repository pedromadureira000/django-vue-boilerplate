import {eraseCookie, setCookie} from '../functions'
import {user, admin, users} from './db_user'

function mockasync (data) {
  return new Promise((resolve, reject) => {
    setTimeout(() => resolve(data), 600)
  })
}

function mockasyncerror (message = 'Something went wrong') {
  return new Promise((resolve, reject) => {
    setTimeout(() => reject(new Error(message)), 600)
  })
}

export default {	
	checkAuthenticated(){
		return mockasync(user)
	},

	getCsrf(){
		setCookie('csrftoken', 'sometoken', 1)
		return mockasync('ok')
	},

	login(payload){ 
		if (typeof payload.email === 'string' && typeof payload.password === 'string' && typeof payload.csrftoken === 'string'){
		if (payload.email === "admin@admin.com"){
			return mockasync(admin)
		}else{
			setCookie('sessionid', 'anothertoken', 1)
			return mockasync(user)
		}
		}else {
			mockasyncerror()
		}
	},

	logout(){
		eraseCookie('sessionid')
		eraseCookie('csrftoken')
		return mockasync("User logged out.")
	},

	updateProfile(payload){
		if (typeof payload.first_name === 'string' && typeof payload.last_name === 'string'){
			let updated_user = {...user, ...payload}
			return mockasync(updated_user)	
		}else {
			mockasyncerror()
		// if (typeof payload.email === 'string' && typeof payload.password === 'string' && typeof payload.csrftoken === 'string'){
		}
	},

	updatePassword(payload){
		if (typeof payload.current_password === 'string' && typeof payload.password === 'string'){
			eraseCookie('sessionid')
			eraseCookie('csrftoken')
			return mockasync("Passsword changed.")
		}else {
			mockasyncerror()
		}

	},

	passwordReset(email){
		if (typeof email === 'string'){
			return mockasync("Email was been sent")
		}else {
			mockasyncerror()
		}
	},

	passwordResetConfirm(payload){
		if (typeof payload.new_password === 'string' && typeof payload.token === 'string' && typeof payload.uid === 'string'){
			return mockasync("Passsword was been changed")
		}else {
			mockasyncerror()
		}
	},

	createUser(payload){
		if (typeof payload.first_name === 'string' && typeof payload.last_name === 'string' &&
				typeof payload.email === 'string' && typeof payload.password === 'string'  
				)
				{
					delete payload.password	
					return mockasync(payload)	
				}
		else {
			mockasyncerror("createUser Error")
		}
	},

	fetchUsersByAdmin(){
		return mockasync(users)
	},

	deleteUserByAdmin(id){
		return mockasync('ok')	
	}
}
