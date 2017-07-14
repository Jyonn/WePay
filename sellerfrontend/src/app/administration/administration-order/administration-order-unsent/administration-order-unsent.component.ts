import { Component, ViewChild, OnInit } from '@angular/core';
import { MdPaginator, PageEvent } from '@angular/material';
import { Order, TotalNum } from 'app/_model'
import { OrderDatabase } from '../order-database'
import { OrderService } from 'app/_services'
import { OrderDataSource } from '../order-datasource'
@Component({
  selector: 'app-administration-order-unsent',
  templateUrl: './administration-order-unsent.component.html',
  styleUrls: ['./administration-order-unsent.component.css']
})
export class AdministrationOrderUnsentComponent implements OnInit {
  displayedColumns: string[];
  orderDatabase: OrderDatabase;
  dataSource: OrderDataSource | null;
  totalNum: TotalNum;

  constructor(private orderService: OrderService) {

  }

  @ViewChild(MdPaginator) paginator: MdPaginator;

  ngOnInit() {
    this.displayedColumns = ['order_detail', 'buyer_real_name_phone', 'address', 'operation'];
    this.orderDatabase = new OrderDatabase(this.orderService, "unsent");
    this.dataSource = new OrderDataSource(this.orderDatabase, this.paginator);
    this.paginator.pageSize = 10;
    this.totalNum = {
      totalNumber: 20
    }
    this.orderDatabase.flushOrdersInfo(0, this.paginator.pageSize, this.totalNum);
  }

  public sent(order_id: number) {
    this.orderDatabase.deleteOrderInfo(this.paginator.pageIndex, this.paginator.pageSize, order_id, this.totalNum);
  }

  public onPageChange(event: PageEvent) {
    this.orderDatabase.flushOrdersInfo(event.pageIndex, event.pageSize, this.totalNum);
  }

}