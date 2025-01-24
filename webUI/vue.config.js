const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: '../templates',
  devServer: {
    proxy: {
    '/api': {
        target: 'http://localhost:8980', // 你的后端服务地址
        changeOrigin: true,
      },
}}
})
