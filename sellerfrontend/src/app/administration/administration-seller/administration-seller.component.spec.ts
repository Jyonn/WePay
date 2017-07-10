import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdministrationSellerComponent } from './administration-seller.component';

describe('AdministrationSellerComponent', () => {
  let component: AdministrationSellerComponent;
  let fixture: ComponentFixture<AdministrationSellerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdministrationSellerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdministrationSellerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
