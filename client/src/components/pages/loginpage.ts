import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class LoginPage extends Vue {
    username: string = "";
    password: string = "";
    loading: boolean = false;

    created(): void {
        console.log("Login page created!");
    }

    submit(): void {
        console.log("Submit button clicked")
    }
}
