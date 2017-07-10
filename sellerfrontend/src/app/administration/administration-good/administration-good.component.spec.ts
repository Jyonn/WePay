import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdministrationGoodComponent } from './administration-good.component';

describe('AdministrationGoodComponent', () => {
  let component: AdministrationGoodComponent;
  let fixture: ComponentFixture<AdministrationGoodComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdministrationGoodComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdministrationGoodComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
