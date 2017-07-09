import { Injectable } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch';

@Injectable()
export class AuthenticationService {
    private loginURL: string = '/session';
    constructor(private http: Http) { }

    login(username: string, password: string) {

        return this.http.post(this.loginURL, { username: username, password: password })
            .map((response: Response) => {
                let responseJson = response.json().data;
                console.log(responseJson);
                if (responseJson.code == 0) {
                    localStorage.setItem('currentUser', responseJson.body.user_id);
                }
                return responseJson;
            }).catch(this.handleError);
    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
        return this.http.delete(this.loginURL)
            .map((response: Response) => {

                /*

                {
                    'code': 0
                    'msg': OK
                    'body': []
                }
                
                */
                // login successful if there's a jwt token in the response
                /*
                let user = response.json();
                if (user && user.token) {
                    // store user details and jwt token in local storage to keep user logged in between page refreshes
                    localStorage.setItem('currentUser', JSON.stringify(user));
                }
 
                return user;
                */
            });
    }
    private handleError(error: Response | any) {
        // In a real world app, you might use a remote logging infrastructure
        let errMsg: string;
        if (error instanceof Response) {
            const body = error.json() || '';
            const err = body.error || JSON.stringify(body);
            errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Observable.throw(errMsg);
    }
}