<template>
    <nav class="navbar navbar-expand-md navbar-dark zd-bg-blue">
        <div class="d-flex zd-center mx-auto">
            <i class="fas fa-cloud zd-icon d-flex align-items-center justify-content-center" style="color: white"></i>
            <router-link class="navbar-brand zd-bold mr-auto zd-use-font" to="/">Zerodrive</router-link>
            <router-link class="btn ml-auto btn-outline-light zd-use-font" to="/login" v-if="this.$route.path !== '/login'">Log in</router-link>
        </div>
    </nav>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    
});
</script>

<style>
</style>
