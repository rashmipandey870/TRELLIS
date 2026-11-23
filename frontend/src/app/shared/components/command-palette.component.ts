import { CommonModule } from '@angular/common';
import { Component, ElementRef, HostListener, ViewChild, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

interface CommandItem {
  id: string;
  title: string;
  subtitle?: string;
  category: 'Navigation' | 'Actions' | 'Demo Switcher' | 'Help';
  icon?: string;
  badge?: string;
  action: () => void;
}

@Component({
  selector: 'app-command-palette',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    @if (isOpen()) {
      <div 
        class="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-slate-950/60 backdrop-blur-sm animate-in fade-in duration-150"
        (click)="closeOnBackdrop($event)">
        
        <div 
          class="w-full max-w-xl bg-white border border-slate-200 rounded-2xl shadow-2xl overflow-hidden animate-in zoom-in-95 duration-150"
          (click)="$event.stopPropagation()">
          
          <!-- Search Header -->
          <div class="flex items-center px-4 py-3.5 border-b border-slate-200 gap-3">
            <svg class="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            
            <input 
              #searchInput
              type="text"
              [(ngModel)]="searchQuery"
              placeholder="Type a command, page, or search action... (ESC to close)"
              class="flex-1 bg-transparent border-none text-sm text-slate-900 placeholder-slate-400 focus:outline-none"
              (keydown)="handleKeydown($event)" />

            <kbd class="px-2 py-0.5 text-[10px] font-semibold text-slate-500 bg-slate-100 border border-slate-200 rounded-md">
              ESC
            </kbd>
          </div>

          <!-- Command Items List -->
          <div class="max-h-80 overflow-y-auto p-2 space-y-1">
            @if (filteredCommands().length === 0) {
              <div class="py-8 text-center text-xs text-slate-400">
                No matching commands found for "{{ searchQuery }}".
              </div>
            }

            @for (cmd of filteredCommands(); track cmd.id; let idx = $index) {
              <button
                type="button"
                (click)="execute(cmd)"
                (mouseenter)="selectedIndex.set(idx)"
                class="w-full text-left px-3.5 py-2.5 rounded-xl flex items-center justify-between transition group"
                [ngClass]="selectedIndex() === idx ? 'bg-sky-50  text-[#008FBB] ' : 'text-slate-700  hover:bg-slate-50 '">
                
                <div class="flex items-center gap-3">
                  <div 
                    class="w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold"
                    [ngClass]="selectedIndex() === idx ? 'bg-[#008FBB]/10 text-[#008FBB]' : 'bg-slate-100  text-slate-500'">
                    {{ cmd.category[0] }}
                  </div>
                  <div>
                    <div class="text-xs font-semibold leading-tight flex items-center gap-2">
                      <span>{{ cmd.title }}</span>
                      @if (cmd.badge) {
                        <span class="text-[9px] px-1.5 py-0.2 rounded bg-slate-100 text-slate-500 font-normal">
                          {{ cmd.badge }}
                        </span>
                      }
                    </div>
                    @if (cmd.subtitle) {
                      <div class="text-[10px] text-slate-400 mt-0.5">{{ cmd.subtitle }}</div>
                    }
                  </div>
                </div>

                <div class="flex items-center gap-2 text-[10px] text-slate-400">
                  <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400/80">{{ cmd.category }}</span>
                  <span class="opacity-0 group-hover:opacity-100 transition">↵</span>
                </div>
              </button>
            }
          </div>

          <!-- Footer Hints -->
          <div class="px-4 py-2.5 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-[11px] text-slate-400">
            <div class="flex items-center gap-3">
              <span><kbd class="px-1 py-0.2 bg-white border rounded text-[10px]">↑</kbd> <kbd class="px-1 py-0.2 bg-white border rounded text-[10px]">↓</kbd> to navigate</span>
              <span><kbd class="px-1 py-0.2 bg-white border rounded text-[10px]">↵</kbd> to select</span>
            </div>
            <div class="flex items-center gap-1.5 font-semibold text-slate-500">
              <span class="w-1.5 h-1.5 rounded-full bg-[#008FBB]"></span>
              <span>TRELLIS Command Palette</span>
            </div>
          </div>

        </div>
      </div>
    }
  `,
})
export class CommandPaletteComponent {
  private readonly router = inject(Router);
  private readonly authService = inject(AuthService);

  @ViewChild('searchInput') searchInput?: ElementRef<HTMLInputElement>;

  readonly isOpen = signal<boolean>(false);
  readonly selectedIndex = signal<number>(0);
  searchQuery = '';

  @HostListener('window:keydown', ['$event'])
  onKeyDown(event: KeyboardEvent): void {
    // Ctrl+K or Cmd+K
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      this.toggle();
    }
    // ESC closes palette
    if (event.key === 'Escape' && this.isOpen()) {
      this.close();
    }
  }

  toggle(): void {
    if (this.isOpen()) {
      this.close();
    } else {
      this.open();
    }
  }

  open(): void {
    this.searchQuery = '';
    this.selectedIndex.set(0);
    this.isOpen.set(true);
    setTimeout(() => this.searchInput?.nativeElement.focus(), 50);
  }

  close(): void {
    this.isOpen.set(false);
  }

  closeOnBackdrop(event: MouseEvent): void {
    this.close();
  }

  handleKeydown(event: KeyboardEvent): void {
    const list = this.filteredCommands();
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      this.selectedIndex.update((i) => (i + 1) % (list.length || 1));
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      this.selectedIndex.update((i) => (i - 1 + list.length) % (list.length || 1));
    } else if (event.key === 'Enter') {
      event.preventDefault();
      if (list[this.selectedIndex()]) {
        this.execute(list[this.selectedIndex()]);
      }
    }
  }

  execute(cmd: CommandItem): void {
    this.close();
    cmd.action();
  }

  readonly allCommands = computed<CommandItem[]>(() => {
    const role = this.authService.primaryRole() || 'LEARNER';
    const commands: CommandItem[] = [];

    // Role-aware Navigation Commands
    if (role === 'ADMIN') {
      commands.push(
        { id: 'admin-dash', title: 'Admin Governance Dashboard', subtitle: 'Platform health and KPI overview', category: 'Navigation', action: () => this.router.navigate(['/admin/dashboard']) },
        { id: 'admin-users', title: 'Manage Users & Permissions', subtitle: 'User accounts, roles, OTP provisioning', category: 'Navigation', action: () => this.router.navigate(['/admin/users']) },
        { id: 'admin-batches', title: 'Manage Batches & Cohorts', subtitle: 'Engineering cohort assignment', category: 'Navigation', action: () => this.router.navigate(['/admin/batches']) },
        { id: 'admin-learners', title: 'Learner Directory & Analytics', subtitle: 'Learner roster and progression', category: 'Navigation', action: () => this.router.navigate(['/admin/learners']) },
        { id: 'admin-settings', title: 'Security Settings & Audit Logs', subtitle: 'Immutable ledger and AI configuration', category: 'Navigation', action: () => this.router.navigate(['/admin/settings']) },
      );
    } else if (role === 'MENTOR') {
      commands.push(
        { id: 'mentor-dash', title: 'Mentor Dashboard', subtitle: 'Assessment pipeline and attention queue', category: 'Navigation', action: () => this.router.navigate(['/mentor/dashboard']) },
        { id: 'mentor-meetings', title: 'Mentorship Meetings', subtitle: '1:1 syncs, workshops and office hours', category: 'Navigation', action: () => this.router.navigate(['/mentor/meetings']) },
        { id: 'mentor-assessments', title: 'Assessments Studio', subtitle: 'Question bank, publishing and grading', category: 'Navigation', action: () => this.router.navigate(['/mentor/assessments']) },
        { id: 'mentor-learners', title: 'Assigned Learners', subtitle: 'Learner Growth Ring cards and remarks', category: 'Navigation', action: () => this.router.navigate(['/mentor/learners']) },
        { id: 'mentor-spotlight', title: 'Talent Spotlight Alerts', subtitle: 'High-performing candidate recommendations', category: 'Navigation', action: () => this.router.navigate(['/mentor/spotlight']) },
      );
    } else {
      commands.push(
        { id: 'learner-dash', title: 'Learner Home Dashboard', subtitle: 'Daily progress, streaks and upcoming tests', category: 'Navigation', action: () => this.router.navigate(['/learner/dashboard']) },
        { id: 'learner-meetings', title: 'My Meetings & Schedule', subtitle: 'Upcoming 1:1s and workshops (.ics)', category: 'Navigation', action: () => this.router.navigate(['/learner/meetings']) },
        { id: 'learner-assessments', title: 'My Formal Assessments', subtitle: 'Published assessments and submission history', category: 'Navigation', action: () => this.router.navigate(['/learner/assessments']) },
        { id: 'learner-coding', title: 'LeetCode-Style Coding Lab', subtitle: 'Live Monaco editor with multi-language tests', category: 'Navigation', action: () => this.router.navigate(['/learner/coding']) },
        { id: 'learner-practice', title: 'AI Practice Drills & Dedication', subtitle: 'Procedural and verified practice questions', category: 'Navigation', action: () => this.router.navigate(['/learner/practice']) },
      );
    }

    // Quick Actions
    commands.push(
      {
        id: 'change-password',
        title: 'Change Password',
        subtitle: 'Update account credentials and password',
        category: 'Actions',
        action: () => this.router.navigate(['/auth/change-password']),
      },
      {
        id: 'sign-out',
        title: 'Sign Out',
        subtitle: 'Securely sign out of TRELLIS',
        category: 'Actions',
        action: () => this.authService.logout(),
      },
    );

    return commands;
  });

  readonly filteredCommands = computed<CommandItem[]>(() => {
    const q = this.searchQuery.trim().toLowerCase();
    const all = this.allCommands();
    if (!q) return all;
    return all.filter(
      (c) =>
        c.title.toLowerCase().includes(q) ||
        c.subtitle?.toLowerCase().includes(q) ||
        c.category.toLowerCase().includes(q)
    );
  });
}
