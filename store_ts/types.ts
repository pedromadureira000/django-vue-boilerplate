interface menuItem {
	title: string;
	icon: string;
	to: string;
}

export interface RootState {
	drawer: boolean;
	menuItems: menuItem[];
}
