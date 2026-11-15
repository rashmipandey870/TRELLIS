import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { FreezeStreakResponseDto, HomeDashboardDto } from '../models/home.models';

@Injectable({
  providedIn: 'root',
})
export class HomeService {
  private readonly http = inject(HttpClient);

  /**
   * Fetch complete personalised home dashboard telemetry computed from real database state.
   */
  getHomeDashboard(): Observable<HomeDashboardDto> {
    return this.http.get<HomeDashboardDto>('/api/v1/home');
  }

  /**
   * Consume one streak freeze in a transactionally audited mutation.
   */
  freezeStreak(): Observable<FreezeStreakResponseDto> {
    return this.http.post<FreezeStreakResponseDto>('/api/v1/home/freeze-streak', {});
  }
}
