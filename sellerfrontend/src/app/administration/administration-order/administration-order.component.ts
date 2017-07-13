
import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-administration-order',
  templateUrl: './administration-order.component.html',
  styleUrls: ['./administration-order.component.css']
})
export class AdministrationOrderComponent implements OnInit {

  tabs = [
    {
      label: '待发货',
      link:"unsent",
    },
    {
      label: '待收货',
      link:"unreceived",
    },
  ];

  ngOnInit() {

  }

}