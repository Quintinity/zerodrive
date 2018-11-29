<template>
    <div v-if="$root.loggedIn != null">
        <topbar></topbar>
        <router-view></router-view>
        <bottombar></bottombar>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

import topbar from "./topbar.vue";
import bottombar from "./bottombar.vue";

@Component({components: { topbar, bottombar }})
export default class Main extends Vue {}
</script>

<style>
body {
    background-color: #fbfbfb !important;
}
</style>
