import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface AdminDashboardData {
  total_learners: number;
  total_mentors: number;
  total_batches: number;
  average_score: number;
  top_performers: Array<{
    id: string;
    full_name: string;
    email: string;
    streak_days: number;
    score: number;
  }>;
  learners_needing_attention: Array<{
    id: string;
    full_name: string;
    email: string;
    reason: string;
  }>;
  mentor_metrics: Array<{
    mentor_id: string;
    name: string;
    batches_count: number;
    learners_count: number;
    assessments_count: number;
  }>;
  practice_engagement: {
    total_attempts: number;
    active_learners_30d: number;
  };
  talent_alerts: Array<any>;
}

export interface UserSummary {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  streak_days: number;
  created_at: string;
}

export interface BatchSummary {
  id: string;
  name: string;
  code: string;
  description?: string;
  is_active: boolean;
  mentors: Array<{ id: string; name: string }>;
  learners_count: number;
}

export interface LearnerDetailData {
  id: string;
  full_name: string;
  email: string;
  batch: string | null;
  mentor: string | null;
  streak_days: number;
  assessment_scores: Array<{
    assessment_title: string;
    score: number;
    passed: boolean;
    date: string;
  }>;
  coding_submissions: Array<{
    problem_title: string;
    language: string;
    verdict: string;
    runtime_ms: number;
    date: string;
  }>;
  meeting_attendance: Array<{
    meeting_title: string;
    attended: boolean;
    date: string;
  }>;
  practice_activity: Array<{
    field: string;
    problems_attempted: number;
    accuracy: number;
    dedication_score: number;
  }>;
  performance_analysis: {
    strengths: string[];
    weak_topics: string[];
    batch_percentile: number;
    practice_dedication: number;
  };
}

@Injectable({
  providedIn: 'root',
})
export class AdminService {
  private readonly http = inject(HttpClient);

  getDashboard(): Observable<AdminDashboardData> {
    return this.http.get<AdminDashboardData>('/api/v1/admin/dashboard');
  }

  getUsers(role?: string, search?: string): Observable<UserSummary[]> {
    let params = new HttpParams();
    if (role) params = params.set('role', role);
    if (search) params = params.set('search', search);
    return this.http.get<UserSummary[]>('/api/v1/admin/users', { params });
  }

  createUser(payload: { email: string; full_name: string; role: string; password?: string }): Observable<UserSummary> {
    return this.http.post<UserSummary>('/api/v1/admin/users', payload);
  }

  updateUser(id: string, payload: Partial<UserSummary>): Observable<UserSummary> {
    return this.http.put<UserSummary>(`/api/v1/admin/users/${id}`, payload);
  }

  deactivateUser(id: string): Observable<{ status: string }> {
    return this.http.delete<{ status: string }>(`/api/v1/admin/users/${id}`);
  }

  bulkImportUsers(csvContent: string): Observable<{ created: number; errors: string[] }> {
    return this.http.post<{ created: number; errors: string[] }>('/api/v1/admin/users/bulk-import', {
      csv_content: csvContent,
    });
  }

  getBatches(): Observable<BatchSummary[]> {
    return this.http.get<BatchSummary[]>('/api/v1/admin/batches');
  }

  createBatch(payload: { name: string; code: string; description?: string }): Observable<BatchSummary> {
    return this.http.post<BatchSummary>('/api/v1/admin/batches', payload);
  }

  assignMentorToBatch(batchId: string, mentorId: string): Observable<any> {
    return this.http.post(`/api/v1/admin/batches/${batchId}/assign-mentor`, { mentor_id: mentorId });
  }

  assignLearnerToBatch(batchId: string, learnerId: string): Observable<any> {
    return this.http.post(`/api/v1/admin/batches/${batchId}/assign-learner`, { learner_id: learnerId });
  }

  getLearners(batchId?: string, search?: string): Observable<any[]> {
    let params = new HttpParams();
    if (batchId) params = params.set('batch_id', batchId);
    if (search) params = params.set('search', search);
    return this.http.get<any[]>('/api/v1/admin/learners', { params });
  }

  getLearnerDetail(learnerId: string): Observable<LearnerDetailData> {
    return this.http.get<LearnerDetailData>(`/api/v1/admin/learners/${learnerId}`);
  }

  getSettings(): Observable<any[]> {
    return this.http.get<any[]>('/api/v1/admin/settings');
  }

  updateSetting(key: string, value: string): Observable<any> {
    return this.http.put(`/api/v1/admin/settings/${key}`, { value });
  }

  getAuditLogs(): Observable<any[]> {
    return this.http.get<any[]>('/api/v1/admin/audit-logs');
  }

  getTalentSpotlight(): Observable<any[]> {
    return this.http.get<any[]>('/api/v1/admin/talent-spotlight');
  }

  getAIHealth(): Observable<AIHealthData> {
    return this.http.get<AIHealthData>('/api/v1/admin/ai/health');
  }

  manageCircuitBreaker(action: 'trip' | 'reset'): Observable<any> {
    return this.http.post('/api/v1/admin/ai/circuit-breaker', { action });
  }

  refillAIPool(): Observable<any> {
    return this.http.post('/api/v1/admin/ai/pool/refill', {});
  }
}

export interface AIHealthData {
  status: 'HEALTHY' | 'DEGRADED' | 'DOWN';
  primary_provider: string;
  active_instruct_model: string;
  active_code_model: string;
  circuit_breaker_state: 'CLOSED' | 'OPEN' | 'HALF_OPEN';
  p50_latency_ms: number;
  p95_latency_ms: number;
  total_requests: number;
  success_rate_percent: number;
  validation_pass_rate_percent: number;
  pool_counts: Record<string, number>;
  queue_depth: number;
  alerts: string[];
}
