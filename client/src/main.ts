import Vue from "vue";
Vue.config.devtools = true;

import VueRouter from "vue-router";
import "./component-hooks";

import main from "./components/main.vue";

// Import page components
import HomePage from "./components/pages/homepage.vue";
import LoginPage from "./components/pages/loginpage.vue";
import ErrorPage from "./components/pages/errorpage.vue";
import FolderPage from "./components/pages/folderpage.vue";

import "./styles/zerodrive.css";
import "./images/favicon.ico";

import "bootstrap-vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import axios from "axios";

Vue.use(VueRouter);

const router = new VueRouter({
    mode: MODE === "production" ? "history" : "hash",
    base: BASE_PATH,
    routes: [
        { path: "/", component: HomePage },
        { path: "/login", component: LoginPage },
        { path: "/folder/:folder_id", name: "folder", component: FolderPage},
        { path: "*", component: ErrorPage, props: { statusCode: 404, statusReason: "Page not found"} }
    ]
});

interface UserData {
    username: string;
}

new Vue({
    data: {
        userData: {
            username: "vmarica"
        } as UserData,
        loggedIn: false
    },
    methods: {
        refreshUserData: function() {
            axios.get("/api/user")
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    this.loggedIn = false;
                });
        }
    },
    created: function() {
        this.refreshUserData();
    },
    router: router,
    render: create => create(main)
}).$mount("#app");
