import { Observable } from 'rxjs/Observable';
import { MdPaginator } from '@angular/material';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/observable/merge';
import 'rxjs/add/operator/map';
import { DataSource } from '@angular/cdk';
import { Order } from 'app/_model'
import { UnreceivedOrderDatabase } from './administration-order-unreceived/unreceived-order-database'
import { UnsentOrderDatabase } from './administration-order-unsent/unsent-order-database'

export class OrderDataSource extends DataSource<any> {
    constructor(private _orderDatabaseService: UnreceivedOrderDatabase | UnsentOrderDatabase,
        private _paginator: MdPaginator) {
        super();
    }

    /** Connect function called by the table to retrieve one stream containing the data to render. */
    connect(): Observable<Order[]> {
        const displayDataChanges = [
            this._orderDatabaseService.dataChange,
            this._paginator.page
        ];

        return Observable.merge(...displayDataChanges).map(() => {
            const data = this._orderDatabaseService.data.slice();

            // Grab the page's slice of data.
            const startIndex = this._paginator.pageIndex * this._paginator.pageSize;
            return data.splice(startIndex, this._paginator.pageSize);
        });
    }

    disconnect() { }
}