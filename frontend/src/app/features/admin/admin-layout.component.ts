import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { NavigationEnd, Router, RouterModule } from '@angular/router';
import { filter } from 'rxjs';
import { AuthService } from '../../core/services/auth.service';
import { NotificationService } from '../../core/services/notification.service';
import { AssistantComponent } from '../../shared/assistant/assistant.component';

interface NavItem {
  label: string;
  route: string;
  icon: string;
  badge?: string;
}

interface NavSection {
  title: string;
  items: NavItem[];
}

@Component({
  selector: 'app-admin-layout',
  standalone: true,
  imports: [CommonModule, RouterModule, AssistantComponent],
  template: `
    <div class="min-h-screen bg-slate-50 flex font-sans antialiased">
      
      <!-- Collapsible Left Sidebar (Signal Red Admin Tone) -->
      <aside 
        class="bg-white border-r border-slate-200 transition-all duration-300 flex flex-col z-30 shrink-0 sticky top-0 h-screen shadow-xs select-none"
        [ngClass]="sidebarCollapsed() ? 'w-20' : 'w-64'">
        
        <!-- Sidebar Brand Header -->
        <div class="h-16 flex items-center justify-between px-4 border-b border-slate-200">
          <a routerLink="/admin/dashboard" class="flex items-center gap-3 overflow-hidden focus:outline-none">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-[#D7182A] via-[#FAA634] to-[#008FBB] flex items-center justify-center shrink-0 shadow-sm">
              <span class="text-white font-black text-lg">T</span>
            </div>
            @if (!sidebarCollapsed()) {
              <div class="flex flex-col truncate">
                <span class="text-base font-black tracking-tight text-slate-900 leading-none">TRELLIS</span>
                <span class="text-[9px] font-bold text-[#D7182A] uppercase tracking-widest mt-0.5">Admin Oversight</span>
              </div>
            }
          </a>
          
          <button 
            type="button"
            (click)="toggleSidebar()"
            class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition focus:outline-none"
            [title]="sidebarCollapsed() ? 'Expand Sidebar' : 'Collapse Sidebar'">
            <svg class="w-4 h-4 transition-transform duration-200" [ngClass]="sidebarCollapsed() ? 'rotate-180' : ''" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
            </svg>
          </button>
        </div>

        <!-- Navigation Section List -->
        <div class="flex-1 overflow-y-auto px-3 py-4 space-y-6">
          @for (sec of sections; track sec.title) {
            <div class="space-y-1">
              @if (!sidebarCollapsed()) {
                <span class="px-3 text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-2">
                  {{ sec.title }}
                </span>
              }
              @for (item of sec.items; track item.route) {
                <a 
                  [routerLink]="item.route" 
                  routerLinkActive="bg-rose-50 text-[#D7182A] font-bold shadow-2xs border-l-4 border-[#D7182A]"
                  [routerLinkActiveOptions]="{ exact: item.route === '/admin/dashboard' }"
                  class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition group relative"
                  [title]="sidebarCollapsed() ? item.label : ''">
                  <span class="text-base shrink-0 group-hover:scale-110 transition-transform">{{ item.icon }}</span>
                  @if (!sidebarCollapsed()) {
                    <span class="truncate">{{ item.label }}</span>
                    @if (item.badge) {
                      <span class="ml-auto px-1.5 py-0.5 rounded text-[9px] font-bold bg-rose-100 text-[#D7182A]">
                        {{ item.badge }}
                      </span>
                    }
                  }
                </a>
              }
            </div>
          }
        </div>

        <!-- Footer / Current Admin User Pill -->
        <div class="p-3 border-t border-slate-200 bg-slate-50/50">
          <div class="flex items-center gap-3 p-2 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
            <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-[#D7182A] to-[#FAA634] text-white flex items-center justify-center font-bold text-xs shrink-0 shadow-xs">
              {{ initials() }}
            </div>
            @if (!sidebarCollapsed()) {
              <div class="truncate flex-1">
                <p class="text-xs font-bold text-slate-900 truncate leading-tight">{{ currentUser()?.fullName || 'Administrator' }}</p>
                <p class="text-[10px] text-slate-400 font-mono truncate">{{ currentUser()?.email }}</p>
              </div>
            }
          </div>
        </div>

      </aside>

      <!-- Main Column -->
      <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
        
        <!-- Top Navigation Bar -->
        <header class="h-16 bg-white/95 backdrop-blur border-b border-slate-200 sticky top-0 z-20 flex items-center justify-between px-4 sm:px-6 shadow-2xs">
          
          <!-- Left: Breadcrumbs -->
          <div class="flex items-center gap-2 text-xs">
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase bg-rose-50 text-[#D7182A] border border-rose-200 flex items-center gap-1.5 shadow-2xs">
              <span class="w-1.5 h-1.5 rounded-full bg-[#D7182A] animate-pulse"></span>
              Admin Console
            </span>
            <span class="text-slate-300">/</span>
            <span class="font-bold text-slate-700 capitalize">{{ currentSectionName() }}</span>
          </div>

          <!-- Right: Actions, Palette Trigger & User Menu -->
          <div class="flex items-center gap-3">
            
            <!-- Global Search Palette Trigger -->
            <button 
              type="button" 
              (click)="triggerSearch()"
              class="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200/80 text-xs text-slate-500 font-medium transition border border-slate-200">
              <svg class="w-3.5 h-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span>Search or jump to...</span>
              <kbd class="px-1.5 py-0.5 text-[10px] font-mono bg-white border border-slate-300 rounded text-slate-400">Ctrl+K</kbd>
            </button>

            <!-- Notifications Bell -->
            <div class="relative">
              <button 
                type="button" 
                (click)="toggleNotifications()"
                class="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition relative focus:outline-none">
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

              @if (showNotifications()) {
                <div class="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-2xl border border-slate-200 p-3 z-50 animate-in fade-in">
                  <div class="flex items-center justify-between pb-2 border-b border-slate-100 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider text-slate-700">Governance Notifications</span>
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
                        class="p-2.5 rounded-xl text-xs cursor-pointer transition"
                        [ngClass]="item.is_read ? 'bg-slate-50 text-slate-500' : 'bg-rose-50/50 text-slate-800 font-medium border-l-2 border-[#D7182A]'">
                        <p class="font-bold text-[11px]">{{ item.title }}</p>
                        <p class="text-[10px] text-slate-500 mt-0.5 line-clamp-2">{{ item.message }}</p>
                      </div>
                    } @empty {
                      <p class="text-xs text-center text-slate-400 py-6">No notifications yet.</p>
                    }
                  </div>
                </div>
              }
            </div>

            <!-- User Menu -->
            <div class="relative pl-2 border-l border-slate-200">
              <button 
                type="button" 
                (click)="toggleUserMenu()"
                class="flex items-center gap-2 p-1 rounded-xl hover:bg-slate-100 transition focus:outline-none">
                <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-[#D7182A] to-[#FAA634] text-white flex items-center justify-center font-bold text-xs shadow-xs">
                  {{ initials() }}
                </div>
                <span class="hidden sm:inline text-xs font-bold text-slate-800">{{ currentUser()?.fullName }}</span>
                <svg class="w-3.5 h-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              @if (showUserMenu()) {
                <div class="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-2xl border border-slate-200 py-2 z-50 animate-in fade-in">
                  <div class="px-4 py-2 border-b border-slate-100 mb-1">
                    <p class="text-xs font-bold text-slate-800">{{ currentUser()?.fullName }}</p>
                    <p class="text-[11px] text-slate-400 truncate">{{ currentUser()?.email }}</p>
                    <span class="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-rose-100 text-[#D7182A]">
                      ADMINISTRATOR
                    </span>
                  </div>

                  <a routerLink="/auth/change-password" (click)="closeUserMenu()" class="flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-slate-50 transition">
                    Profile &amp; Credentials
                  </a>

                  <div class="border-t border-slate-100 my-1"></div>

                  <button 
                    type="button" 
                    (click)="authService.logout(); closeUserMenu()"
                    class="w-full text-left flex items-center gap-2 px-4 py-2 text-xs text-[#D7182A] hover:bg-rose-50 font-semibold transition">
                    Sign Out
                  </button>
                </div>
              }
            </div>

          </div>
        </header>

        <!-- Main Body -->
        <main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <router-outlet />
        </main>

        <app-assistant />
      </div>

    </div>
  `,
})
export class AdminLayoutComponent {
  readonly authService = inject(AuthService);
  readonly notificationService = inject(NotificationService);
  private readonly router = inject(Router);

