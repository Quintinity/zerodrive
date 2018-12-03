<template>
    <div @contextmenu.prevent class="context-menu" :style='{"left": x + "px", "top": y + "px"}'>
        <div @click.prevent="$emit('buttonClicked', 'download')" v-if="itemData.type === 'File'" class="ctx-button px-3 pt-1 pb-1 zd-use-font zd-bold"><i class="fa fa-file-download mr-2"></i>&nbsp;Download</div>
        <div @click.prevent="$emit('buttonClicked', 'rename')" class="ctx-button px-3 pt-1 pb-1 zd-use-font zd-bold"><i class="fa fa-pencil-alt mr-2"></i>Rename</div>
        <div @click.prevent="$emit('buttonClicked', 'delete')" class="ctx-button px-3 pt-1 pb-1 zd-use-font zd-bold"><i class="fa fa-trash-alt mr-2"></i>&nbsp;Delete</div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ItemData } from "../types";
import { Component, Prop } from "vue-property-decorator";

@Component
export default class ContextMenu extends Vue {
    @Prop(Number) x!: number;
    @Prop(Number) y!: number;
    @Prop() itemData!: ItemData;
}
</script>

<style scoped>
.context-menu {
    position: absolute;
    display: block;
    width: 200px;
    box-shadow: 0 0 15px 2px hsla(0, 0%, 0%, 0.2);
    background-color: white;
    border-radius: 3px;
}

.ctx-button {
    width: 100%;
    cursor: pointer;
    color: #6c757d;
}

.ctx-button:hover {
    background-color: rgba(0, 0, 0, 0.075);
}
</style>
