import { Routes } from '@angular/router';
import {
    AdministrationGoodAddComponent,
    AdministrationMainComponent,
    AdministrationOrderComponent,
    AdministrationGoodComponent,
    AdministrationSellerAddComponent,
    AdministrationSellerComponent,
    AdministrationGoodEditComponent
} from './'
import {administrationOrderRoutes} from './administration-order/administration-order.routes'
import { AuthGuard } from "app/_guards";
export const administrationRoutes: Routes = [
    {
        path: 'administration',
        component: AdministrationMainComponent,
        canActivate: [AuthGuard],
        children: [
            {
                path: '',
                redirectTo: 'seller',
                pathMatch: 'full'
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
                path: "addSeller",
                component: AdministrationSellerAddComponent
            },
            {
                path: "addGood",
                component: AdministrationGoodAddComponent
            },
            {
                path: "good/:id",
                component: AdministrationGoodEditComponent
            },
            ...administrationOrderRoutes
        ]
    },
];