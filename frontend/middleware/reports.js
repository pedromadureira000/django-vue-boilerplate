// If fail in "authenticated" middleware, it will not enter this middleware
export default async (ctx) => {
		//Checks if report module exist in user modules
		console.log(ctx)
		if (ctx.store.state.auth.currentUser.modules.includes('reports')){  
			console.log('reports middleware passed')
			return;
		}else{
			console.log('not passed')
			ctx.redirect(302, '/')
		}
}
