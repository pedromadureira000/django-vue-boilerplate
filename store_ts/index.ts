import { RootState } from "@/store/types";

export const state = ():RootState  => ({
    drawer: false,
    menuItems: [
      { title: "Home", icon: "mdi-home", to: "/" },
      { title: "About", icon: "mdi-help-box", to: "/about" },
    ],
});

