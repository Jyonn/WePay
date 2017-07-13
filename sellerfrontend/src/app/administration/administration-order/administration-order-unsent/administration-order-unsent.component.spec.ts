import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdministrationOrderUnsentComponent } from './administration-order-unsent.component';

describe('AdministrationOrderUnsentComponent', () => {
  let component: AdministrationOrderUnsentComponent;
  let fixture: ComponentFixture<AdministrationOrderUnsentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdministrationOrderUnsentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdministrationOrderUnsentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
