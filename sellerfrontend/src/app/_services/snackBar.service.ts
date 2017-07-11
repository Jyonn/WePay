import { Injectable } from '@angular/core';
import { MdSnackBar } from '@angular/material';

@Injectable()
export class SnackBarService {

    constructor(private snackBar: MdSnackBar) {

    }
    public openSnackBar(content: string) {
        this.snackBar.open(content, null, {
            duration: 1000
        });
    }
}