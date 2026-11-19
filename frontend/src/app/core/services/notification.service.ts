import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';

export interface TrellisNotification {
  id: string;
  title: string;
  message: string;
  notification_type: 'MEETING' | 'ASSESSMENT' | 'TALENT_ALERT' | 'SYSTEM' | string;
  is_read: boolean;
  link_url?: string;
  created_at: string;
}

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  private readonly http = inject(HttpClient);

  readonly notifications = signal<TrellisNotification[]>([]);
  readonly unreadCount = computed(() => this.notifications().filter((n) => !n.is_read).length);

  loadNotifications(): Observable<TrellisNotification[]> {
    return this.http.get<TrellisNotification[]>('/api/v1/notifications').pipe(
      tap((data) => this.notifications.set(data || []))
    );
  }

  markAsRead(id: string): Observable<any> {
    return this.http.post(`/api/v1/notifications/${id}/read`, {}).pipe(
      tap(() => {
        this.notifications.update((list) =>
          list.map((n) => (n.id === id ? { ...n, is_read: true } : n))
        );
      })
    );
  }

  markAllAsRead(): Observable<any> {
    return this.http.post('/api/v1/notifications/mark-all-read', {}).pipe(
      tap(() => {
        this.notifications.update((list) =>
          list.map((n) => ({ ...n, is_read: true }))
        );
      })
    );
  }
}
