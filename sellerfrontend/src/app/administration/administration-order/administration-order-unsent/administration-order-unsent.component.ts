import { Component, ViewChild, OnInit } from '@angular/core';
import { MdPaginator, PageEvent } from '@angular/material';
import { Order } from 'app/_model'
import { UnsentOrderDatabase } from './unsent-order-database'
import { OrderService } from 'app/_services'
import { OrderDataSource } from '../order-datasource'
@Component({
  selector: 'app-administration-order-unsent',
  templateUrl: './administration-order-unsent.component.html',
  styleUrls: ['./administration-order-unsent.component.css']
})
export class AdministrationOrderUnsentComponent implements OnInit {
  displayedColumns: string[];
  orderDatabase: UnsentOrderDatabase;
  dataSource: OrderDataSource | null;
  totalNum:TotalNum;

  constructor(private orderService: OrderService) {

  }

  @ViewChild(MdPaginator) paginator: MdPaginator;

  ngOnInit() {
    this.displayedColumns = ['detail', 'real_name', 'phone', 'address', 'operation'];
    this.orderDatabase = new UnsentOrderDatabase(this.orderService);
    this.dataSource = new OrderDataSource(this.orderDatabase, this.paginator);
    this.paginator.pageSize = 10;
    this.orderDatabase.flushOrdersInfo(0, this.paginator.pageSize, this.totalNum);
    this.totalNum = {
      totalNumber:0
    }
  }

  public sent(order_id: number) {
    this.orderDatabase.deleteOrderInfo(this.paginator.pageIndex, this.paginator.pageSize, order_id, this.totalNum);
    //to do delete order
  }

  public onPageChange(event: PageEvent) {
    console.log(event);
    this.orderDatabase.flushOrdersInfo(event.pageIndex, event.pageSize, this.totalNum);
  }

}

export interface TotalNum{
  totalNumber:number;
}