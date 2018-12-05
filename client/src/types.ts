/*****************************************
* Zerodrive - a cloud storage webapp     *
* INFO 3103 Term Project                 *
* by Vlad Marica (3440500)               *
* Fall 2018                              *
*****************************************/

import Vue from "vue";

export interface UserData {
    id: number;
    username: string;
    fullname: string;
    root_folder_id: number;
    storage_used: number;
    max_storage_space: number;
}

export interface HierarchyEntry {
    id: number;
    name: string;
}

export interface ItemData extends HierarchyEntry {
    size_bytes: number | null;
    type: string;
    last_modified: string;
}

export interface FolderData extends HierarchyEntry{
    parent_folder: number | null;
    last_modified: string;
    contents: ItemData[];
    hierarchy: HierarchyEntry[];
}

export interface VueRoot extends Vue {
    userData: UserData;
    loggedIn: boolean | null;

    refreshUserData(): Promise<void>;
}
