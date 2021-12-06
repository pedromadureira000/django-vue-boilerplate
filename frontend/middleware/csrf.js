export default async (ctx) => {
	if (process.server){
		console.log('middleware csrf' )

		if (ctx.req.headers.cookie){
			let csrftoken = ctx.req.headers.cookie
				.split(";")
				.find(c => c.trim().startsWith("csrftoken="));
			if (csrftoken) {
				let token = csrftoken.split("=")[1];
				console.log('saving csft in store, on server side.')
				ctx.store.commit('auth/setCsrfOnServer', token) 
			} else {
				// await ctx.app.$axios.get("/api/user/getcsrf").then((response) => {
				// console.log('wtf: ', response)
				// });
			}
		}else{
			// await ctx.app.$axios.get("/api/user/getcsrf").then((response) => {
				// console.log('wtf: ', response.headers['set-cookie'][0].split(";").find(c => c.trim().startsWith("csrftoken=")))
				// let csrftoken = response.headers['set-cookie'][0]
				// .split(";")
				// .find(c => c.trim().startsWith("csrftoken="));
				// let token = csrftoken.split("=")[1];
				// console.log(token)
				// ctx.store.commit('auth/setCsrfOnServer', token) 
			// }).catch(()=> {console.log('erro')});
		}
	}
	if (process.client){
		if (!document.cookie.includes("csrftoken")) {
			ctx.store.dispatch("getCsrf");
		}
	} 	
}
