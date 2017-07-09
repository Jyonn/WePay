import 'hammerjs';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { AdministrationComponent } from './administration/administration.component';
import { AdministrationSellerComponent } from './administration-seller/administration-seller.component';
import { AdministrationGoodComponent } from './administration-good/administration-good.component';
import { AdministrationOrderComponent } from './administration-order/administration-order.component';
import { MdToolbarModule } from '@angular/material';
import { MdInputModule } from '@angular/material';
import { MdCardModule } from '@angular/material';
import { MdButtonModule } from '@angular/material';
import { MdSlideToggleModule } from '@angular/material';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AuthGuard } from "./_guards/auth.guard";
import { routing } from './app.routing';
import { AuthenticationService } from './_services/index'
import { HttpModule } from '@angular/http';
import { InMemoryWebApiModule } from 'angular-in-memory-web-api';
import { InMemoryDataService }  from './_services/index';
import { EqualValidator } from "./register/directives/equal-validator.directive";
import { RegisterService } from "app/register/register.service";
@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    AdministrationComponent,
    AdministrationSellerComponent,
    AdministrationGoodComponent,
    AdministrationOrderComponent,
    EqualValidator
  ],
  imports: [
    BrowserModule,
    MdToolbarModule,
    MdInputModule,
    FormsModule,
    ReactiveFormsModule,
    MdCardModule,
    MdButtonModule,
    MdSlideToggleModule,
    BrowserAnimationsModule,
    routing,
    HttpModule
  ],
  providers: [AuthGuard,
    AuthenticationService,
    RegisterService],
  bootstrap: [AppComponent]
})
export class AppModule { }
