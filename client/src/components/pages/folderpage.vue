<template>
    <div>
        <ErrorBanner v-if="statusCode != null" :statusCode="statusCode" :statusReason="statusReason"></ErrorBanner>
        <div v-else class="mx-auto zd-center pt-5 px-3">
            <div id="buttonbar">
                <button @click.prevent="$refs.filePickerInput.click()" class="float-right btn zd-use-font zd-bg-blue btn-primary"><i class="fa fa-file-upload mr-2 fa-button"></i>Upload File</button>
                <input ref="filePickerInput" type="file" style="display: none" @change="uploadFile">
                <button @click.prevent="$refs.newFolderModal.show()" class="float-right btn zd-use-font zd-bg-blue btn-primary mr-2"><i class="fa fa-folder-plus mr-2 fa-button"></i>Create Folder</button>
            </div>
            <FolderBar class="pt-2 pl-2" :currentID="folderData.id" :currentName="folderData.name" :hierarchy="folderData.hierarchy"></FolderBar>

            <!-- Items table -->
            <div class="table-responsive">
                <table class="table table-hover mt-2 mb-0" style="width: calc(100% - 17px)">
                    <thead>
                        <tr class="border-bottom">
                            <td width="65%" scope="col">Name</td>
                            <td width="20%" class="px-0" scope="col">Last Modified</td>
                            <td width="15%" class="px-0" scope="col">Size</td>
                        </tr>
                    </thead>
                </table>

                <div class="bodycontainer">
                    <table class="table table-hover">
                        <tbody>
                            <template v-for="item in folderData.contents">
                                <ItemRow :key="item.id" :itemData="item"></ItemRow>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>

            <p class="text-center pt-3 zd-use-font zd-bold " style="color: darkgrey; font-size: 20px" v-if="folderData.contents.length === 0">There is nothing here</p>
        </div>

        <!-- New folder modal dialog-->
        <b-modal class="zd-modal" noCloseOnBackdrop centered hide-header hide-footer no-fade ref="newFolderModal" @shown="$refs.folderNameField.focus()">
            <div>
                <span class="zd-use-font">Create New Folder</span>
                <i @click="closeModal($refs.newFolderModal)" class="fa fa-times float-right close_button"></i>
                <p :style="{visibility: errorMessage === null ? 'hidden' : 'visible'}" style="color: #ca2020; font-weight: 300" class="mt-3 zd-use-font">{{ errorMessage || "." }}</p>
                <input type="text" v-model="newFolderName" ref="folderNameField" class="form-control zd-input mt-2" placeholder="Enter folder name">
                <button type="submit" v-if="!waiting" @click.prevent="createFolder" class="float-right btn zd-use-font zd-bg-blue btn-primary mt-4">Create</button>
                <div v-else class="float-right pt-3 lds-dual-ring mr-5" style="margin-bottom: 14px; margin-right: 3.5rem !important"></div>
            </div>
        </b-modal>

        <!-- File upload modal dialog-->
        <b-modal class="zd-modal" noCloseOnBackdrop centered hide-header hide-footer no-fade ref="fileUploadModal">
            <div>
                <span class="zd-use-font">Uploading</span>
                <p :style="{visibility: errorMessage === null ? 'hidden' : 'visible'}" style="color: #ca2020; font-weight: 300" class="mt-3 zd-use-font">{{ errorMessage || "." }}</p>
                <b-progress :striped="true" ref="progressBar" :value="uploadProgress" height="25px" class="mb-3"></b-progress>
                <button :style="{visibility: errorMessage === null ? 'hidden' : 'visible'}" type="submit" @click.prevent="closeModal($refs.fileUploadModal)" class="float-right btn zd-use-font zd-bg-blue btn-primary mt-4">OK</button>
            </div>
        </b-modal>
    </div>
</template>

<script lang="ts" src="./folderpage.ts"></script>

<style scoped>
.bottom-border {
    border-bottom: 1px solid #dee2e6;
}

.fa-button {
    padding-left: 10px;
}

#buttonbar {
    width: 100%;
    height: 36px;
}

button {
    width: 170px;
    font-weight: 700;
    border-width: 0px;
    transition: background-color .15s ease-in !important;
}

button:hover {
    background-color: #5b78fa !important;
}

thead td {
    font-weight: 400;
    font-family: 'Raleway', sans-serif;
}

.close_button {
    cursor: pointer;
}

.close_button:hover {
    color: darkgray;
}

.form-control::placeholder { 
    color: #ced4da;
}

.bodycontainer {
    max-height: calc(100vh - 350px);
    width: 100%;
    margin: 0;
    overflow-y: overlay;
    padding-right: 17px;
}
</style>

<style>
tr:first-child td {
    border-top: none;
}

.modal-content {
    border: none !important;
    border-radius: 0.1rem !important;
    box-shadow: 0 4px 6px 0 hsla(0, 0%, 0%, 0.2) !important;
}

.modal-header {
    border-bottom: none !important;
}

.modal-dialog {
    max-width: 400px !important;
}

.progress-bar {
    background-color: #435cff !important;
}
</style>
