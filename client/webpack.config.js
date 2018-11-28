const path = require("path")
const webpack = require("webpack")
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;
const HtmlWebpackPlugin = require("html-webpack-plugin");
const VueLoaderPlugin = require("vue-loader/lib/plugin");
const HtmlBeautifyPlugin = require("html-beautify-webpack-plugin");
const CompressionPlugin = require("compression-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const CleanWebpackPlugin = require("clean-webpack-plugin");

const mode = process.env.NODE_ENV;
if (mode === undefined) {
    throw Error("NODE_ENV is not set!");
}

const baseURL = process.env.ZERODRIVE_SERVER_BASE_URL || "/";

const config = {
    mode: mode,
    entry: "./src/main.ts",
    output: {
        path: path.resolve(__dirname, "dist"),
        publicPath: baseURL + "static/",
        filename: "bundle.js"
    },
    plugins: [
        /*new BundleAnalyzerPlugin({
            analyzerMode: "disabled",
            generateStatsFile: true,
            statsOptions: { source: false }
        }),*/
        new CleanWebpackPlugin(["./dist"]),
        new HtmlWebpackPlugin({ template: "./src/index.html" }),
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
        new MiniCssExtractPlugin({ filename: "style.css" }),
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
                test: /\.(png|jpg|gif|svg|ico)$/,
                loader: "file-loader",
                options: {
                    name: "[name].[ext]"
                }
            },
            {
                test: /\.css$/, 
                use: [
                    mode === "production" ? MiniCssExtractPlugin.loader : "vue-style-loader", 
                    "css-loader"
                ]
            }
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
    if (mode === "development") {
        config.devtool = "eval-source-map";
    }
    else if (mode === "production") {
        config.devtool = "source-map";
    }

    config.plugins.push(new webpack.DefinePlugin({
        "MODE": JSON.stringify(config.mode),
        "BASE_PATH": JSON.stringify(basePath)
    }));

    return config;
};
