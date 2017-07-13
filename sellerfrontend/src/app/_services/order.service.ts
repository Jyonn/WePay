import { Injectable } from '@angular/core';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch';

@Injectable()
export class OrderService {

    private URL: string;
    private headers: Headers;
    private options: RequestOptions;

    constructor(private http: Http) {
        this.headers = new Headers();
        this.headers.append('Content-Type', 'application/json');
        this.headers.append('Accept', 'application/json');
        this.options = new RequestOptions({ headers: this.headers });
    }


    public getOrdersInfo(exist: number, count: number, status:string) {
        this.URL = "/order?status=" + status + "&exist=" + exist + "&count=" + count;
        return this.http.get(this.URL)
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

    public delteOrderInfo(order_id:number) {
        this.URL = "/order/" + order_id + "/status";
        let orderInfo = JSON.stringify({
        });
        
        return this.http.put(this.URL, orderInfo, this.options)
            .map((response: Response) => response.json()).catch(this.handleError);
    }
}
