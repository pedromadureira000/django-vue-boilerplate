import {Commit, Dispatch} from "vuex"

export const doesHttpOnlyCookieExist = (cookiename: string): boolean => {
	var d = new Date();
	d.setTime(d.getTime() + (1000));
	var expires = "expires=" + d.toUTCString();
	document.cookie = cookiename + "=new_value;path=/;" + expires;
	return document.cookie.indexOf(cookiename + '=') == -1;
}

export const setCookie = (name: string, value: string, days: number) => {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

export const getCookie = (name: string) => {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

export const eraseCookie = (name: string) => {   
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

export const handleError = (response: any, commit: Commit) => {
	console.log('>>>>>>>>>> handlerror: ', response)
	if (response.data ===  "Session already open."){
		commit("toggleSessionError")
	}
}
