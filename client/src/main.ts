import Vue from "vue";
import VueRouter from "vue-router";
import main from "./components/main.vue";

// Import page components
import HomePage from "./components/pages/homepage.vue";
import LoginPage from "./components/pages/loginpage.vue";
import ErrorPage from "./components/pages/errorpage.vue";

import "./styles/zerodrive.css";

import "bootstrap-vue";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import "axios";

Vue.use(VueRouter);

const router = new VueRouter({
    mode: MODE === "production" ? "history" : "hash",
    routes: [
        { path: "/", component: HomePage },
        { path: "/login", component: LoginPage },
        { path: "*", component: ErrorPage, props: { statusCode: 404, statusReason: "Page not found"} }
    ]
});

new Vue({
    data: {
        text: "Hello, world!"
    },
    router: router,
    render: create => create(main),
    created: function() {
        console.log("Zerodrive running in " + MODE);
    }
}).$mount("#app");
