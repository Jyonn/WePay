import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdministrationOrderUnreceivedComponent } from './administration-order-unreceived.component';

describe('AdministrationOrderUnreceivedComponent', () => {
  let component: AdministrationOrderUnreceivedComponent;
  let fixture: ComponentFixture<AdministrationOrderUnreceivedComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdministrationOrderUnreceivedComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdministrationOrderUnreceivedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
