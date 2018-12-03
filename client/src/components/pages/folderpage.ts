import Vue from "vue";
import Component from "vue-class-component";
import { Route } from 'vue-router';
import { FolderData, ItemData, HierarchyEntry } from "../../types";

import FolderBar from "../folderbar.vue";
import ErrorBanner from "../errorbanner.vue";
import ContextMenu from "../contextmenu.vue";
import ItemRow from "../itemrow.vue";

import axios, { AxiosError } from "axios";
import { sleep } from "../../util";
import { Modal, Progress } from "bootstrap-vue";

import * as download from "downloadjs";

@Component({components: { FolderBar, ErrorBanner, ItemRow, ContextMenu }})
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
    uploadProgress = 0;

    selectedItem: ItemData | null = null;
    contextMenuX = 0;
    contextMenuY = 0;

    showContextMenu(data: ItemData, event: MouseEvent): void {
        this.contextMenuX = event.pageX;
        this.contextMenuY = event.pageY;
        this.selectedItem = data;
    }

    async onContextMenuClick(button: string): Promise<void> {
        console.log(button);
        if (button === "delete") {
            await this.deleteItem();
        }
        else if (button === "download") {
            await this.downloadFile();
        }
        await this.loadFolderData(this.folderData.id.toString());
        this.selectedItem = null;
    }

    async deleteItem(): Promise<void> {
        const type = this.selectedItem!.type.toLowerCase();
        const itemID = this.selectedItem!.id;

        return new Promise<void>((resolve, reject) => {
            axios.delete("/api/" + type + "/" + itemID)
                .then(response => {})
                .catch(error => {})
                .then(() => resolve());
        });
    }

    async downloadFile(): Promise<void> {
        const fileID = this.selectedItem!.id;
        const filename = this.selectedItem!.name;

        return new Promise<void>((resolve, reject) => {
            axios.get("/api/file/" + fileID)
                .then(response => {
                    console.log(response);
                    download(response.data, filename, response.headers["content-type"])
                })
                .catch(error => {})
                .then(() => { 
                    console.log("here");
                    resolve()
                });
        });
    }

    async uploadFile(event: Event): Promise<void> {
        let data = new FormData();
        let inputElement = event.target as HTMLInputElement;
        let fileList = inputElement.files!;
        console.log(fileList);

        let formData = new FormData();
        formData.append("parent_folder", this.folderData.id.toString());
        formData.append("file", fileList[0]);
        
        (inputElement.form as HTMLFormElement).reset();

        const vm = this;
        const requestConfig = {
            onUploadProgress: (event: ProgressEvent) => {
                vm.uploadProgress = Math.floor(100 * (event.loaded / event.total));
            }
        };

        (this.$refs.fileUploadModal as Modal).show();
        this.uploadProgress = 0;
        await sleep(100);

        return new Promise<void>((resolve, reject) => {
            axios.post("/api/file", formData, requestConfig)
                .then(async response => {
                    console.log(response);
                    await sleep(1000);
                    await vm.loadFolderData(vm.folderData.id.toString());
                    this.closeModal(this.$refs.fileUploadModal);
                })
                .catch(async error => {
                    await sleep(500);
                    this.errorMessage = error.response.data.message;
                })
                .then(() => resolve());
        }); 
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
            (vm.$refs.folderNameField as HTMLInputElement).focus();
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
                vm.selectedItem = null;
                await vm.loadFolderData(to.params["folder_id"]);
                resolve();
            });
        });
    }

    async beforeRouteUpdate(to:Route, from: Route, next: Function): Promise<void> {
        this.selectedItem = null;
        await this.loadFolderData(to.params["folder_id"]);
        next();
    }

    created(): void {
        let vm = this;
        this.$root.$on("onGlobalClick", (event: MouseEvent) => {
            if (!(event.target as Element).classList.contains("ctx-button")) {
                vm.selectedItem = null;
            }
        });
    }
}
