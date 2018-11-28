import Vue from "vue";
import Component from "vue-class-component";
import { Route } from 'vue-router';

@Component
export default class FolderPage extends Vue {
    beforeRouteEnter(to: Route, from: Route, next: Function): void {
        next();
    }

    created(): void {
        console.log("Folder page created");
    }
}
