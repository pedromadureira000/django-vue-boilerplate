import {UserState} from "@/store/auth/types";

export default (): UserState => ({
	currentUser: null,
	csrftoken: ""
})  
