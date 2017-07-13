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
import { TotalNum } from './administration-order-unsent.component'
/** An order database that the data source uses to retrieve data for the table. */
export class UnsentOrderDatabase {
    /** Stream that emits whenever the data has been modified. */
    dataChange: BehaviorSubject<Order[]> = new BehaviorSubject<Order[]>([]);
    public last = 0;


    constructor(private orderService: OrderService) {

    }

    get data(): Order[] {
        return this.dataChange.value;
    }

    flushOrdersInfo(page: number, count: number, totalNum: TotalNum) {
        console.log(page + " " + count + " " + this.data.length);
        if ((page + 1) * count > this.data.length) {
/*
            const copiedData = this.data.slice();
            for (let i = 1; i <= count; i++) {
                copiedData.push(this.createNewUser());
            }
            this.dataChange.next(copiedData);
            totalNum.totalNumber += 10;
*/
            return this.orderService.getOrdersInfo(this.data.length, count, "unsent").subscribe(
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
/*
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
        */

        this.orderService.delteOrderInfo(order_id).subscribe(
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
                    const copiedData = this.data.splice(page * count + deleteIndex, 1);
                    this.dataChange.next(copiedData);
                    totalNum.totalNumber--;
                    this.flushOrdersInfo(page, count, totalNum);
                }
            },
            error => {
                console.error(error);
            }
        );
    }


    /** Builds and returns a new User. */
    private createNewUser(): Order {
        this.last++;
        return {
            good_name: "沙宣洗发露",
            real_name: "陈毅强",
            phone: this.last.toString(),
            address: "浙江省杭州市浙江大学玉泉校区30舍",
            number: 1,
            order_id: this.last
        };
    }
}
