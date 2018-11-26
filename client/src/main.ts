import Vue from "vue";
import main from "./components/main.vue";
import "./styles/zerodrive.css";
import "bootstrap-vue";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import VueRouter from "vue-router";

Vue.use(VueRouter);

const router = new VueRouter({
    mode: "history",
    routes: [
        { path: "/", component: { template: "#homepage-template" } },
        { path: "/login", component: { template: "#login-template" } },
        { path: "*", component: { template: "#page-404-template" } }
    ]
});

new Vue({
    data: {
        text: "Hello, world!"
    },
    router: router,
    render: create => create(main),
    created: function() {
        console.log("Hello from Vue + Typescript!");
    }
}).$mount("#app");
