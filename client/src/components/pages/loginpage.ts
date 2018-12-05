/*****************************************
* Zerodrive - a cloud storage webapp     *
* INFO 3103 Term Project                 *
* by Vlad Marica (3440500)               *
* Fall 2018                              *
*****************************************/

import Vue from "vue";
import { Route } from "vue-router";
import Component from "vue-class-component";
import axios from "axios";

import { VueRoot } from "../../types";
import "../../styles/spinners.css";

@Component
export default class LoginPage extends Vue {
    username: string = "";
    password: string = "";
    errorMessage: string | null = null;
    loading: boolean = false;

    beforeRouteEnter(from: Route, to: Route, next: Function): void {
        next((vm: LoginPage) => {
            if ((vm.$root as VueRoot).loggedIn) {
                next({ path: "/" });
            }
        });
    }

    async submit() {
        if (this.loading) return;
        
        const vm = this;
        this.errorMessage = null;
        this.loading = true;

        axios.post("/api/login", {
            username: this.username,
            password: this.password,
        }).then(async response => {
            const root = vm.$root as VueRoot;
            await root.refreshUserData();

            if (response.status === 200) {
                this.$router.replace("/");
            }
        }).catch(error => {
            vm.errorMessage = error.response.data.message;
            vm.loading = false;
        });
    }
}
