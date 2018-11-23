const router = new VueRouter({
    mode: "history",
    routes: [
        { path: "/", component: { template: "#homepage-template" } },
        { path: "/login", component: { template: "#login-template" } },
        { path: "*", component: { template: "#page-404-template" } }
    ]
});

const app = new Vue({
    el: "#app",
    router: router
});
