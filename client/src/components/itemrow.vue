<template>
    <tr @contextmenu.prevent @click="onClick" style="width: calc(100% - 17px)" :class='{"cursor-pointer": itemData.type === "Folder"}'>
        <td width="65%">
            <i v-if="itemData.type === 'Folder'" class="fa fa-folder item-icon"></i>
            <i v-else class="fa fa-file item-icon"></i>
            {{ itemData.name }}
        </td>
        <td width="20%" scope="col" class="px-0">{{ itemData.last_modified }}</td>
        <td width="15%" scope="col" class="px-0">{{ formatSize }}</td>
    </tr>
</template>

<script lang="ts">
import Vue from "vue";
import { Component, Prop } from "vue-property-decorator";
import { ItemData } from "../types";
import bytes from "bytes";

@Component
export default class ItemRow extends Vue {
    @Prop() itemData!: ItemData;

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
</style>

