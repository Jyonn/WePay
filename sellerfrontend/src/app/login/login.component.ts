import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router, ActivatedRouteSnapshot, RouterState, RouterStateSnapshot } from '@angular/router';
import { AuthenticationService } from '../_services/index';
import { Observable } from 'rxjs/Observable';
import { Seller } from '../_model/index';
import { FormGroup , Validators, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  public loginForm: FormGroup;
  public seller: Seller = new Seller();
  public errorMsg: Error;

  constructor(
    public router: Router,
    public activatedRoute: ActivatedRoute,
    public authenticationService: AuthenticationService,
    private fb: FormBuilder
  ) {}



  ngOnInit() {
    let activatedRouteSnapshot: ActivatedRouteSnapshot = this.activatedRoute.snapshot;
    let routerState: RouterState = this.router.routerState;
    let routerStateSnapshot: RouterStateSnapshot = routerState.snapshot;
    this.createForm();
  }

  private createForm():void{
    this.loginForm = this.fb.group({
      "username": [
        "",
        [
          Validators.required,
          Validators.minLength(4),
          Validators.maxLength(20)
        ]
      ],
      "password": [
        "",
        [
          Validators.required,
          Validators.minLength(6),
        ]
      ]
    });
    
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
                else{
                  this.router.navigateByUrl("");
                }
            },
            error => {
                console.error(error);
            }
            );
  }

  public doRegister() {
    this.router.navigateByUrl("register");
  }

}
