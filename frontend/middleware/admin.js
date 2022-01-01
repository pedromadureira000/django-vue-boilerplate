// If fail in "authenticated" middleware, it will not enter this middleware
export default async (ctx) => {
		//Checks if admin module exist in user modules
		console.log(ctx)
		if (ctx.store.state.auth.currentUser.modules.includes('admin')){  
			console.log('admin middleware passed')
			return;
		}else{
			console.log('not passed')
			ctx.redirect(302, '/')
		}
}
