import Vue from "vue";

export interface UserData {
    id: number;
    username: string;
    fullname: string;
    root_folder_id: number;
    storage_used: number;
    max_storage_space: number;
}

export interface VueRoot extends Vue {
    userData: UserData;
    loggedIn: boolean | null;

    refreshUserData(): Promise<void>;
}
