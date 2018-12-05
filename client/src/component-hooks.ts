/*****************************************
* Zerodrive - a cloud storage webapp     *
* INFO 3103 Term Project                 *
* by Vlad Marica (3440500)               *
* Fall 2018                              *
*****************************************/

// Registers method hooks for Vue class components. As per the documentation,
// it must go in a separate file.
import Component from "vue-class-component";
Component.registerHooks(["beforeRouteEnter", "beforeRouteUpdate"]);
