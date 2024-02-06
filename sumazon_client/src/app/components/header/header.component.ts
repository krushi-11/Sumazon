import { Component, inject } from '@angular/core';
import { MatBadgeModule } from '@angular/material/badge';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { Router, RouterLink, RouterLinkActive, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatBadgeModule, MatButtonModule, MatIconModule, MatListModule, MatMenuModule, MatSidenavModule, MatToolbarModule, RouterLink, RouterLinkActive, RouterModule
  ],
  providers: [AuthService],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  as = inject(AuthService);
  router = inject(Router);
  
  menus: { label: string, isActive: boolean, route: string }[] = [
    {
      label: 'Product List', isActive: false, route: 'product-list'
    },
    {
      label: 'Manage Products', isActive: false, route: 'manage-products'
    }
  ]

  logout(): void {
    this.as.logout().subscribe((r) => {
      if (r) {
        this.router.navigate(['/login']);
      }
    })
  }

}
