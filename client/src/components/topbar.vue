<template>
    <nav class="navbar navbar-expand-md navbar-dark zd-bg-blue">
        <div class="d-flex zd-center mx-auto">
            <i class="fas fa-cloud zd-icon d-flex align-items-center justify-content-center" style="color: white"></i>
            <router-link class="navbar-brand zd-bold mr-auto zd-use-font" to="/">Zerodrive</router-link>
            <router-link class="btn ml-auto btn-outline-light zd-use-font zd-bold" to="/login" v-if="this.$route.path !== '/login' && !$root.loggedIn">Log in</router-link>
            <button v-on:click="logout" class="btn ml-auto btn-outline-light zd-use-font zd-bold" v-if="$root.loggedIn">Log out</button>
        </div>
    </nav>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import { VueRoot } from "../types";
import axios from "axios";

@Component
export default class TopBar extends Vue {
    async logout() {
        const root = this.$root as VueRoot;
        await axios.delete("/api/login");
        root.loggedIn = false;
        this.$router.replace("/");
    }
}
</script>

<style>
</style>
