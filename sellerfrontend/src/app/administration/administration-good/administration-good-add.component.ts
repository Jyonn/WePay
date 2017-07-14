import { GoodService, SnackBarService } from 'app/_services'
import { Good, Category } from 'app/_model'
import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-administration-good-add',
  templateUrl: './administration-good-add.component.html',
  styleUrls: ['./administration-good-add.component.css']
})
export class AdministrationGoodAddComponent implements OnInit {
  public goodForm: FormGroup;
  public category: Category[];
  public newGood: Good = new Good();
  public errorMsg: string;
  public imgSrc: string;
  constructor(
    private goodService: GoodService,
    private snackBarService: SnackBarService,
    public router: Router,
    private fb: FormBuilder,
    private location: Location
  ) { }

  ngOnInit() {
    this.category = [
      {
        category_id: 1,
        category_name: "洗发水"
      },
      {
        category_id: 2,
        category_name: "沐浴露"
      }
    ]
    this.getCategory();
    this.createForm();

  }

  private getCategory() {
    this.goodService.getCategory().subscribe(data => {
      if (data.code == 0) {
        this.snackBarService.openSnackBar("获取商品类别成功！");
        this.category = data.body;
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
        "category_id":
        [
          "",
          [
            Validators.required
          ]
        ],
        "good_name":
        [
          "",
          [
            Validators.minLength(1),
            Validators.maxLength(20),
            Validators.required
          ]
        ],
        "price":
        [
          "",
          [
            Validators.min(0.01),
            Validators.required
          ]
        ],
        "store":
        [
          "",
          [
            Validators.min(0),
            Validators.required
          ]
        ],
        "description":
        [
          "",
          [
            Validators.maxLength(512)
          ]
        ]
      }
    );
  }

  public addGood() {
    this.newGood = {
      good_id: null,
      category_id: this.goodForm.value.category_id,
      category_name: null,
      good_name: this.goodForm.value.good_name,
      price: this.goodForm.value.price,
      store: this.goodForm.value.store,
      pic: this.imgSrc,
      description: this.goodForm.value.description,
      gzipped: 0
    }
    this.goodService.addGoodInfo(this.newGood).subscribe(data => {
      if (data.code > 0) {
        this.errorMsg = data.msg;
      }
      else {
        this.errorMsg = "正在上传中...";
        setTimeout(() => {
          this.errorMsg = "";
          this.snackBarService.openSnackBar("添加成功！");
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
        this.imgSrc = e.target.result;
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


