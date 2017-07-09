import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router, ActivatedRouteSnapshot, RouterState, RouterStateSnapshot } from '@angular/router';
import { AuthenticationService } from '../_services/index';
import { Observable } from 'rxjs/Observable';

import { Seller } from '../_model/index';

import { FormControl, Validators } from '@angular/forms';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  usernameFormControl = new FormControl('', [
    Validators.required]);
  passwordFormControl = new FormControl('', [
    Validators.required]);
  public seller: Seller = new Seller();
  public errorMsg: Error;

  constructor(
    public router: Router,
    public activatedRoute: ActivatedRoute,
    public authenticationService: AuthenticationService
  ) {
    console.log(this.authenticationService);
  }

  ngOnInit() {
    console.log("--- user-login-component ---");
    console.log(this.router);
    console.log(this.activatedRoute);

    let activatedRouteSnapshot: ActivatedRouteSnapshot = this.activatedRoute.snapshot;
    let routerState: RouterState = this.router.routerState;
    let routerStateSnapshot: RouterStateSnapshot = routerState.snapshot;

    console.log(activatedRouteSnapshot);
    console.log(routerState);
    console.log(routerStateSnapshot);
  }

  public doLogin(): void {
    /**
     * {
          'code': 错误代码，默认为0（OK）
          'msg': OK / 不存在的用户名 / 错误的用户名或密码
          'body': {
            'user_id': 用户ID
            'avatar': 用户头像链接
            'brand': 商家品牌（仅当用户为商家时存在）
          }
       }
     */
    this.authenticationService.login(this.seller.username, this.seller.password).subscribe(
            data => {
                if(data.code > 0){
                  this.errorMsg = data.msg;
                }
            },
            error => {
                console.error(error);
            }
            );
  }

  public doLogout(): void {
    this.authenticationService.logout();
    this.router.navigateByUrl("");
  }

  public doRegister() {
    this.router.navigateByUrl("register");
  }

}
