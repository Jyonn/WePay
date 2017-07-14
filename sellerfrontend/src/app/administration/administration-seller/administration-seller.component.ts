import { Component, OnInit } from '@angular/core';
import { SellerInfoService } from 'app/_services/index'
import { Card } from 'app/_model/index'
import { MdCheckboxChange } from '@angular/material';
import { SnackBarService } from 'app/_services/index';
import { Router } from '@angular/router';
import { DialogService } from 'app/_services';

@Component({
  selector: 'app-administration-seller',
  templateUrl: './administration-seller.component.html',
  styleUrls: ['./administration-seller.component.css']
})
export class AdministrationSellerComponent implements OnInit {
  cards: Card[];
  defaultCard: Card;
  constructor(
    private sellerInfoService: SellerInfoService,
    private snackBarService: SnackBarService,
    private router: Router,
    private dialogService: DialogService
  ) { }

  ngOnInit() {

    this.cards = [
      {
        card: "1111",
        card_id: 1,
        is_default: 1
      },
      {
        card: "2222",
        card_id: 2,
        is_default: 0
      }
    ];
    this.defaultCard = this.cards[0];
    this.getSellerInfo();
  }

  private getSellerInfo(): void {
    this.sellerInfoService.getSellerInfo().subscribe(
      data => {
        if (data.code == 0) {
          this.cards = data.body;
          console.log(this.cards);
          this.snackBarService.openSnackBar("刷新数据成功！");
          this.cards.forEach(card => {
            if (card.is_default == 1) {
              this.defaultCard = card;
            }
          })
        }
      },
      error => {
        console.error(error);
      }
    );
  }
  /**
   * onCheckBoxChange
   */
  public onCheckBoxChange(event: MdCheckboxChange, card: Card) {
    if (card == this.defaultCard) {
      this.snackBarService.openSnackBar("请选择其他银行卡作为默认银行卡，必须有且仅有一张默认银行卡！");
      event.source.checked = true;
    }
    else {
      this.sellerInfoService.updateSellerInfo(card.card_id).subscribe(
        data => {
          if (data.code == 0) {
            this.defaultCard.is_default = 0;
            card.is_default = 1
            this.defaultCard = card;
            this.snackBarService.openSnackBar("成功设定默认银行卡！");
          }
        },
        error => {
          console.error(error);
        }
      );
    }
  }

  public deleteCard(card: Card): void {
    if (this.defaultCard === card) {
      this.snackBarService.openSnackBar("不能删除默认银行卡，请先修改默认银行卡！");
    }
    else {
      this.dialogService
        .confirm('确认对话框', '你确定要删除银行卡吗，删除后将不可恢复？')
        .subscribe(res => {
          if (res == true) {
            this.sellerInfoService.deleteSellerInfo(card.card_id).subscribe(
              data => {
                if (data.code == 0) {
                  this.cards = this.cards.filter(c => c !== card);
                  this.snackBarService.openSnackBar("删除成功！");
                }
              },
              error => {
                console.error(error);
              }
            );
          }
        });


    }
  }

  /**
   * addCard
   */
  public addCard() {
    this.router.navigateByUrl("administration/addSeller");
  }
}
