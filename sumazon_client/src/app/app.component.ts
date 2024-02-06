import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { NavigationStart, Router, RouterOutlet } from '@angular/router';
import { HeaderComponent } from './components/header/header.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, HeaderComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  private readonly router = inject(Router);

  whitelistedUrls: string[] = ['/', '/login'];
  loaded: boolean = true;
  isLoggedIn: boolean = false;

  ngOnInit(): void {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationStart) {
        if (this.whitelistedUrls.includes(event.url)) {
          this.loaded = true;
          this.isLoggedIn = false;
        } else {
          this.isLoggedIn = true;
        }
      }
    })
  }
}
