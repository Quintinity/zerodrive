<template>
    <nav class="navbar navbar-expand-md navbar-dark zd-bg-blue">
        <div class="d-flex zd-center mx-auto">
            <i class="fas fa-cloud zd-icon d-flex align-items-center justify-content-center" style="color: white"></i>
            <router-link class="navbar-brand zd-bold mr-auto zd-use-font" to="/">Zerodrive</router-link>


            <div id="user-info-display" v-show="$root.loggedIn" class="ml-auto mr-3 text-center" style="height: 32px; padding-top: 2px">
                <p class="zd-use-font zd-bold mb-0" style="color: white">{{ $root.userData.username }}@unb.ca</p>
                <b-progress id="data-bar" class="data-bar" height="6px" :value="100 * $root.userData.storage_used / $root.userData.max_storage_space"></b-progress>
            </div>
            <b-popover target="user-info-display" placement="bottom" triggers="hover focus">
                {{ popoverText }}
            </b-popover>
            <router-link class="btn ml-auto btn-outline-light zd-use-font zd-bold" to="/login" v-if="this.$route.path !== '/login' && !$root.loggedIn">Log in</router-link>
            <button v-on:click="logout" class="btn btn-outline-light zd-use-font zd-bold" v-if="$root.loggedIn">Log out</button>
        </div>
    </nav>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import { VueRoot } from "../types";
import axios from "axios";
import * as bytes from "bytes";

@Component
export default class TopBar extends Vue {
    popoverText: string = "";

    async logout() {
        const root = this.$root as VueRoot;
        await axios.delete("/api/login");
        root.loggedIn = false;
        this.$router.replace("/");
    }

    created(): void {
        this.$root.$on("userdataUpdated", () => {
            this.computePopoverText();
        });
        this.computePopoverText();
    }

    computePopoverText(): void {
        this.popoverText = bytes.format((this.$root as VueRoot).userData.storage_used, { unitSeparator: " " }) + " / " + bytes.format((this.$root as VueRoot).userData.max_storage_space, { unitSeparator: " " });
    }
}
</script>

<style>
.data-bar .progress-bar {
    background-color: #d39e00 !important;
}
</style>
