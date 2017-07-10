import 'hammerjs';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { MdToolbarModule } from '@angular/material';
import { MdInputModule } from '@angular/material';
import { MdCardModule } from '@angular/material';
import { MdButtonModule } from '@angular/material';
import { MdSlideToggleModule } from '@angular/material';
import { MdSidenavModule } from '@angular/material';
import { MdIconModule } from '@angular/material';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AuthGuard } from "./_guards/auth.guard";
import { AuthenticationService } from './_services/index'
import { HttpModule } from '@angular/http';
import { EqualValidator } from "./register/directives/equal-validator.directive";
import { RegisterService } from "./register/register.service";
import { appRoutes } from './app.routes';
import { RouterModule } from '@angular/router';
import { AdministrationSellerComponent, AdministrationGoodComponent, AdministrationOrderComponent, AdministrationMainComponent } from "./administration/index";


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    EqualValidator,
    AdministrationMainComponent,
    AdministrationSellerComponent,
    AdministrationGoodComponent,
    AdministrationOrderComponent
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
    RouterModule.forRoot(appRoutes)
  ],
  providers: [AuthGuard,
    AuthenticationService,
    RegisterService],
  bootstrap: [AppComponent]
})
export class AppModule { }
