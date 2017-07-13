import { DataSource } from '@angular/cdk';
import { Order } from 'app/_model'
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import { MdPaginator } from '@angular/material';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/observable/merge';
import 'rxjs/add/operator/map';
import {OrderService} from 'app/_services'

/** An order database that the data source uses to retrieve data for the table. */
export class UnreceivedOrderDatabase {
    /** Stream that emits whenever the data has been modified. */
    dataChange: BehaviorSubject<Order[]> = new BehaviorSubject<Order[]>([]);


    constructor(private orderService:OrderService) {

    }

    get data(): Order[] {
        return this.dataChange.value;
    }

    flushOrdersInfo(page: number, count: number) {
        if ((page + 1) * count > this.data.length) {
            return this.orderService.getOrdersInfo(page, count, "unreceived").subscribe(
                data => {
                    if (data.code == 0) {
                        const copiedData = this.data.slice();

                        data.body.order_list.forEach(order => {
                            copiedData.push(new Order(
                                order.good_name,
                                order.real_name,
                                order.phone,
                                order.number,
                                order.address,
                                order.order_id
                            ));
                        });
                        this.dataChange.next(copiedData);
                    }
                },
                error => {
                    console.error(error);
                }
                );
        }
    }
}
