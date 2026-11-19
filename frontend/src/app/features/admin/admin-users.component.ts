import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AdminService, UserSummary } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-users',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">User Management</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Provision, manage, and govern accounts across ADMIN, MENTOR, and LEARNER roles.
          </p>
        </div>
        <div class="flex items-center gap-2">
          <button 
            type="button" 
            (click)="showBulkImportModal.set(true)"
            class="px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-xs font-bold text-slate-700 dark:text-slate-200 transition">
            &uarr; CSV Bulk Import
          </button>
          <button 
            type="button" 
            (click)="openAddUserModal()"
            class="px-3.5 py-2 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-xs font-bold text-white transition shadow-sm">
            + Add New User
          </button>
        </div>
      </div>

      <!-- Filters & Search Bar -->
      <div class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div class="w-full sm:w-72">
          <input 
            type="text" 
            [(ngModel)]="searchQuery" 
            (ngModelChange)="applyFilters()"
            placeholder="Search by name or email..."
            class="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-[#008FBB]" />
        </div>

        <div class="flex items-center gap-2 w-full sm:w-auto">
          <span class="text-xs text-slate-400 font-semibold">Filter Role:</span>
          <select 
            [(ngModel)]="selectedRole" 
            (ngModelChange)="applyFilters()"
            class="px-3 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-[#008FBB]">
            <option value="">All Roles (3 Only)</option>
            <option value="ADMIN">ADMIN</option>
            <option value="MENTOR">MENTOR</option>
            <option value="LEARNER">LEARNER</option>
          </select>
        </div>
      </div>

      <!-- Users Table -->
      <div class="rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-50 dark:bg-slate-800/60 text-[10px] font-bold uppercase tracking-wider text-slate-400 border-b border-slate-200 dark:border-slate-800">
              <tr>
                <th class="py-3 px-4">User</th>
                <th class="py-3 px-4">Role</th>
                <th class="py-3 px-4">Status</th>
                <th class="py-3 px-4">Streak</th>
                <th class="py-3 px-4">Created Date</th>
                <th class="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              @for (user of filteredUsers(); track user.id) {
                <tr class="hover:bg-slate-50/50 dark:hover:bg-slate-800/40 transition">
                  <td class="py-3 px-4">
                    <div class="font-bold text-slate-900 dark:text-white">{{ user.full_name }}</div>
                    <div class="text-[11px] text-slate-400">{{ user.email }}</div>
                  </td>
                  <td class="py-3 px-4">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase"
                      [ngClass]="{
                        'bg-rose-100 text-[#D7182A] border border-rose-300': user.role === 'ADMIN',
                        'bg-amber-100 text-[#FAA634] border border-amber-300': user.role === 'MENTOR',
                        'bg-sky-100 text-[#008FBB] border border-sky-300': user.role === 'LEARNER'
                      }">
                      {{ user.role }}
                    </span>
                  </td>
                  <td class="py-3 px-4">
                    <span class="inline-flex items-center gap-1.5 text-xs font-semibold" [ngClass]="user.is_active ? 'text-emerald-600' : 'text-slate-400'">
                      <span class="w-1.5 h-1.5 rounded-full" [ngClass]="user.is_active ? 'bg-emerald-500' : 'bg-slate-400'"></span>
                      {{ user.is_active ? 'Active' : 'Deactivated' }}
                    </span>
                  </td>
                  <td class="py-3 px-4 font-mono font-bold text-slate-700 dark:text-slate-300">
                    {{ user.streak_days || 0 }}d
                  </td>
                  <td class="py-3 px-4 text-slate-400">
                    {{ user.created_at ? (user.created_at | date:'mediumDate') : 'Pre-seeded' }}
                  </td>
                  <td class="py-3 px-4 text-right space-x-2">
                    @if (user.is_active) {
                      <button 
                        (click)="deactivateUser(user)"
                        class="text-xs text-rose-500 hover:text-rose-700 font-semibold transition">
                        Deactivate
                      </button>
                    } @else {
                      <span class="text-xs text-slate-400">Disabled</span>
                    }
                  </td>
                </tr>
              } @empty {
                <tr>
                  <td colspan="6" class="py-8 text-center text-slate-400">
                    No users matching criteria.
                  </td>
                </tr>
              }
            </tbody>
          </table>
        </div>
      </div>

      <!-- Add User Modal -->
      @if (showAddUserModal()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-md w-full p-6 space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">Create New User</h3>
              <button (click)="showAddUserModal.set(false)" class="text-slate-400 hover:text-slate-600">&times;</button>
            </div>

            <form (ngSubmit)="submitCreateUser()" class="space-y-3">
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-1">Full Name</label>
                <input type="text" [(ngModel)]="newUser.full_name" name="name" required class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs" />
              </div>
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-1">Corporate Email</label>
                <input type="email" [(ngModel)]="newUser.email" name="email" required class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs" />
              </div>
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-1">Role (Strict 3 Roles)</label>
                <select [(ngModel)]="newUser.role" name="role" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs">
                  <option value="LEARNER">LEARNER</option>
                  <option value="MENTOR">MENTOR</option>
                  <option value="ADMIN">ADMIN</option>
                </select>
              </div>

              <div class="flex justify-end gap-2 pt-4">
                <button type="button" (click)="showAddUserModal.set(false)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-600 dark:text-slate-300">Cancel</button>
                <button type="submit" class="px-4 py-2 rounded-xl bg-[#008FBB] text-xs font-bold text-white hover:bg-[#007499]">Create Account</button>
              </div>
            </form>
          </div>
        </div>
      }

      <!-- CSV Bulk Import Modal -->
      @if (showBulkImportModal()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-lg w-full p-6 space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">CSV Bulk Import Users</h3>
              <button (click)="showBulkImportModal.set(false)" class="text-slate-400 hover:text-slate-600">&times;</button>
            </div>

            <p class="text-xs text-slate-500 dark:text-slate-400">
              Paste standard comma-separated lines. Format: <code class="font-mono bg-slate-100 dark:bg-slate-800 px-1 py-0.5 rounded text-[11px]">email,full_name,role</code>
            </p>

            <textarea 
              [(ngModel)]="bulkCsvContent" 
              rows="6" 
              placeholder="priya.verma@csmtech.internal,Priya Verma,LEARNER&#10;amit.sharma@csmtech.internal,Amit Sharma,MENTOR"
              class="w-full font-mono text-xs p-3 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-1 focus:ring-[#008FBB]"></textarea>

            @if (bulkImportMessage()) {
              <div class="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-200 text-xs font-bold">
                {{ bulkImportMessage() }}
              </div>
            }

            <div class="flex justify-end gap-2 pt-2">
              <button type="button" (click)="showBulkImportModal.set(false)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-600 dark:text-slate-300">Close</button>
              <button type="button" (click)="submitBulkImport()" [disabled]="!bulkCsvContent.trim()" class="px-4 py-2 rounded-xl bg-[#008FBB] text-xs font-bold text-white hover:bg-[#007499] disabled:opacity-50">Run Import</button>
            </div>
          </div>
        </div>
      }
    </div>
  `,
})
export class AdminUsersComponent {
  private readonly adminService = inject(AdminService);

  readonly users = signal<UserSummary[]>([]);
  readonly filteredUsers = signal<UserSummary[]>([]);

  searchQuery = '';
  selectedRole = '';

  readonly showAddUserModal = signal<boolean>(false);
  readonly showBulkImportModal = signal<boolean>(false);
  readonly bulkImportMessage = signal<string | null>(null);
  bulkCsvContent = '';

  newUser = {
    full_name: '',
    email: '',
    role: 'LEARNER',
  };

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.adminService.getUsers().subscribe({
      next: (list) => {
        this.users.set(list || []);
        this.applyFilters();
      },
      error: () => {},
    });
  }

  applyFilters(): void {
    const q = this.searchQuery.toLowerCase();
    const r = this.selectedRole.toUpperCase();
    const result = this.users().filter((u) => {
      const matchQ = !q || u.full_name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q);
      const matchR = !r || (u.role || '').toUpperCase() === r;
      return matchQ && matchR;
    });
    this.filteredUsers.set(result);
  }

  openAddUserModal(): void {
    this.newUser = { full_name: '', email: '', role: 'LEARNER' };
    this.showAddUserModal.set(true);
  }

  submitCreateUser(): void {
    this.adminService.createUser(this.newUser).subscribe({
      next: () => {
        this.showAddUserModal.set(false);
        this.loadUsers();
      },
    });
  }

  deactivateUser(user: UserSummary): void {
    if (confirm(`Deactivate user account ${user.full_name}?`)) {
      this.adminService.deactivateUser(user.id).subscribe({
        next: () => this.loadUsers(),
      });
    }
  }

  submitBulkImport(): void {
    this.adminService.bulkImportUsers(this.bulkCsvContent).subscribe({
      next: (res) => {
        this.bulkImportMessage.set(`Successfully created ${res.created} user account(s).`);
        this.bulkCsvContent = '';
        this.loadUsers();
      },
    });
  }
}
