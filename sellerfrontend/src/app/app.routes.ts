import { Routes } from '@angular/router';
 
import { LoginComponent } from './login/index';
import { RegisterComponent } from './register/index';
import { AuthGuard } from './_guards/index';
import { administrationRoutes }from './administration/administration.routes'
 
export const appRoutes: Routes = [
    { path: '', redirectTo:'administration', pathMatch:'full' },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },
    ...administrationRoutes,
    // otherwise redirect to home
    { path: '**', redirectTo: '' }
]; 