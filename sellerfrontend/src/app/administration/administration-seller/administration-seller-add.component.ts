import { SellerInfoService, SnackBarService } from 'app/_services/index'
import { Card } from 'app/_model/index'
import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router, ActivatedRouteSnapshot, RouterState, RouterStateSnapshot } from '@angular/router';


@Component({
  selector: 'app-administration-seller-add',
  templateUrl: './administration-seller-add.component.html',
  styleUrls: ['./administration-seller-add.component.css']
})
export class AdministrationSellerAddComponent implements OnInit {
  public cardForm: FormGroup;
  public newCard: Card = new Card();
  public errorMsg: Error;
  constructor(
    private sellerInfoService: SellerInfoService,
    private snackBarService: SnackBarService,
    public router: Router,
    public activatedRoute: ActivatedRoute,
    private fb: FormBuilder
  ) { }

  ngOnInit() {
    this.createForm();

  }


  private createForm(): void {
    this.cardForm = this.fb.group(
      {
        "cardname":
        [
          "",
          [
            Validators.required
          ]
        ],
        "default": ""
      }
    );
  }

  public addCard() {
    this.newCard.card = this.cardForm.value.card;
    this.newCard.is_default = this.cardForm.value.is_default;

    this.sellerInfoService.addSellerInfo(this.cardForm.value.card, this.cardForm.value.is_default).subscribe(data => {
      if (data.code > 0) {
        this.errorMsg = data.msg;
      }
      else {
        this.snackBarService.openSnackBar("添加成功！");
        this.router.navigateByUrl("administration/seller");
      }
    },
      error => {
        console.error(error);
      }
    );
  }

  /**
   * cancel
   */
  public cancel() {
    this.router.navigateByUrl("administration/seller");
  }

}


