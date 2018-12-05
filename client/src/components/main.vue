<template>
    <div id="zd-body-wrapper" @click="onGlobalClick" v-if="$root.loggedIn != null" style="height:100%">
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
export default class Main extends Vue {
    onGlobalClick(event: MouseEvent): void {
        this.$root.$emit("onGlobalClick", event); // emit click event so other components can listen to it
    }
}
</script>

<style scoped>
.zd-body-wrapper {
    height: 100%;
}
</style>
