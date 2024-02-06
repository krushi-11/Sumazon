import { HttpClient } from "@angular/common/http";
import { Injectable, inject } from "@angular/core";
import { Observable, map } from "rxjs";

@Injectable()
export class AuthService {
    private readonly http = inject(HttpClient);

    login(payload: any): Observable<any> {
        const { username, password } = payload;
        return this.http.post('http://localhost:8000/login', { username, password });
    }

    logout(): Observable<any> {
        return this.http.get('http://localhost:8000/logout')
    }

    getCurrentUser(): Observable<any> {
        return this.http.get('http://localhost:8000/profile')
    }

    isAdminUser(): Observable<boolean> {
        return this.http.get('http://localhost:8000/profile').pipe(map((res: any) => res.is_admin))
    }

    getUsers(): Observable<any> {
        return this.http.get('http://localhost:8000/users')
    }
}