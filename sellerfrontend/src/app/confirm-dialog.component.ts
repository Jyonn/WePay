import { MdDialogRef } from '@angular/material';
import { Component } from '@angular/core';

@Component({
    selector: 'confirm-dialog',
    template: `
    <h1 md-dialog-title>{{ title }}</h1>
    <md-dialog-content>
     {{ message }}
    </md-dialog-content>
    <md-dialog-actions>
        <button type="button" md-raised-button 
            (click)="dialogRef.close(true)">是</button>
        <button type="button" md-button 
            (click)="dialogRef.close()" md-dialog-close>否</button>
    </md-dialog-actions>
    `,
})
export class ConfirmDialog {

    public title: string;
    public message: string;

    constructor(public dialogRef: MdDialogRef<ConfirmDialog>) {

    }
}
