module.exports = {
  lintOnSave: false,
  publicPath: './',
  productionSourceMap: false,
  outputDir: process.env.IS_LIB ? 'lib-dist' : 'dist',
  css: {
    extract: false
  },
  configureWebpack: {
    module: {
      rules: [
      ]
    }
  },
  devServer: {
    disableHostCheck: true,
    open: true,
    before(app) {
      app.use((req, res, next) => {
        req.headers['Authorization'] = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODMzNTU4OTYsInBheWxvYWQiOnsiaWQiOjE2NDY3Njg3NjMwNjU5OTUyNjQsImFkdmFuY2VkIjowfX0.f4ocqSbBtGXduHNTe2q-3vitC4euYi5_LbIFGsnK-bY';
        next();
      });
    },
  },
  chainWebpack: config => {
    const svgRule = config.module.rule('svg')
    svgRule.uses.clear()

    svgRule
      .test(/\.svg$/)
      .use('svg-url-loader')
      .loader('svg-url-loader')
  }
}