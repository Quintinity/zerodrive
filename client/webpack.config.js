const path = require("path")
const webpack = require("webpack")
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;
const HtmlWebpackPlugin = require("html-webpack-plugin");
const VueLoaderPlugin = require("vue-loader/lib/plugin");
const HtmlBeautifyPlugin = require("html-beautify-webpack-plugin");
const CompressionPlugin = require('compression-webpack-plugin');

const config = {
    mode: "development",
    entry: "./src/main.ts",
    output: {
        path: path.resolve(__dirname, "dist"),
        publicPath: "/dist/",
        filename: "bundle.js"
    },
    plugins: [
        new BundleAnalyzerPlugin({
            analyzerMode: "disabled",
            generateStatsFile: true,
            statsOptions: { source: false }
        }),
        new HtmlWebpackPlugin({
            template: "./src/index.html"
        }),
        new HtmlBeautifyPlugin({
            config: {
                html: {
                    extra_liners: [],
                    indent_inner_html: true,
                    indent_with_tabs: true
                }
            }
        }),
        new VueLoaderPlugin(),
        new CompressionPlugin({
            filename: "[path].gz[query]",
            algorithm: "gzip",
            test: /\.js$|\.css$/,
        })
    ],
    module: {
        rules: [
            { test: /\.vue$/, loader: "vue-loader" },
            {
                test: /\.tsx?$/,
                loader: "ts-loader",
                exclude: /node_modules/,
                options: {
                    appendTsSuffixTo: [/\.vue$/],
                }
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: "file-loader",
                options: {
                    name: "[name].[ext]?[hash]"
                }
            },
            { test: /\.css$/, use: ["vue-style-loader", "css-loader"] }
        ]
    },
    resolve: {
        extensions: [".ts", ".js", ".vue", ".json"],
        alias: {
            "vue$": "vue/dist/vue.esm.js"
        }
    },
    devServer: {
        contentBase: path.join(__dirname, "dist"),
        port: 9000
    },
    performance: {
        hints: false
    },
};

module.exports = (env, argv) => {
    if (argv.mode === "development") {
        config.devtool = "eval-source-map";
    }
    else if (argv.mode === "production") {
        config.devtool = "source-map";
    }
    return config;
};
