<template>
   <div class="mx-auto zd-center px-5 pt-5 align-center">
        <p class="zd-use-font zd-bold zd-fg-blue text-center" style="font-size: 30px; color: #383d41">Log in to Zerodrive</p>
        
        <div class="mx-auto mb-5 bg-white rounded text-center" style="width: 400px; height: 340px; box-shadow: 0 4px 6px 0 hsla(0, 0%, 0%, 0.2)">
            <form class="zd-use-font mx-auto pt-3" style="width: 90%; text-align: left">
                <div class="form-group">
                    <label class="zd-bold" for="inputUsername" style="color: #383d41">UNB Username</label>
                    <input type="text" v-model="username" class="form-control zd-input" id="inputUsername" aria-describedby="emailHelp" placeholder="Enter username">
                    <small id="emailHelp" class="form-text text-muted">This is your UNB computer science username and password.</small>
                </div>
                
                <div class="form-group">
                    <label class="zd-bold" for="inputPassword" style="color: #383d41">Password</label>
                    <input type="password" v-model="password" class="form-control zd-input" id="inputPassword" placeholder="Enter password">
                </div>
                
                <span class="align-center" v-bind:style="{visibility: errorMessage == null ? 'hidden' : 'visible'}" id="errorMessage">{{ errorMessage || "placeholder" }}</span>
                <div v-if="loading" class="d-flex mb-3 mt-3" style="width: 100%">
                    <div class="mx-auto lds-dual-ring"></div>
                </div>
                <button v-else v-on:click.prevent="submit" class="btn zd-use-font zd-bg-blue mb-3 mt-3 btn-lg btn-primary" style="width: 100%">Submit</button>
            </form>
        </div>
    </div> 
</template>

<script lang="ts" src="./loginpage.ts"></script>

<style scoped>
button {
    font-weight: 700;
    border-width: 0px;
    transition: background-color .15s ease-in !important;
}

button:hover {
    background-color: #5163d8 !important;
}

.form-control::placeholder { 
    color: #ced4da;
}

#errorMessage {
    color: #ca2020;
}
</style>
