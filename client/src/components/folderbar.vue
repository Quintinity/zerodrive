<template>
    <div class="d-flex">
        <template v-for="item in hierarchy">
            <span class="link-divider zd-use-font" :key='item.id + "div"'>/&nbsp;</span>
            <router-link :key="item.id" class="folder-link zd-bold zd-use-font mr-1" :to='"/folder/" + item.id'>{{ item.name | formatName }}</router-link>
        </template>
        <span class="link-divider zd-use-font">/&nbsp;</span>
        <router-link class="folder-link zd-bold zd-use-font mr-1" :to='"/folder/" + currentID'>{{ currentName | formatName }}</router-link>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import { HierarchyEntry } from "../types";
import { Component, Prop } from "vue-property-decorator";

@Component({
    filters: {
        formatName: (name: string): string => {
            if (name === null || name === "") {
                return "My Files";
            }
            return name;
        }
    }
})
export default class FolderBar extends Vue {
    @Prop() hierarchy!: HierarchyEntry[];
    @Prop(String) currentName!: string;
    @Prop(Number) currentID!: number;
}

</script>

<style scoped>
.folder-link {
    color: rgb(92, 92, 92);
}

.link-divider {
    color:darkgray;
}
</style>
