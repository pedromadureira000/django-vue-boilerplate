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

export interface UserState {
	currentUser: User | null,
	csrftoken: string
}

export default (): UserState => ({
	currentUser: null,
	csrftoken: ""
})  
