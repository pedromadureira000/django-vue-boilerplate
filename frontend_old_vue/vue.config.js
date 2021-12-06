// module.exports = {
  // outputDir: "../backend/core/templates",
  // assetsDir: "../static",
// };

module.exports = {
  devServer: {
    proxy: {
      "^/api/": {
        target: "http://localhost:8000",
        changeOrigin: true,
        logLevel: "debug",
        pathRewrite: { "^/api": "/api" },
      },
    },
  },

  transpileDependencies: [
    'vuetify'
  ]
};

