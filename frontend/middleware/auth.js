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
		// ctx.store.commit('toggleDrawer') 

		const sessionid = ctx.req.headers.cookie
			.split(";")
			.find(c => c.trim().startsWith("sessionid="));
		if (!sessionid) {
			return;
		}

		// await ctx.store.dispatch("auth/checkAuthenticated");  // ==> this will no work. Will add user after retrive the page

		await ctx.app.$axios.get("/api/user/checkauth").then((response) => {
			console.log('user is authenticated!')
			ctx.store.commit("auth/SET_USER", response.data);
		}).catch((error) => {
			console.log("not Authenticated")
			console.log(error)
		});
	}

}

