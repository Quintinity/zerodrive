import Vue from "vue";
Vue.config.devtools = true;

import VueRouter, { Route } from "vue-router";
import "./component-hooks";

import main from "./components/main.vue";
import { UserData, VueRoot } from "./types";

// Import page components
import HomePage from "./components/pages/homepage.vue";
import LoginPage from "./components/pages/loginpage.vue";
import ErrorPage from "./components/pages/errorpage.vue";
import FolderPage from "./components/pages/folderpage.vue";

import "./styles/zerodrive.css";
import "./images/favicon.ico";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

const components = require("bootstrap-vue/es/components/");
Vue.use(components.Modal);
Vue.use(components.Progress);

import axios from "axios";

Vue.use(VueRouter);

console.log("Using base URL: " + BASE_PATH);
axios.defaults.baseURL = BASE_PATH;

const router = new VueRouter({
    mode: MODE === "production" ? "history" : "hash",
    base: BASE_PATH,
    routes: [
        { path: "/", component: HomePage },
        { path: "/login", name: "login", component: LoginPage },
        { path: "/folder/:folder_id", name: "folder", component: FolderPage},
        { path: "*", component: ErrorPage, props: { statusCode: "404", statusReason: "Page not found"} },
    ]
});

const root = new Vue({
    data: {
        userData: {
            id: 0,
            username: "",
            root_folder_id: -1,
            storage_used: 0,
            max_storage_space: 0
        } as UserData,
        loggedIn: null as boolean | null // this value is null if we don't know if the user is logged in
    },
    methods: {
        refreshUserData: async function(): Promise<void> {
            return new Promise<void>((resolve, reject) => {
                axios.get("/api/user")
                    .then(response => {
                        console.log(response);
                        this.userData = response.data as UserData;
                        this.loggedIn = true;
                    })
                    .catch(error => {
                        this.loggedIn = false;
                    })
                    .then(() => {
                        resolve();
                    });
            });
        }
    },
    created: async function() {
        await this.refreshUserData();
    },
    router: router,
    render: create => {
        return create(main);
    }
});

root.$mount("#app");