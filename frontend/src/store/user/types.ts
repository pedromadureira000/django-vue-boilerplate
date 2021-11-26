interface menuItem {
	title: string;
	icon: string;
	to: string;
}

export class User {
	first_name!: string;
	last_name!: string;
	email!: string;
	modules!: menuItem[];
}

type user = User | null;


export interface UserState {
	user: user,
	csrftoken: string,
}
