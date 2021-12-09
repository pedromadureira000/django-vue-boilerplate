import api from '~api'

export default async (ctx) => {
		// A middleware can be asynchronous. To do this return a  Promise or use async/await.
	if (process.server && ctx.req.headers.cookie){
		let csrftoken = ctx.req.headers.cookie
			.split(";")
			.find(c => c.trim().startsWith("csrftoken="));
		if (!csrftoken) {
			return;
		}
		const token = csrftoken.split("=")[1];
		ctx.store.commit('auth/setCsrfOnServer', token) 

		const sessionid = ctx.req.headers.cookie
			.split(";")
			.find(c => c.trim().startsWith("sessionid="));
		if (!sessionid) {
			return;
		}
		let data = await api.checkAuthenticated()	
		if (!data['some_error']){
			console.log(data)
			ctx.store.commit('auth/SET_USER', data )	
		} else {
			console.log(data)
		}
	}
}
