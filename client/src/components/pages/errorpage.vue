<template>
    <ErrorBanner :statusCode="statusCode" :statusReason="statusReason"></ErrorBanner>
</template>

<script lang="ts">
import Vue from "vue";
import { Component, Prop } from "vue-property-decorator";
import ErrorBanner from "../errorbanner.vue";

@Component({ components: { ErrorBanner } })
export default class ErrorPage extends Vue {
    @Prop(String) statusCode!: string;
    @Prop({type: String, default: "Something went wrong"}) statusReason!: string;
}
</script>

<style></style>
