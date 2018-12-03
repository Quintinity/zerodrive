<template>
    <tr @contextmenu.prevent="$emit('onRightClick', itemData, $event)" @click="onClick" style="width: calc(100% - 17px)" :class='{"tr-selected": selected, "cursor-pointer": itemData.type === "Folder"}'>
        <td :class='{"td-selected": selected}' width="65%" class="zd-use-font">
            <i v-if="itemData.type === 'Folder'" class="fa fa-folder item-icon"></i>
            <i v-else class="fa fa-file item-icon"></i>
            {{ itemData.name }}
        </td>
        <td :class='{"td-selected": selected}' width="20%" scope="col" class="zd-use-font px-0">{{ itemData.last_modified }}</td>
        <td :class='{"td-selected": selected}' width="15%" scope="col" class="zd-use-font px-0">{{ formatSize }}</td>
    </tr>
</template>

<script lang="ts">
import Vue from "vue";
import { Component, Prop } from "vue-property-decorator";
import { ItemData } from "../types";
import * as bytes from "bytes";

@Component
export default class ItemRow extends Vue {
    @Prop() itemData!: ItemData;
    @Prop(Boolean) selected!: boolean;

    get formatSize(): string {
        return this.itemData.size_bytes === null ? "--" : bytes.format(this.itemData.size_bytes, { unitSeparator: " " });
    }

    onClick(): void {
        if (this.itemData.type === "Folder") {
            this.$router.push("/folder/" + this.itemData.id);
        }
    }
}
</script>

<style scoped>
td {
    color: #6c757d;
    font-weight: 300;
    font-family: 'Raleway', sans-serif;
}

.item-icon {
    padding-right: 5px;
    font-size: 20px;
}

.cursor-pointer {
    cursor: pointer;
}

.tr-selected {
    background-color: darkgray !important;
}

.td-selected {
    color: white !important;
}
</style>

