import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { NotificationService } from '../../core/services/notification.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <header class="sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-slate-200 shadow-sm" [attr.data-tone]="roleTone()">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          
          <!-- Logo & Brand -->
          <div class="flex items-center gap-6">
            <a routerLink="/" class="flex items-center gap-2.5 focus:outline-none">
              <!-- CSM Technologies Stylized Cut-Corner Badge -->
              <div class="w-9 h-9 rounded-lg bg-gradient-to-tr from-[#FAA634] via-[#D7182A] to-[#008FBB] flex items-center justify-center shadow-sm">
                <span class="text-white font-black text-lg tracking-tighter">T</span>
              </div>
              <div class="flex flex-col">
                <span class="text-lg font-black tracking-tight text-slate-900 leading-none">TRELLIS</span>
                <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest mt-0.5">CSM Technologies</span>
              </div>
            </a>

            <!-- Role Tone Indicator Tag -->
            @if (currentUser()) {
              <div class="hidden sm:inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider"
                [ngClass]="{
                  'bg-rose-100 text-[#D7182A] border border-rose-300': roleTone() === 'admin',
                  'bg-amber-100 text-[#FAA634] border border-amber-300': roleTone() === 'mentor',
                  'bg-sky-100 text-[#008FBB] border border-sky-300': roleTone() === 'learner'
                }">
                <span class="w-1.5 h-1.5 rounded-full mr-1.5 animate-pulse"
                  [ngClass]="{
                    'bg-[#D7182A]': roleTone() === 'admin',
                    'bg-[#FAA634]': roleTone() === 'mentor',
                    'bg-[#008FBB]': roleTone() === 'learner'
                  }"></span>
                {{ currentUser()?.role || 'LEARNER' }} PORTAL
              </div>
            }

            <!-- Navigation Links according to Role -->
            <nav class="hidden md:flex items-center gap-1">
              @if (authService.isAdmin()) {
                <a routerLink="/admin/dashboard" routerLinkActive="text-[#D7182A] bg-rose-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Dashboard</a>
                <a routerLink="/admin/users" routerLinkActive="text-[#D7182A] bg-rose-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Users</a>
                <a routerLink="/admin/batches" routerLinkActive="text-[#D7182A] bg-rose-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Batches</a>
                <a routerLink="/admin/learners" routerLinkActive="text-[#D7182A] bg-rose-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Learner Directory</a>
                <a routerLink="/admin/settings" routerLinkActive="text-[#D7182A] bg-rose-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Settings &amp; Audits</a>
              } @else if (authService.isMentor()) {
                <a routerLink="/mentor/dashboard" routerLinkActive="text-[#FAA634] bg-amber-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Dashboard</a>
                <a routerLink="/mentor/meetings" routerLinkActive="text-[#FAA634] bg-amber-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Meetings</a>
                <a routerLink="/mentor/assessments" routerLinkActive="text-[#FAA634] bg-amber-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Assessments</a>
                <a routerLink="/mentor/learners" routerLinkActive="text-[#FAA634] bg-amber-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">My Learners</a>
                <a routerLink="/mentor/spotlight" routerLinkActive="text-[#FAA634] bg-amber-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Talent Spotlight</a>
              } @else if (authService.isLearner()) {
                <a routerLink="/learner/dashboard" routerLinkActive="text-[#008FBB] bg-sky-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Dashboard</a>
                <a routerLink="/learner/meetings" routerLinkActive="text-[#008FBB] bg-sky-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Meetings</a>
                <a routerLink="/learner/assessments" routerLinkActive="text-[#008FBB] bg-sky-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Assessments</a>
                <a routerLink="/learner/results" routerLinkActive="text-[#008FBB] bg-sky-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Results &amp; Analytics</a>
                <a routerLink="/learner/coding" routerLinkActive="text-[#008FBB] bg-sky-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">Coding Lab</a>
                <a routerLink="/learner/practice" routerLinkActive="text-[#008FBB] bg-sky-50" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 transition">AI Practice</a>
              }
            </nav>
          </div>

          <!-- Actions & Right Menu -->
          <div class="flex items-center gap-3">
            
            <!-- Global Search Quick Trigger (Ctrl+K / Cmd+K) -->
            <button 
              type="button" 
              (click)="triggerSearch()"
              class="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200/80 text-xs text-slate-500 font-medium transition border border-slate-200">
              <svg class="w-3.5 h-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span>Search or jump to...</span>
              <kbd class="px-1.5 py-0.5 text-[10px] font-mono bg-white border border-slate-300 rounded shadow-xs text-slate-400">Ctrl+K</kbd>
            </button>

            <!-- Notifications Bell -->
            <div class="relative">
              <button 
                type="button" 
                (click)="toggleNotifications()"
                class="relative p-2 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition">
                <span class="sr-only">View notifications</span>
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                @if (unreadCount() > 0) {
                  <span class="absolute top-1.5 right-1.5 flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#D7182A] opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-[#D7182A]"></span>
                  </span>
                }
              </button>

              <!-- Notifications Dropdown -->
              @if (showNotifications()) {
                <div class="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-2xl border border-slate-200 p-3 z-50">
                  <div class="flex items-center justify-between pb-2 border-b border-slate-100 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider text-slate-700">Notifications</span>
                    @if (unreadCount() > 0) {
                      <button (click)="notificationService.markAllAsRead().subscribe()" class="text-[10px] text-[#008FBB] hover:underline font-semibold">
                        Mark all as read
                      </button>
                    }
                  </div>
                  <div class="max-h-64 overflow-y-auto space-y-2">
                    @for (item of notificationService.notifications(); track item.id) {
                      <div 
                        (click)="notificationService.markAsRead(item.id).subscribe()"
                        class="p-2 rounded-lg text-xs cursor-pointer transition"
                        [ngClass]="item.is_read ? 'bg-slate-50 text-slate-500' : 'bg-sky-50 text-slate-800 font-medium border-l-2 border-[#008FBB]'">
                        <p class="font-bold text-[11px]">{{ item.title }}</p>
                        <p class="text-[10px] text-slate-500 mt-0.5 line-clamp-2">{{ item.message }}</p>
                      </div>
                    } @empty {
                      <p class="text-xs text-center text-slate-400 py-4">No notifications yet.</p>
                    }
                  </div>
                </div>
              }
            </div>

            <!-- User Menu with Initials, Role Badge & Dropdown (Phase A2) -->
            <div class="relative pl-2 border-l border-slate-200">
              <button 
                type="button" 
                (click)="toggleUserMenu()"
                class="flex items-center gap-2 p-1 rounded-xl hover:bg-slate-100 transition focus:outline-none focus:ring-2 focus:ring-[#008FBB]">
                <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-[#008FBB] to-[#FAA634] text-white flex items-center justify-center font-bold text-xs shadow-xs">
                  {{ initials() }}
                </div>
                <div class="hidden sm:flex flex-col text-left">
                  <span class="text-xs font-bold text-slate-800 leading-tight">{{ currentUser()?.fullName || 'User' }}</span>
                  <span class="text-[10px] text-slate-400 leading-none">{{ currentUser()?.role || 'LEARNER' }}</span>
                </div>
                <svg class="w-3.5 h-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              @if (showUserMenu()) {
                <div class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-2xl border border-slate-200 py-2 z-50">
                  <div class="px-4 py-2 border-b border-slate-100 mb-1">
                    <p class="text-xs font-bold text-slate-800">{{ currentUser()?.fullName }}</p>
                    <p class="text-[11px] text-slate-400 truncate">{{ currentUser()?.email }}</p>
                    <span class="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-600">
                      {{ currentUser()?.role }}
                    </span>
                  </div>

                  <a routerLink="/auth/change-password" (click)="closeUserMenu()" class="flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-slate-50 transition">
                    <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                    </svg>
                    Profile &amp; Credentials
                  </a>

                  <button type="button" (click)="triggerSearch(); closeUserMenu()" class="w-full text-left flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-slate-50 transition">
                    <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Help &amp; Shortcuts
                  </button>

                  <div class="border-t border-slate-100 my-1"></div>

                  <button 
                    type="button" 
                    (click)="authService.logout(); closeUserMenu()"
                    class="w-full text-left flex items-center gap-2 px-4 py-2 text-xs text-[#D7182A] hover:bg-rose-50 font-semibold transition">
                    <svg class="w-4 h-4 text-[#D7182A]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Sign Out
                  </button>
                </div>
              }
            </div>

          </div>

        </div>
      </div>
    </header>
  `,
})
export class HeaderComponent {
  readonly authService = inject(AuthService);
  readonly notificationService = inject(NotificationService);
  private readonly router = inject(Router);

  readonly showNotifications = signal<boolean>(false);
  readonly showUserMenu = signal<boolean>(false);

  readonly currentUser = this.authService.currentUser;
  readonly unreadCount = this.notificationService.unreadCount;

  readonly roleTone = computed(() => {
    const role = (this.currentUser()?.role || '').toLowerCase();
    if (role === 'admin') return 'admin';
    if (role === 'mentor') return 'mentor';
    return 'learner';
  });

  readonly initials = computed(() => {
    const name = this.currentUser()?.fullName || 'User';
    return name.split(' ').map((n) => n[0]).slice(0, 2).join('').toUpperCase();
  });

  ngOnInit(): void {
    if (this.authService.isAuthenticated()) {
      this.notificationService.loadNotifications().subscribe();
    }
  }

  toggleNotifications(): void {
    this.showNotifications.update((v) => !v);
    this.showUserMenu.set(false);
  }

  toggleUserMenu(): void {
    this.showUserMenu.update((v) => !v);
    this.showNotifications.set(false);
  }

  closeUserMenu(): void {
    this.showUserMenu.set(false);
  }

  triggerSearch(): void {
    // Trigger keyboard event for Ctrl+K to open Command Palette
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'k', ctrlKey: true }));
  }
}
