import { Component, OnInit, inject } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product';

@Component({
  selector: 'app-product-list',
  standalone: true,
  providers: [ProductService],
  templateUrl: './product-list.component.html',
  styleUrl: './product-list.component.scss'
})
export class ProductListComponent implements OnInit {
  ps = inject(ProductService);
  products: Array<Product> = [];

  ngOnInit(): void {
    this.ps.getProducts().subscribe(r => {
      this.products = r.data;
    })
  }
}
