<template>
    <div class="mx-auto zd-center pt-5 px-3">
        <div id="buttonbar">
            <button v-on:click.prevent="submit" class="float-right btn zd-use-font zd-bg-blue btn-primary"><i class="fa fa-file-upload mr-2 fa-button"></i>Upload File</button>
            <button v-on:click.prevent="submit" class="float-right btn zd-use-font zd-bg-blue btn-primary mr-2"><i class="fa fa-folder-plus mr-2 fa-button"></i>Create Folder</button>
        </div>
        <router-link class="zd-bold zd-use-font" to="/">My Files</router-link>

        <table class="table table-hover mt-3">
        <thead>
            <tr>
                <td class="zd-use-font" scope="col">Name</td>
                <td class="zd-use-font text-right" scope="col">Last Modified</td>
                <td class="zd-use-font text-right" scope="col">Size</td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><i class="fa fa-folder"></i>Mark</td>
                <td>Otto</td>
                <td>@mdo</td>
            </tr>
            <tr>
                <td>Jacob</td>
                <td>Thornton</td>
                <td>@fat</td>
            </tr>
            <tr>
                <td>Larry</td>
                <td>the Bird</td>
                <td>@twitter</td>
            </tr>
        </tbody>
        </table>
    </div>
</template>

<script lang="ts" src="./folderpage.ts"></script>

<style scoped>
thead tr:first-child td{
    border-top: none;
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
    background-color: #4d6cf5 !important;
}

td {
    color: #6c757d;
}
</style>
