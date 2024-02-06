import { HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { ToastrService } from 'ngx-toastr';
import { tap } from 'rxjs';


export const httpInterceptorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const toastr = inject(ToastrService);

  if (req.url.indexOf('login') > -1) {
    return next(req);
  } else {
    const cs = inject(CookieService);
    const token = cs.get('token');
    const cloned = req.clone({
      headers: req.headers.set('Authorization', `Bearer ${token}`)
    });
    return next(cloned).pipe(
      tap({
        next: (e: any) => {
          if (e instanceof HttpRequest && e.body['message']) {
            toastr.success(e.body['message'])
          }
        },
        error: (err) => {
          if (err.status === 401 || err.status === 403) {
            toastr.error(err.body.message);
            router.navigate(['/']);
          }
        }
      })
    );
  }
};
