import { HttpClient } from "@angular/common/http";
import { Injectable, inject } from "@angular/core";
import { Observable } from "rxjs";

@Injectable()
export class ProductService {
    private readonly http = inject(HttpClient);

    getProducts(): Observable<any> {
        return this.http.get('http://localhost:8000/products')
    }
}