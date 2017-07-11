import { Injectable } from '@angular/core';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch';

@Injectable()
export class SellerInfoService {

    private URL: string;
    private headers: Headers;
    private options: RequestOptions;
    constructor(private http: Http) {
        this.headers = new Headers();
        this.headers.append('Content-Type', 'application/json');
        this.headers.append('Accept', 'application/json');
        this.options = new RequestOptions({ headers: this.headers });
    }

    getSellerInfo() {
        this.URL = '/card';
        return this.http.get(this.URL)
            .map((response: Response) => response.json()).catch(this.handleError);
    }

    addSellerInfo(card: string, is_default: number) {
        this.URL = '/card';
        let sellerInfo = JSON.stringify({ card: card, is_default: is_default });

        return this.http.post(this.URL, sellerInfo, this.options)
            .map((response: Response) => response.json()).catch(this.handleError);
    }

    deleteSellerInfo(cardID: number) {
        this.URL = '/card';
        let deleteURL = this.URL + "/" + cardID;
        return this.http.delete(this.URL)
            .map((response: Response) => response.json()).catch(this.handleError);
    }

    updateSellerInfo(cardID: number) {
        this.URL = '/user/default-card';
        let sellerInfo = JSON.stringify({ card_id: cardID });
        return this.http.put(this.URL, sellerInfo, this.options)
            .map((response: Response) => response.json()).catch(this.handleError);
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