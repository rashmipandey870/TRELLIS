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
    <header class="sticky top-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur border-b border-slate-200 dark:border-slate-800 shadow-sm" [attr.data-tone]="roleTone()">
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
                <span class="text-lg font-black tracking-tight text-slate-900 dark:text-white leading-none">TRELLIS</span>
                <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest mt-0.5">CSM Technologies</span>
              </div>
            </a>

            <!-- Role Tone Indicator Tag -->
            @if (currentUser()) {
              <div class="hidden sm:inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider"
                [ngClass]="{
                  'bg-rose-100 text-[#D7182A] border border-rose-300 dark:bg-rose-950/60 dark:border-rose-800': roleTone() === 'admin',
                  'bg-amber-100 text-[#FAA634] border border-amber-300 dark:bg-amber-950/60 dark:border-amber-800': roleTone() === 'mentor',
                  'bg-sky-100 text-[#008FBB] border border-sky-300 dark:bg-sky-950/60 dark:border-sky-800': roleTone() === 'learner'
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
                <a routerLink="/admin/dashboard" routerLinkActive="text-[#D7182A] bg-rose-50 dark:bg-rose-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Dashboard</a>
                <a routerLink="/admin/users" routerLinkActive="text-[#D7182A] bg-rose-50 dark:bg-rose-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Users</a>
                <a routerLink="/admin/batches" routerLinkActive="text-[#D7182A] bg-rose-50 dark:bg-rose-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Batches</a>
                <a routerLink="/admin/learners" routerLinkActive="text-[#D7182A] bg-rose-50 dark:bg-rose-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Learner Directory</a>
                <a routerLink="/admin/settings" routerLinkActive="text-[#D7182A] bg-rose-50 dark:bg-rose-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Settings &amp; Audits</a>
              } @else if (authService.isMentor()) {
                <a routerLink="/mentor/dashboard" routerLinkActive="text-[#FAA634] bg-amber-50 dark:bg-amber-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Dashboard</a>
                <a routerLink="/mentor/meetings" routerLinkActive="text-[#FAA634] bg-amber-50 dark:bg-amber-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Meetings</a>
                <a routerLink="/mentor/assessments" routerLinkActive="text-[#FAA634] bg-amber-50 dark:bg-amber-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Assessments</a>
                <a routerLink="/mentor/learners" routerLinkActive="text-[#FAA634] bg-amber-50 dark:bg-amber-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">My Learners</a>
                <a routerLink="/mentor/spotlight" routerLinkActive="text-[#FAA634] bg-amber-50 dark:bg-amber-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Talent Spotlight</a>
              } @else if (authService.isLearner()) {
                <a routerLink="/learner/dashboard" routerLinkActive="text-[#008FBB] bg-sky-50 dark:bg-sky-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Dashboard</a>
                <a routerLink="/learner/meetings" routerLinkActive="text-[#008FBB] bg-sky-50 dark:bg-sky-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">My Meetings</a>
                <a routerLink="/learner/assessments" routerLinkActive="text-[#008FBB] bg-sky-50 dark:bg-sky-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">My Assessments</a>
                <a routerLink="/learner/coding" routerLinkActive="text-[#008FBB] bg-sky-50 dark:bg-sky-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">Coding Lab</a>
                <a routerLink="/learner/practice" routerLinkActive="text-[#008FBB] bg-sky-50 dark:bg-sky-950/40" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">AI Practice</a>
              }
            </nav>
          </div>

          <!-- Actions & Right Menu -->
          <div class="flex items-center gap-3">
            
            <!-- Quick Demo Role Switcher for Testing Ease -->
            <div class="hidden lg:flex items-center gap-1 bg-slate-100 dark:bg-slate-800 p-1 rounded-lg text-[11px] font-semibold text-slate-600 dark:text-slate-300">
              <span class="px-1.5 text-slate-400">Switch:</span>
              <button (click)="quickSwitch('learner1@csmtech.internal')" class="px-2 py-0.5 rounded hover:bg-white dark:hover:bg-slate-700 hover:text-[#008FBB] transition">Learner</button>
              <button (click)="quickSwitch('mentor1@csmtech.internal')" class="px-2 py-0.5 rounded hover:bg-white dark:hover:bg-slate-700 hover:text-[#FAA634] transition">Mentor</button>
              <button (click)="quickSwitch('admin@csmtech.internal')" class="px-2 py-0.5 rounded hover:bg-white dark:hover:bg-slate-700 hover:text-[#D7182A] transition">Admin</button>
            </div>

            <!-- Notifications Bell -->
            <div class="relative">
              <button 
                type="button" 
                (click)="toggleNotifications()"
                class="relative p-2 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 transition">
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
                <div class="absolute right-0 mt-2 w-80 bg-white dark:bg-slate-900 rounded-xl shadow-2xl border border-slate-200 dark:border-slate-800 p-3 z-50">
                  <div class="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">Notifications</span>
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
                        [ngClass]="item.is_read ? 'bg-slate-50 dark:bg-slate-800/50 text-slate-500' : 'bg-sky-50 dark:bg-sky-950/40 text-slate-800 dark:text-slate-100 font-medium border-l-2 border-[#008FBB]'">
                        <p class="font-bold text-[11px]">{{ item.title }}</p>
                        <p class="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5 line-clamp-2">{{ item.message }}</p>
                      </div>
                    } @empty {
                      <p class="text-xs text-center text-slate-400 py-4">No notifications yet.</p>
                    }
                  </div>
                </div>
              }
            </div>

            <!-- User Profile & Sign Out -->
            <div class="flex items-center gap-2 pl-2 border-l border-slate-200 dark:border-slate-800">
              <div class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center font-bold text-xs text-slate-700 dark:text-slate-200">
                {{ initials() }}
              </div>
              <div class="hidden sm:flex flex-col text-left">
                <span class="text-xs font-bold text-slate-800 dark:text-slate-100 leading-tight">{{ currentUser()?.fullName || 'User' }}</span>
                <span class="text-[10px] text-slate-400 leading-none">{{ currentUser()?.email }}</span>
              </div>
              <button 
                type="button" 
                (click)="authService.logout()"
                title="Sign Out"
                class="ml-2 p-1.5 rounded-lg text-slate-400 hover:text-[#D7182A] hover:bg-rose-50 dark:hover:bg-rose-950/40 transition">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
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
  }

  quickSwitch(email: string): void {
    this.authService.login(email, 'CSMTrellis2026!').subscribe({
      next: () => {
        const dest = this.authService.getRoleRedirectPath();
        this.router.navigate([dest]);
      },
    });
  }
}
