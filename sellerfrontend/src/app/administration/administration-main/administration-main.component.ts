import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from "../../_services/index";
import { ActivatedRoute, Router, ActivatedRouteSnapshot, RouterState, RouterStateSnapshot } from '@angular/router';

@Component({
  selector: 'app-administration-main',
  templateUrl: './administration-main.component.html',
  styleUrls: ['./administration-main.component.css']
})
export class AdministrationMainComponent implements OnInit {
  public imgSrc: string = "../../../assets/img/sp_girl.png";

  constructor(
    private authenticationService: AuthenticationService,
    private router: Router
  ) { }

  ngOnInit() {
    this.imgSrc = localStorage.getItem("avatar");
    if (!this.imgSrc) {
      this.imgSrc = "../../../assets/img/sp_girl.png";
    }
  }

  public doLogout(): void {
    this.authenticationService.logout();
    this.router.navigateByUrl("");
  }
}
