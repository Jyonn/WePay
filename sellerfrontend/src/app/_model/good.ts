export class Good {
	good_id: number;
	category_id: number;
	category_name: string;
	name: string;
	price: number;
	store: number;
	pic: string;
	description: string;
	gzipped: number;

	constructor() {
		this.good_id = 0;
		this.category_id = 0;
		this.category_name = "";
		this.name = "";
		this.price = 0;
		this.store = 0;
		this.pic = "";
		this.description = "";
		this.gzipped = 0;
	}
}