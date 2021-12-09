export default (ctx) => {
	if (!ctx.store.state.auth.currentUser){
		ctx.redirect(302, '/')
	}	
}
