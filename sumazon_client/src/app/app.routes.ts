import { Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
    { path: 'login', loadComponent: () => import('./components/login/login.component').then(c => c.LoginComponent) },
    { path: 'manage-products', canActivate: [AuthGuard], loadComponent: () => import('./components/product-list/product-list.component').then(c => c.ProductListComponent) },
    { path: 'product-list', loadComponent: () => import('./components/product-list/product-list.component').then(c => c.ProductListComponent) },
    { path: 'user-profile', loadComponent: () => import('./components/user-profile/user-profile.component').then(c => c.UserProfileComponent) },
    { path: 'cart', loadComponent: () => import('./components/cart/cart.component').then(c => c.CartComponent) },
    { path: 'product-details/:product_id', loadComponent: () => import('./components/product/product.component').then(c => c.ProductComponent) },
    { path: '', pathMatch: 'full', redirectTo: 'login' }
];
