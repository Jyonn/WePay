import { DataSource } from '@angular/cdk';
import { Order } from 'app/_model'
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import { MdPaginator } from '@angular/material';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/observable/merge';
import 'rxjs/add/operator/map';
import { OrderService } from 'app/_services'
import { TotalNum } from 'app/_model'
/** An order database that the data source uses to retrieve data for the table. */
export class OrderDatabase {
    /** Stream that emits whenever the data has been modified. */
    dataChange: BehaviorSubject<Order[]> = new BehaviorSubject<Order[]>([]);
    status: string;
    //last: number = 0;

    constructor(private orderService: OrderService, status: string) {
        this.status = status;
        /*
        for (let i = 0; i < 20; i++) {
            const copiedData = this.data.slice();
            copiedData.push(this.newOrder());
            this.dataChange.next(copiedData);
        }*/
    }

    get data(): Order[] {
        return this.dataChange.value;
    }

    flushOrdersInfo(page: number, count: number, totalNum: TotalNum) {
        if ((page + 1) * count > this.data.length) {

            return this.orderService.getOrdersInfo(this.data.length, count, this.status).subscribe(
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
                        totalNum.totalNumber = data.body.count;
                    }
                },
                error => {
                    console.error(error);
                }
            );
        }
    }

    deleteOrderInfo(page: number, count: number, order_id: number, totalNum: TotalNum) {

        this.orderService.deleteOrderInfo(order_id).subscribe(
            data => {
                if (data.code == 0) {
                    let start = page * count;
                    let end = (page + 1) * count > this.data.length ? this.data.length : (page + 1) * count;
                    let tempData = this.data.slice(start, end);
                    let deleteIndex = 0;
                    tempData.filter((value, index) => {
                        if (value.order_id == order_id)
                            deleteIndex = index;
                    })
                    this.data.splice(page * count + deleteIndex, 1);
                    this.dataChange.next(this.data);
                    totalNum.totalNumber--;
                    this.flushOrdersInfo(page, count, totalNum);
                }
            },
            error => {
                console.error(error);
            }
        );
    }
/*
    private newOrder(): Order {
        this.last++;
        return new Order(
            "dd",
            "edward",
            "17816872348",
            this.last,
            "dsadas",
            this.last
        )
    }*/
}
