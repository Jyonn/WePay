import { Routes } from '@angular/router';
import {
    AdministrationOrderComponent,
    AdministrationOrderUnreceivedComponent,
    AdministrationOrderUnsentComponent
} from './'

import { AuthGuard } from "app/_guards";
export const administrationOrderRoutes: Routes = [
    {
        path: 'order',
        component: AdministrationOrderComponent,
        canActivate: [AuthGuard],
        children: [
            {
                path: '',
                redirectTo: 'unsent',
                pathMatch: 'full'
            },
            {
                path: 'unsent',
                component: AdministrationOrderUnsentComponent
            },
            {
                path: 'unreceived',
                component: AdministrationOrderUnreceivedComponent
            }
        ]
    }
];