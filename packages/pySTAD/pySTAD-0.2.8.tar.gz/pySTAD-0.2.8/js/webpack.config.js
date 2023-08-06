const path = require('path');
const version = require('./package.json').version;

const rules = [
    {
        test: /\.svelte$/,
        loader: 'svelte-loader'
    },
    { test: /\.worker\.(c|m)?js$/i, use: [
        {
          loader: 'worker-loader',
          options: {
            filename: '[name].worker.js',
            inline: 'fallback'
          },
        }
      ],
  },
    { test: /\.ts$/, loader: 'ts-loader' },
    { test: /\.js$/, use: {
        loader: 'source-map-loader',
        options: {
          filterSourceMappingUrl: (url, resourcePath) => {
            return !(/.*\/node_modules\/.*/.test(resourcePath))
          }
        }
      }
    },
    { test: /\.css$/, use: ['style-loader', 'css-loader']},
    { test: /\.(jpg|png)$/, loader: 'url-loader' }
];
const externals = ['@jupyter-widgets/base'];
const resolve = {
    alias: {
        svelte: path.resolve('node_modules', 'svelte')
    },
    extensions: ['.webpack.js', '.web.js', '.mjs', '.ts', '.js', '.svelte'],
    mainFields: ['svelte', 'browser', 'module', 'main'],
};
  
module.exports = (env, argv) => {
    var devtool = argv.mode === 'development' ? 'source-map' : false;
    return [
        { // Jupyter lab bundle
            mode: argv.mode,
            entry: {
                plugin: './src/plugin.ts',
                index: './src/index.ts'
            },
            output: {
                filename: '[name].js',
                path: path.resolve(__dirname, 'lib'),
                libraryTarget: 'amd',
                publicPath: '',
            },
            module: {
                rules: rules,
            },
            devtool: devtool,
            externals,
            resolve,
        }, { // Jupyter notebook bundle
          entry: './src/extension.ts',
          output: {
            filename: 'index.js',
            path: path.resolve(__dirname, '..', 'stad', 'widget', 'nbextension'),
            libraryTarget: 'amd',
            publicPath: '',
          },
          module: {
            rules: rules
          },
          devtool: devtool,
          externals,
          resolve,
        }, { // Embeddable Jupyter notebook bundle
          entry: './src/index.ts',
          output: {
              filename: 'index.js',
              path: path.resolve(__dirname, 'dist'),
              libraryTarget: 'amd',
              library: "jupyter_stad",
              publicPath: 'https://unpkg.com/jupyter_stad@' + version + '/dist/'
          },
          devtool: devtool,
          module: {
              rules: rules
          },
          externals,
          resolve,
        },
    ];
}
