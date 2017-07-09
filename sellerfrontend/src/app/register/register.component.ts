import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router, ActivatedRouteSnapshot, RouterState, RouterStateSnapshot } from '@angular/router';
import { AuthenticationService } from '../_services/index';
import { Observable } from 'rxjs/Observable';
import { Seller } from '../_model/index';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { RegisterService } from "app/register/register.service";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  public registerForm: FormGroup;
  public seller: Seller = new Seller();
  public errorMsg: Error;

  constructor(
    public router: Router,
    public activatedRoute: ActivatedRoute,
    public authenticationService: AuthenticationService,
    private fb: FormBuilder,
    private registerService: RegisterService
  ) { }



  ngOnInit() {
    let activatedRouteSnapshot: ActivatedRouteSnapshot = this.activatedRoute.snapshot;
    let routerState: RouterState = this.router.routerState;
    let routerStateSnapshot: RouterStateSnapshot = routerState.snapshot;
    this.createForm();
  }

  private createForm(): void {
    this.registerForm = this.fb.group({
      "username": [
        "",
        [
          Validators.required,
          Validators.minLength(4),
          Validators.maxLength(20)
        ]
      ],
      "brand": [
        "",
        [
          Validators.required,
          Validators.minLength(2),
          Validators.maxLength(32)
        ]
      ],
      "password": [
        "",
        [
          Validators.required,
          Validators.minLength(6),
        ]
      ],
      "confirmPassword": [
        "",
        []
      ]
    });

  }

  public doRegister() {
    this.registerService.addSeller(this.seller.username, this.seller.brand, this.seller.password).subscribe(data => {
      if (data.code > 0) {
        this.errorMsg = data.msg;
      }
      else {
        this.router.navigateByUrl("");
      }
    },
      error => {
        console.error(error);
      }
    );
  }

}

