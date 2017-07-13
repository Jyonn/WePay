import { GoodService, SnackBarService } from 'app/_services'
import { Good, Category } from 'app/_model'
import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { Location } from '@angular/common';
import 'rxjs/add/operator/switchMap';

@Component({
  selector: 'app-administration-good-edit',
  templateUrl: './administration-good-edit.component.html',
  styleUrls: ['./administration-good-edit.component.css']
})
export class AdministrationGoodEditComponent implements OnInit {
  is_modified: number;
  public goodForm: FormGroup;
  public good: Good = new Good();
  public errorMsg: string;
  constructor(
    private goodService: GoodService,
    private snackBarService: SnackBarService,
    public route: ActivatedRoute,
    private fb: FormBuilder,
    private location: Location
  ) { }

  ngOnInit() {
    this.is_modified = 0;

    this.createForm();
    this.route.paramMap
      .switchMap((params: ParamMap) => this.goodService.getGoodInfo(+params.get('id'))).subscribe(
      data => {
        if (data.code == 0) {
          this.good.category_name = data.body.category_name;
          this.good.description = data.body.description;
          this.good.name = data.body.name;
          this.good.pic = data.body.pic;
          this.good.price = data.body.price;
          this.good.store = data.body.store;
          this.good.good_id = data.body.good_id;
          this.snackBarService.openSnackBar("刷新数据成功！");
        }
      },
      error => {
        console.error(error);
      }
      );

  }

  private createForm(): void {
    this.goodForm = this.fb.group(
      {
        "name":
        [
          this.good.name,
          [
            Validators.minLength(1),
            Validators.maxLength(20),
            Validators.required
          ]
        ],
        "price":
        [
          this.good.price,
          [
            Validators.min(0.01),
            Validators.required
          ]
        ],
        "store":
        [
          this.good.store,
          [
            Validators.min(0),
            Validators.required
          ]
        ],
        "description":
        [
          this.good.description,
          [
            Validators.maxLength(512)
          ]
        ]
      }
    );
  }

  public editGood() {
    this.good.name = this.goodForm.value.name;
    this.good.description = this.goodForm.value.description;
    this.good.price = this.goodForm.value.price;
    this.good.store = this.goodForm.value.store;
    
    this.goodService.editGoodInfo(this.good, this.is_modified).subscribe(data => {
      if (data.code > 0) {
        this.errorMsg = data.msg;
      }
      else {
        this.errorMsg = "正在上传中...";
        setTimeout(() => {
          this.errorMsg = "";
          this.snackBarService.openSnackBar("修改成功！");
          this.location.back();
        }, 1000);
      }
    },
      error => {
        console.error(error);
      }
    );
  }

  public previewImage(event): void {
    if (event.target.files && event.target.files[0]) {
      var reader = new FileReader();
      reader.onload = (e: any) => {
        this.is_modified = 1;
        this.good.pic = e.target.result;
      }
      reader.readAsDataURL(event.target.files[0]);
    }
  }
  /**
   * cancel
   */
  public cancel() {
    this.location.back();
  }

}


