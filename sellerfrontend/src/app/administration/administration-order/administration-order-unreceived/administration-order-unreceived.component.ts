import { Component, ViewChild, OnInit } from '@angular/core';
import { MdPaginator, PageEvent } from '@angular/material';
import { OrderService } from 'app/_services'
import { OrderDataSource } from '../order-datasource'
import { Order, TotalNum } from 'app/_model'
import { OrderDatabase } from '../order-database'

@Component({
  selector: 'app-administration-order-unreceived',
  templateUrl: './administration-order-unreceived.component.html',
  styleUrls: ['./administration-order-unreceived.component.css']
})

export class AdministrationOrderUnreceivedComponent implements OnInit {
  displayedColumns: string[];
  orderDatabase: OrderDatabase;
  dataSource: OrderDataSource | null;
  totalNum: TotalNum;

  constructor(private orderService: OrderService) {

  }

  @ViewChild(MdPaginator) paginator: MdPaginator;

  ngOnInit() {
    this.displayedColumns = ['order_detail', 'buyer_real_name_phone', 'address'];
    this.orderDatabase = new OrderDatabase(this.orderService, "unreceived");
    this.dataSource = new OrderDataSource(this.orderDatabase, this.paginator);
    this.paginator.pageSize = 10;
    this.totalNum = {
      totalNumber: 20
    }
    this.orderDatabase.flushOrdersInfo(0, this.paginator.pageSize, this.totalNum);
  }

  public onPageChange(event: PageEvent) {
    this.orderDatabase.flushOrdersInfo(event.pageIndex, event.pageSize, this.totalNum);
  }

}