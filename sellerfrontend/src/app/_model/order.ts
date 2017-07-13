export class Order {
    good_name: string;
    real_name: string;
    phone: string;
    address: string;
    number: number;
    order_id: number;
    constructor(good_name: string,
        real_name: string,
        phone: string,
        number: number,
        address:string,
        order_id: number) {
        this.good_name = good_name;
        this.real_name = real_name;
        this.phone = phone;
        this.address = address;
        this.number = number;
        this.order_id = order_id;
    }
}
