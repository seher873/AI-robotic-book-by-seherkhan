module.exports = {
  // Server configuration to improve stability
  server: {
    port: 3000,
    host: '0.0.0.0', // Listen on all interfaces
    serve: {
      // Serve options
      compress: true,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
        'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
      }
    }
  },
  // Add performance optimizations
  generateBuildPath: './build',
  minify: true,
  // Add development server config
  devServer: {
    hot: true,
    compress: true,
    open: false, // Don't automatically open browser
    liveReload: true,
    watchFiles: ['src/**/*', 'docs/**/*', 'static/**/*'],
    client: {
      overlay: {
        errors: true,
        warnings: false,
      },
    },
  }
};