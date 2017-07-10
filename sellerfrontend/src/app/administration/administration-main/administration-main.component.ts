import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from "../../_services/index";
import { ActivatedRoute, Router, ActivatedRouteSnapshot, RouterState, RouterStateSnapshot } from '@angular/router';

@Component({
  selector: 'app-administration-main',
  templateUrl: './administration-main.component.html',
  styleUrls: ['./administration-main.component.css']
})
export class AdministrationMainComponent implements OnInit {

  constructor(
    private authenticationService:AuthenticationService,
    private router: Router
  ) { }

  ngOnInit() {
  }

  public doLogout(): void {
    this.authenticationService.logout();
    this.router.navigateByUrl("");
  }
}
