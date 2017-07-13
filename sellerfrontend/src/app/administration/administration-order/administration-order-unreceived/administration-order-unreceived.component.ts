import { Component, ViewChild, OnInit } from '@angular/core';
import { MdPaginator,PageEvent } from '@angular/material';
import { Order } from 'app/_model'
import {UnreceivedOrderDatabase} from './unreceived-order-database'
import {OrderService} from 'app/_services'
import {OrderDataSource} from '../order-datasource'

@Component({
  selector: 'app-administration-order-unreceived',
  templateUrl: './administration-order-unreceived.component.html',
  styleUrls: ['./administration-order-unreceived.component.css']
})

export class AdministrationOrderUnreceivedComponent implements OnInit {
  displayedColumns:string[];
  orderDatabase :UnreceivedOrderDatabase;
  dataSource: OrderDataSource | null;
  totalNumber:number;

  constructor(private orderService:OrderService){

  }

  @ViewChild(MdPaginator) paginator: MdPaginator;

  ngOnInit() {
    this.displayedColumns = ['detail', 'real_name', 'phone', 'address', 'operation'];
    this.orderDatabase = new UnreceivedOrderDatabase(this.orderService);
    this.totalNumber = 20;
    this.dataSource = new OrderDataSource(this.orderDatabase, this.paginator);
    this.orderDatabase.flushOrdersInfo(0, this.paginator.pageSize);
  }

  public sent(order_id: number) {
    console.log(order_id);
  }

  public onPageChange(event:PageEvent){
    console.log(event);
    this.orderDatabase.flushOrdersInfo(event.pageIndex,event.pageSize);
  }
}