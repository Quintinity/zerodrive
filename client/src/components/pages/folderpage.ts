import Vue from "vue";
import Component from "vue-class-component";
import { Route } from 'vue-router';
import FolderBar from "../folderbar.vue";

@Component({components: { FolderBar }})
export default class FolderPage extends Vue {
    items = [

    ];

    beforeRouteEnter(to: Route, from: Route, next: Function): void {
        next();
    }

    created(): void {
        console.log("Folder page created");
    }
}
