import 'hammerjs';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import {
  MdToolbarModule,
  MdInputModule,
  MdCardModule,
  MdButtonModule,
  MdSlideToggleModule,
  MdSidenavModule,
  MdIconModule,
  MdSelectModule,
  MdSnackBarModule,
  MdCheckboxModule,
  MdTableModule,
  MdPaginatorModule,
  MdTabsModule
} from '@angular/material';
import { CdkTableModule } from '@angular/cdk'
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AuthGuard } from "./_guards/auth.guard";
import {
  AuthenticationService,
  SellerInfoService,
  SnackBarService,
  GoodService
} from './_services'
import { HttpModule } from '@angular/http';
import { EqualValidator } from "./register/directives/equal-validator.directive";
import { RegisterService } from "./register/register.service";
import { appRoutes } from './app.routes';
import { RouterModule } from '@angular/router';
import {
  AdministrationSellerComponent,
  AdministrationGoodComponent,
  AdministrationOrderComponent,
  AdministrationMainComponent,
  AdministrationSellerAddComponent,
  AdministrationGoodAddComponent,
  AdministrationGoodEditComponent
} from "./administration";
@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    EqualValidator,
    AdministrationMainComponent,
    AdministrationSellerComponent,
    AdministrationGoodComponent,
    AdministrationOrderComponent,
    AdministrationSellerAddComponent,
    AdministrationGoodAddComponent,
    AdministrationGoodEditComponent
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
    HttpModule,
    MdSidenavModule,
    MdIconModule,
    MdCheckboxModule,
    MdSnackBarModule,
    MdSelectModule,
    MdTableModule,
    MdPaginatorModule,
    CdkTableModule,
    MdTabsModule,  
    RouterModule.forRoot(appRoutes)
  ],
  providers: [
    AuthGuard,
    AuthenticationService,
    RegisterService,
    SellerInfoService,
    SnackBarService,
    GoodService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
