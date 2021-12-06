export default ({ app }) => {
	app.$axios.defaults.xsrfHeaderName = "X-CSRFToken";
	app.$axios.defaults.xsrfCookieName = "csrftoken";
}
