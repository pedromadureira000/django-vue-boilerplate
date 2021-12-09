import axios from '~/plugins/axios'

export default {
	async checkAuthenticated(){
		// return await axios.get("/api/user/checkauth").then((data)=> {return data.data}).catch((error) => {return {some_error: error}})
		return await axios.get("/api/user/checkauth").then((data)=> {return data.data}).catch((error) => {return {some_error: error.response.data}})
	},
	async getCsrf(){
		return await axios.get("/api/user/getcsrf").then(() => {
			return 'ok'
	 }).catch(() => { return 'error'})
	},
	async login(payload){ 
		return await axios({
			method: "post",
			url: "/api/user/login",
			data: { email: payload.email, password: payload.password },
			headers: { "X-CSRFToken": payload.csrftoken },
		})
			.then((response) => {
				return response.data
			})
		},	
	async logout(){
		return await axios({
				method: "post",
				url: "/api/user/logout",
			})
				.then(() => {
					return 'ok'
				})
				.catch(() => {
					console.log("logout error");
					return 'error'
				});
		},
	async updateProfile(payload){
		return await axios({ 
		method: "put",
		url: "/api/user/profile",
		data:{
			first_name: payload.first_name,
			last_name: payload.last_name,
		}
			}).then((request) => {
					return request.data 
				})
	},
	async updatePassword(payload){
		return await axios({ 
		method: "put",
		url: "/api/user/profilepassword",
		data:{
			current_password: payload.current_password,
			password: payload.password,
		}
			}).then((request) => {
					return request.data 
				})
	},
	async passwordReset(payload){
      return await axios({
        method: "post",
        url: "/api/user/passwordreset/users/reset_password/",
        data: { email: payload },
      })
        .then(() => {})
	},
	async passwordResetConfirm(payload){
      return await axios({
        method: "post",
        url: "/api/user/passwordreset/users/reset_password_confirm/",
        data: { new_password: payload.new_password, token: payload.token, uid: payload.uid},
      })
        .then(() => {})
				.catch((error) => {return {error: 'error', message: Object.values(error.response.data)[0][0]}})
	}


}
