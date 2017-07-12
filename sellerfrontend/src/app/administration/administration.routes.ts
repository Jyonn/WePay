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
                path: 'order',
                component: AdministrationOrderComponent
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
            }
        ]
    }
];