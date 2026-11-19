import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const roleGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (!authService.isAuthenticated()) {
    return router.createUrlTree(['/login'], { queryParams: { returnUrl: state.url } });
  }

  const allowedRoles = (route.data['roles'] as string[]) || [];
  const currentUser = authService.currentUser();
  const userRole = (currentUser?.role || currentUser?.roles?.[0] || 'LEARNER').toUpperCase();

  if (allowedRoles.length === 0 || allowedRoles.includes(userRole)) {
    return true;
  }

  // Redirect to user's permitted role dashboard
  const defaultPath = authService.getRoleRedirectPath();
  return router.createUrlTree([defaultPath]);
};
