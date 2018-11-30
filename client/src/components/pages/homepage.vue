<template>
    <div>
        <!-- Hero banner -->
        <div class="zd-hero-banner zd-bg-blue">
            <div class="mx-auto zd-center px-5 pt-5">
                <p class="zd-use-font zd-bold zd-banner-text">
                    Free cloud storage for all of your files
                </p>
                <div v-if="$root.loggedIn">
                    <p id="usernameLabel" class="zd-use-font zd-bold pt-2">Hi {{ $root.userData.fullname }},</p>
                    <router-link class="btn btn-lg ml-auto btn-outline-light mt-1 zd-use-font" v-bind:to="'/folder/' + $root.userData.root_folder_id">View your files</router-link>
                </div>
                <router-link v-else class="btn btn-lg ml-auto btn-outline-light mt-5 zd-use-font" to="/login">Log in with your UNB account</router-link>
            </div>
        </div>

        <div class="mx-auto zd-center pt-3">
            <div class="row pt-5">
                <div class="col align-items-center d-flex flex-column">
                    <i class="fas fa-lock zd-fg-blue zd-icon mb-3" style="font-size: 80px"></i>
                    <p class="zd-use-font zd-bold zd-header text-center mb-0">Pretty Secure</p>
                    <p class="text-muted text-center">Your files are probably safe</p>
                </div>
                <div class="col align-items-center d-flex flex-column">
                    <i class="fas fa-hdd zd-fg-blue zd-icon mb-3" style="font-size: 80px"></i>
                    <p class="zd-use-font zd-bold zd-header text-center mb-0">Unlimited Storage</p>
                    <p class="text-muted text-center">Up to 100MB per account</p>
                </div>
                <div class="col align-items-center d-flex flex-column">
                    <i class="fas fa-bolt zd-fg-blue zd-icon mb-3" style="font-size: 80px"></i>
                    <p class="zd-use-font zd-bold zd-header text-center mb-0">Lightning Fast</p>
                    <p class="text-muted text-center">As long as no one else is using it</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class HomePage extends Vue {}
</script>

<style scope>
#usernameLabel {
    color: white;
    font-size: 30px;
    margin-bottom: 0;
}
</style>
