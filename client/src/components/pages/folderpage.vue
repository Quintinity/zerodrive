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
                <td class="" scope="col">Name</td>
                <td class="text-right" scope="col">Last Modified</td>
                <td class="text-right" scope="col">Size</td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><i class="fa fa-folder item-icon"></i>Folder 1</td>
                <td class="text-right">Yesterday</td>
                <td class="text-right">--</td>
            </tr>
            <tr>
                <td><i class="fa fa-file-archive item-icon"></i>Assignment5.zip</td>
                <td class="text-right">Wednesday</td>
                <td class="text-right">164 KB</td>
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

.item-icon {
    padding-right: 5px;
    font-size: 20px;
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

tbody td {
    color: #6c757d;
    font-weight: 300;
    font-family: 'Raleway', sans-serif;
}

thead td {
    font-weight: 400;
    font-family: 'Raleway', sans-serif;
}
</style>
