import Vue from "vue";
import Component from "vue-class-component";
import axios from "axios";
import "../../styles/spinners.css";

@Component
export default class LoginPage extends Vue {
    username: string = "";
    password: string = "";
    errorMessage: string | null = null;
    loading: boolean = false;

    created(): void {
        console.log("Login page created!");
    }

    submit(): void {
        if (this.loading) return;
        
        var vm = this;
        this.errorMessage = null;
        this.loading = true;

        axios.post("/api/login", {
            username: this.username,
            password: this.password,
        }).then(response => {
            console.log(response);
            vm.loading = false;
        }).catch(error => {
            vm.errorMessage = error.response.data.message;
            vm.loading = false;
            console.log(error.response);
        });
    }
}
