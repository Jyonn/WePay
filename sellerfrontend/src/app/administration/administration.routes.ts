import { Routes } from '@angular/router';
import {AdministrationSellerComponent} from './administration-seller/administration-seller.component';
import {AdministrationGoodComponent} from './administration-good/administration-good.component';
import {AdministrationOrderComponent} from './administration-order/administration-order.component';
import {AdministrationMainComponent} from './administration-main/administration-main.component';
import { AuthGuard } from "app/_guards";

export const administrationRoutes: Routes =[
    {
        path: 'administration',
        component: AdministrationMainComponent,
        canActivate: [AuthGuard],
        children: [
                {
                    path: '', 
                    redirectTo:'order',
                    pathMatch:'full'
                },
                {
                    path: 'seller',
                    component: AdministrationSellerComponent
                },
                {
                    path: 'good',
                    component: AdministrationGoodComponent
                },
                {
                    path: 'order', 
                    component: AdministrationOrderComponent  
                }
        ]
    }
];