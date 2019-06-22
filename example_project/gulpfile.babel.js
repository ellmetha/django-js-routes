import '@babel/polyfill';

import ExtractTextPlugin from 'extract-text-webpack-plugin';
import gulp from 'gulp';
import env from 'gulp-env';
import mjml from 'gulp-mjml';
import gutil from 'gulp-util';
import path from 'path';
import named from 'vinyl-named';
import webpack from 'webpack';
import WebpackDevServer from 'webpack-dev-server';
import webpackStream from 'webpack-stream';


/* Global variables */
const rootDir = './';
const staticDir = `${rootDir}main/static/`;
const templatesDir = `${rootDir}main/templates/`;
const PROD_ENV = gutil.env.production;
const WEBPACK_DEV_SERVER_PORT = (
  process.env.WEBPACK_DEV_SERVER_PORT ? process.env.WEBPACK_DEV_SERVER_PORT : 8080);
env.set({ NODE_ENV: PROD_ENV ? 'production' : 'debug' });

/* Directories */
const buildDir = PROD_ENV ? `${staticDir}build` : `${staticDir}build_dev`;
const sassDir = `${staticDir}sass`;
const jsDir = `${staticDir}js`;


/*
 * Global webpack config
 * ~~~~~~~~~~~~~~~~~~~~~
 */

const webpackConfig = {
  mode: PROD_ENV ? 'production' : 'development',
  output: {
    filename: 'js/[name].js',
    publicPath: '/static/',
  },
  resolve: {
    modules: ['node_modules'],
    extensions: ['.webpack.js', '.web.js', '.js', '.jsx', '.json', 'scss'],
  },
  module: {
    rules: [
      { test: /\.jsx?$/, exclude: /node_modules/, use: 'babel-loader' },
      {
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
          use: ['css-loader', 'sass-loader'], fallback: 'style-loader', publicPath: '../',
        }),
      },
      { test: /\.txt$/, use: 'raw-loader' },
      { test: /\.(png|jpg|jpeg|gif|svg|woff|woff2)([\?]?.*)$/, use: 'url-loader?limit=10000' },
      { test: /\.(eot|ttf|wav|mp3|otf)([\?]?.*)$/, use: 'file-loader' },
    ],
  },
  optimization: {
    minimize: PROD_ENV,
  },
  plugins: [
    new ExtractTextPlugin({ filename: 'css/[name].css', disable: false }),
    ...(PROD_ENV ? [
      new webpack.LoaderOptionsPlugin({
        minimize: true,
      }),
    ] : []),
  ],
};


/*
 * Webpack task
 * ~~~~~~~~~~~~
 */

/* Task to build our JS and CSS applications. */
gulp.task('build-webpack-assets', gulp.series(() => (
  gulp.src([`${jsDir}/App.js`, `${sassDir}/App.scss`])
    .pipe(named())
    .pipe(webpackStream(webpackConfig, webpack))
    .pipe(gulp.dest(buildDir))
)));


/*
 * Global tasks
 * ~~~~~~~~~~~~
 */

gulp.task('build', gulp.series(['build-webpack-assets']));


/*
 * Development tasks
 * ~~~~~~~~~~~~~~~~~
 */

gulp.task('webpack-dev-server', gulp.series(() => {
  const devWebpackConfig = Object.create(webpackConfig);
  devWebpackConfig.mode = 'development';
  devWebpackConfig.devtool = 'eval';
  devWebpackConfig.devServer = { hot: true };
  devWebpackConfig.entry = {
    App: [
      `${jsDir}/App.js`, `${sassDir}/App.scss`,
      `webpack-dev-server/client?http://localhost:${WEBPACK_DEV_SERVER_PORT}`,
      'webpack/hot/only-dev-server',
    ],
  };
  devWebpackConfig.module = {
    rules: [
      { test: /\.jsx?$/, exclude: /node_modules/, use: 'babel-loader' },
      { test: /\.scss$/, use: ['style-loader', 'css-loader', 'sass-loader'] },
      { test: /\.txt$/, use: 'raw-loader' },
      { test: /\.(png|jpg|jpeg|gif|svg|woff|woff2)([\?]?.*)$/, use: 'url-loader?limit=10000' },
      { test: /\.(eot|ttf|wav|mp3|otf)([\?]?.*)$/, use: 'file-loader' },
    ],
  };
  devWebpackConfig.output = {
    path: path.resolve(__dirname, staticDir),
    publicPath: `http://localhost:${WEBPACK_DEV_SERVER_PORT}/static/`,
    filename: 'js/[name].js',
  };
  devWebpackConfig.plugins = [
    new webpack.LoaderOptionsPlugin({ debug: true }),
    new webpack.HotModuleReplacementPlugin(),
  ];

  // Start a webpack-dev-server
  new WebpackDevServer(webpack(devWebpackConfig), {
    contentBase: path.resolve(__dirname, staticDir, '..'),
    publicPath: '/static/',
    headers: { 'Access-Control-Allow-Origin': '*' },
    hot: true,
    inline: true,
  }).listen(WEBPACK_DEV_SERVER_PORT, 'localhost', (err) => {
    if (err) throw new gutil.PluginError('webpack-dev-server', err);
    gutil.log(
      '[webpack-dev-server]',
      `http://localhost:${WEBPACK_DEV_SERVER_PORT}/webpack-dev-server/`,
    );
  });
}));
