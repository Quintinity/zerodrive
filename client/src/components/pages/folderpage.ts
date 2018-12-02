import Vue, from "vue";
import Component from "vue-class-component";
import { Route } from 'vue-router';
import { FolderData, ItemData, HierarchyEntry } from "../../types";
import FolderBar from "../folderbar.vue";
import ErrorBanner from "../errorbanner.vue";
import ItemRow from "../itemrow.vue";
import axios, { AxiosError } from "axios";
import { sleep } from "../../util";

@Component({components: { FolderBar, ErrorBanner, ItemRow }})
export default class FolderPage extends Vue {
    folderData: FolderData = {
        parent_folder: 0,
        contents: [],
        hierarchy: [],
        last_modified: "",
        name: "",
        id: 0
    };

    errorMessage: string | null = null;
    statusCode: string | null = null;
    statusReason: string = "An error has occurred";

    waiting = false;
    newFolderName: string = "";
    uploadProgress = 50;

    fileSelected(event: any): void {
        console.log(event);
    }

    async createFolder() {
        this.waiting = true;
        const vm = this;

        await sleep(600);
        axios.post("/api/folder", {
            name: this.newFolderName,
            parent_folder_id: this.folderData.id
        })
        .then(async response => {
            await vm.loadFolderData("" + vm.folderData.id);
            vm.closeModal(vm.$refs.newFolderModal);
            vm.newFolderName = "";

        })
        .catch(error => {
            console.log(error);
            vm.errorMessage = error.response.data.message;
            vm.$refs.folderNameField.focus();
        })
        .then(() => {
            vm.waiting = false;
        });
    }

    closeModal(modal: any): void {
        modal.hide();
        this.waiting = false;
        this.errorMessage = null;
    }

    async loadFolderData(folder_id: string): Promise<void> {
        const vm = this;
        return new Promise<void>((resolve, reject) => {
            axios.get("/api/folder/" + folder_id)
                .then(response => {
                    vm.folderData = response.data as FolderData;
                    vm.statusCode = null;
                })
                .catch((error: AxiosError) => {
                    if (error.response === undefined)
                        console.log(error);
                    else {
                        vm.statusCode = "" + error.response.status;
                        if (error.response.status === 404)
                            vm.statusReason = "File not found";
                        else if (error.response.status == 401)
                            vm.statusReason = "Unauthorized";
                        else
                            vm.statusReason = "An error has occurred";
                    }
                })
                .then(() => {
                    resolve();
                });
        });
    }

    async beforeRouteEnter(to: Route, from: Route, next: Function): Promise<void> {
        return new Promise<void>((resolve, reject)  => {
            next(async (vm : FolderPage) => {
                await vm.loadFolderData(to.params["folder_id"]);
                resolve();
            });
        });
    }

    async beforeRouteUpdate(to:Route, from: Route, next: Function): Promise<void> {
        await this.loadFolderData(to.params["folder_id"]);
        next();
    }
}
