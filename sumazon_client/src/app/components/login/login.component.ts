import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { AuthService } from '../../services/auth.service';

export interface LoginForm {
  username: FormControl<string>;
  password: FormControl<string>;
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, MatFormFieldModule, MatInputModule, MatIconModule, MatButtonModule],
  providers: [AuthService, CookieService],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  as = inject(AuthService);
  cs = inject(CookieService);
  router = inject(Router);

  hide: boolean = true;
  loginFg: FormGroup<LoginForm>;

  constructor() {
    this.loginFg = new FormGroup({
      username: new FormControl(),
      password: new FormControl()
    });
  }

  login(): void {
    this.as.login(this.loginFg.value).subscribe((r) => {
      if (r.token) {
        this.cs.set('token', r.token);
        this.router.navigate(['/product-list'])
      }
    })
  }
}
