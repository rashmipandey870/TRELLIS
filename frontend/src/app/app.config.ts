import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { Routes, provideRouter } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';
import { authInterceptor } from './core/interceptors/auth.interceptor';
import { LoginComponent } from './features/auth/login.component';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/landing/csm-landing.component').then((m) => m.CsmLandingComponent),
    pathMatch: 'full',
  },
  { path: 'login', component: LoginComponent },

  // ADMIN Routes (Governed by authGuard + roleGuard: ADMIN only)
  {
    path: 'admin',
    loadComponent: () =>
      import('./features/admin/admin-layout.component').then((m) => m.AdminLayoutComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['ADMIN'] },
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/admin/admin-dashboard.component').then((m) => m.AdminDashboardComponent),
      },
      {
        path: 'users',
        loadComponent: () =>
          import('./features/admin/admin-users.component').then((m) => m.AdminUsersComponent),
      },
      {
        path: 'batches',
        loadComponent: () =>
          import('./features/admin/admin-batches.component').then((m) => m.AdminBatchesComponent),
      },
      {
        path: 'learners',
        loadComponent: () =>
          import('./features/admin/admin-learners.component').then((m) => m.AdminLearnersComponent),
      },
      {
        path: 'settings',
        loadComponent: () =>
          import('./features/admin/admin-settings.component').then((m) => m.AdminSettingsComponent),
      },
    ],
  },

  // MENTOR Routes (Governed by authGuard + roleGuard: MENTOR only)
  {
    path: 'mentor',
    loadComponent: () =>
      import('./features/mentor/mentor-layout.component').then((m) => m.MentorLayoutComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['MENTOR'] },
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/mentor/mentor-dashboard.component').then((m) => m.MentorDashboardComponent),
      },
      {
        path: 'meetings',
        loadComponent: () =>
          import('./features/mentor/mentor-meetings.component').then((m) => m.MentorMeetingsComponent),
      },
      {
        path: 'assessments',
        loadComponent: () =>
          import('./features/mentor/mentor-assessments.component').then((m) => m.MentorAssessmentsComponent),
      },
      {
        path: 'learners',
        loadComponent: () =>
          import('./features/mentor/mentor-learners.component').then((m) => m.MentorLearnersComponent),
      },
      {
        path: 'spotlight',
        loadComponent: () =>
          import('./features/mentor/mentor-spotlight.component').then((m) => m.MentorSpotlightComponent),
      },
    ],
  },

  // LEARNER Routes (Governed by authGuard + roleGuard: LEARNER only)
  {
    path: 'learner',
    loadComponent: () =>
      import('./features/learner/learner-layout.component').then((m) => m.LearnerLayoutComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['LEARNER'] },
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/learner/learner-dashboard.component').then((m) => m.LearnerDashboardComponent),
      },
      {
        path: 'meetings',
        loadComponent: () =>
          import('./features/learner/learner-meetings.component').then((m) => m.LearnerMeetingsComponent),
      },
      {
        path: 'assessments',
        loadComponent: () =>
          import('./features/learner/learner-assessments.component').then((m) => m.LearnerAssessmentsComponent),
      },
      {
        path: 'results',
        loadComponent: () =>
          import('./features/learner/learner-results.component').then((m) => m.LearnerResultsComponent),
      },
      {
        path: 'coding',
        loadComponent: () =>
          import('./features/learner/learner-coding.component').then((m) => m.LearnerCodingComponent),
      },
      {
        path: 'practice',
        loadComponent: () =>
          import('./features/learner/learner-practice.component').then((m) => m.LearnerPracticeComponent),
      },
    ],
  },

  { path: '**', redirectTo: 'login' },
];

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideHttpClient(withInterceptors([authInterceptor])),
    provideRouter(routes),
  ],
};
