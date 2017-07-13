import { Injectable } from '@angular/core';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch';

@Injectable()
export class AuthenticationService {

    private loginURL: string;
    private headers: Headers;
    private options: RequestOptions;
    constructor(private http: Http) {
        this.loginURL = '/session'
        this.headers = new Headers();
        this.headers.append('Content-Type', 'application/json');
        this.headers.append('Accept', 'application/json');
        this.options = new RequestOptions({headers:this.headers});
    }

    login(username: string, password: string) {
        let user = JSON.stringify({ username: username, password: password });

        return this.http.post(this.loginURL, user, this.options)
            .map((response: Response) => {
                let responseJson = response.json();
                if (responseJson.code == 0) {
                    localStorage.setItem('currentUser', responseJson.body.user_id);
                }
                return responseJson;
            }).catch(this.handleError);
    }

    logout() {
        console.log(this.loginURL);
        
        // remove user from local storage to log user out
        return this.http.delete(this.loginURL)
            .map((response: Response) => {
                let responseJson = response.json();

                if (responseJson.code == 0) {
                    localStorage.removeItem('currentUser');
                }
                return responseJson;
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