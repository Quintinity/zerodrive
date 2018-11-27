import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class LoginPage extends Vue {
    created(): void {
        console.log("Login page created!");
    }
}
