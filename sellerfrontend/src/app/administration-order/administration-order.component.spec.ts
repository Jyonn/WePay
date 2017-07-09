import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdministrationOrderComponent } from './administration-order.component';

describe('AdministrationOrderComponent', () => {
  let component: AdministrationOrderComponent;
  let fixture: ComponentFixture<AdministrationOrderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdministrationOrderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdministrationOrderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
