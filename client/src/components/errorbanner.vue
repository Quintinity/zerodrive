<template>
    <div class="mx-auto zd-center px-5 pt-5">
        <p class="zd-use-font zd-bold zd-fg-blue zd-banner-text" style="color: black">{{ statusCode }} - {{ statusReason}}</p>
        <router-link class="btn btn-md ml-auto btn-outline-dark mt-5 zd-use-font" to="/">Go to Home</router-link>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Component, Prop } from "vue-property-decorator";

@Component
export default class ErrorBanner extends Vue {
    @Prop(String) statusCode!: string;
    @Prop({type: String, default: "Something went wrong"}) statusReason!: string;
}
</script>

<style scoped></style>