  readonly sidebarCollapsed = signal<boolean>(false);
  readonly showNotifications = signal<boolean>(false);
  readonly showUserMenu = signal<boolean>(false);
  readonly currentUrl = signal<string>(this.router.url);

  readonly currentUser = computed(() => this.authService.currentUser());
  readonly unreadCount = computed(() => this.notificationService.unreadCount());
  readonly initials = computed(() => {
    const name = this.currentUser()?.fullName || 'Admin User';
    return name.split(' ').map((n) => n[0]).join('').slice(0, 2).toUpperCase();
  });

  readonly currentSectionName = computed(() => {
    const url = this.currentUrl();
    if (url.includes('users')) return 'User Provisioning & Roles';
    if (url.includes('batches')) return 'Cohort Batches & Caseloads';
    if (url.includes('learners')) return 'Learner Directory & Analytics';
    if (url.includes('settings')) return 'Governance & Audit Logs';
    return 'Department Overview';
  });

  readonly sections: NavSection[] = [
    {
      title: 'Overview',
      items: [
        { label: 'Executive Dashboard', route: '/admin/dashboard', icon: '📊' },
      ],
    },
    {
      title: 'People & Cohorts',
      items: [
        { label: 'User Directory', route: '/admin/users', icon: '👥' },
        { label: 'Cohort Batches', route: '/admin/batches', icon: '🏛️' },
        { label: 'Learner Directory', route: '/admin/learners', icon: '🎓' },
      ],
    },
    {
      title: 'Governance & Platform',
      items: [
        { label: 'Settings & Audits', route: '/admin/settings', icon: '⚙️' },
      ],
    },
  ];

  constructor() {
    this.router.events
      .pipe(filter((event) => event instanceof NavigationEnd))
      .subscribe((event: any) => {
        this.currentUrl.set(event.urlAfterRedirects || event.url);
        this.showNotifications.set(false);
        this.showUserMenu.set(false);
      });
  }

  toggleSidebar(): void {
    this.sidebarCollapsed.set(!this.sidebarCollapsed());
  }

  toggleNotifications(): void {
    this.showNotifications.set(!this.showNotifications());
    this.showUserMenu.set(false);
  }

  toggleUserMenu(): void {
    this.showUserMenu.set(!this.showUserMenu());
    this.showNotifications.set(false);
  }

  closeUserMenu(): void {
    this.showUserMenu.set(false);
  }

  triggerSearch(): void {
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'k', ctrlKey: true }));
  }
}
