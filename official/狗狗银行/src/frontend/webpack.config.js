const HTMLWebpackPlugin = require('html-webpack-plugin');

const babel_loader = {
  loader: 'babel-loader',
  options: {
    presets: [
      ['@babel/preset-env', {
        targets: 'defaults',
        bugfixes: true,
        useBuiltIns: 'usage',
        corejs: 3,
      }],
      '@babel/preset-react',
    ],
    plugins: [
      ['import', {
        libraryName: 'antd',
        libraryDirectory: 'es',
        style: true,
      }],
    ],
  },
};

const file_loader = {
  loader: 'file-loader',
  options: {
    name: '[name].[ext]',
  },
};

// https://github.com/ant-design/ant-motion/issues/44#issuecomment-620033459
const less_loader = {
  loader: 'less-loader',
  options: {
    lessOptions: {
      javascriptEnabled: true,
    },
  },
};

module.exports = {
  entry: './src',
  output: { filename: '[name].js' },
  devServer: {
    contentBase: 'src',
  },
  watchOptions: {
    ignored: /node_modules/,
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: [babel_loader],
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.less$/,
        use: ['style-loader', 'css-loader', less_loader],
      },
      {
        test: /\.(gif|jpg|png|svg)$/,
        use: [file_loader],
      },
    ],
  },
  plugins: [
    new HTMLWebpackPlugin({
      template: 'src/index.html',
    }),
  ],
};
