import { Injectable } from '@angular/core';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch';

@Injectable()
export class RegisterService {

    private URL: string;
    private headers: Headers;
    private options: RequestOptions;
    constructor(private http: Http) {
        this.URL = '/user'
        this.headers = new Headers();
        this.headers.append('Content-Type', 'application/json');
        this.headers.append('Accept', 'application/json');
        this.options = new RequestOptions({ headers: this.headers });
    }

    addSeller(username: string, brand: string, password: string) {
        let user = JSON.stringify({
            password: password,
            is_seller: 1,
            brand: brand,
            username: username,
            captcha: 0
        }
        );

        return this.http.post(this.URL, user, this.options)
            .map((response: Response) => {
                let responseJson = response.json();
                if (responseJson.code == 0) {
                    localStorage.setItem('currentUser', responseJson.body.user_id);
                }
                return responseJson;
            }).catch(this.handleError);
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