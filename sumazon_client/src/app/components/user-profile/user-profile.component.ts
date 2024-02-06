import { Component, inject } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [],
  providers: [AuthService],
  templateUrl: './user-profile.component.html',
  styleUrl: './user-profile.component.scss'
})
export class UserProfileComponent {
  as = inject(AuthService);

  ngOnInit(): void {
    this.as.getUsers().subscribe((r)=> {})
  }

}
