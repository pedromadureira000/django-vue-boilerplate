import colors from 'vuetify/es5/util/colors'

const _isdev = process.env.DEV
const _apimock = process.env.API_MOCK 
const _apijs = _apimock ? 'apimock' : 'api'
// import pt from 'vuetify/es5/locale/pt'

export default {

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - frontend',
    title: 'frontend',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.jpg' }
    ]
  },

  loading: { color: '#fff' },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
		// {src: '@/plugins/axios', ssr: false},
		// '@/plugins/axios',
		'@/plugins/vuetify',
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
		'@nuxtjs/proxy',
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
	axios: {
		// credentials: true,
	},

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      // dark: true,
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    },
    // lang: {
      // locales: { pt },
      // current: 'pt'
    // },
  },

	// Build Configuration: https://go.nuxtjs.dev/config-build
	build: {
		//You can extend webpack config here
		// loaders: {
			// sass: {
				// implementation: require('sass'),
			// },
		// },
		extend (config, ctx) {
			const home = config.resolve.alias['~']
			config.resolve.alias['~api'] = home + '/helpers/' + _apijs
		}
	},

	proxy: _isdev && !_apimock ? {
		'/api': 'http://127.0.0.1:8000/',
	} : null,

	transpileDependencies: [
		'vuetify'
	],

	env: {
		// test: process.env.test || 'test'
	},
	
  // router: {
    // middleware: ['fwdcookies', 'auth']
  // },
}
