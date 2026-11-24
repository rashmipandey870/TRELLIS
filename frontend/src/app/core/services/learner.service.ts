import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, shareReplay, tap } from 'rxjs';

export interface LearnerDashboardData {
  upcoming_meetings: any[];
  assigned_assessments: any[];
  latest_scores: any[];
  streak_days: number;
  mentor_remarks: any[];
  progress_chart: any[];
}

export interface LearnerMeetingItem {
  id: string;
  title: string;
  description?: string;
  meeting_link: string;
  start_time: string;
  end_time: string;
  status: string;
  mentor_name: string;
}

export interface ActiveAssessmentAttempt {
  attempt_id: string;
  assessment_id: string;
  title: string;
  field: string;
  duration_minutes: number;
  remaining_seconds: number;
  started_at: string;
  questions: Array<{
    id: string;
    question_type: 'MCQ' | 'CODING';
    title: string;
    content: string;
    marks: number;
    options?: Array<{ id: string; option_text: string }>;
    coding_details?: {
      starter_code: Record<string, string>;
      constraints: string;
      sample_cases: Array<{ input: string; output: string }>;
    };
  }>;
  existing_answers: Record<string, any>;
}

@Injectable({
  providedIn: 'root',
})
export class LearnerService {
  private readonly http = inject(HttpClient);

  private dashboardCache$?: Observable<LearnerDashboardData>;
  private assessmentsCache$?: Observable<any[]>;
  private resultsCache$?: Observable<any[]>;
  private meetingsCache$?: Observable<LearnerMeetingItem[]>;
  private diagnosticCache$?: Observable<any>;

  getDashboard(forceRefresh = false): Observable<LearnerDashboardData> {
    if (!this.dashboardCache$ || forceRefresh) {
      this.dashboardCache$ = this.http.get<LearnerDashboardData>('/api/v1/learner/dashboard').pipe(
        shareReplay({ bufferSize: 1, refCount: false })
      );
    }
    return this.dashboardCache$;
  }

  getMeetings(forceRefresh = false): Observable<LearnerMeetingItem[]> {
    if (!this.meetingsCache$ || forceRefresh) {
      this.meetingsCache$ = this.http.get<LearnerMeetingItem[]>('/api/v1/learner/meetings').pipe(
        shareReplay({ bufferSize: 1, refCount: false })
      );
    }
    return this.meetingsCache$;
  }

  downloadIcs(meetingId: string): Observable<string> {
    return this.http.get(`/api/v1/learner/meetings/${meetingId}/ics`, { responseType: 'text' });
  }

  getAssessments(forceRefresh = false): Observable<any[]> {
    if (!this.assessmentsCache$ || forceRefresh) {
      this.assessmentsCache$ = this.http.get<any[]>('/api/v1/learner/assessments').pipe(
        shareReplay({ bufferSize: 1, refCount: false })
      );
    }
    return this.assessmentsCache$;
  }

  startAssessment(assessmentId: string): Observable<ActiveAssessmentAttempt> {
    return this.http.post<ActiveAssessmentAttempt>(`/api/v1/learner/assessments/${assessmentId}/start`, {});
  }

  saveAnswer(attemptId: string, questionId: string, answerData: any): Observable<any> {
    return this.http.post(`/api/v1/learner/attempts/${attemptId}/answers`, {
      question_id: questionId,
      answer_data: answerData,
    });
  }

  submitAssessment(attemptId: string, tabSwitches: number = 0): Observable<any> {
    return this.http.post(`/api/v1/learner/attempts/${attemptId}/submit`, {
      tab_switches: tabSwitches,
    }).pipe(
      tap(() => {
        // Invalidate results and assessments caches on submission
        this.resultsCache$ = undefined;
        this.assessmentsCache$ = undefined;
        this.dashboardCache$ = undefined;
      })
    );
  }

  getResults(forceRefresh = false): Observable<any[]> {
    if (!this.resultsCache$ || forceRefresh) {
      this.resultsCache$ = this.http.get<any[]>('/api/v1/learner/results').pipe(
        shareReplay({ bufferSize: 1, refCount: false })
      );
    }
    return this.resultsCache$;
  }

  getResultDetail(attemptId: string): Observable<any> {
    return this.http.get(`/api/v1/learner/results/${attemptId}`);
  }

  getAssessmentReport(attemptId: string): Observable<any> {
    return this.http.get(`/api/v1/learner/results/${attemptId}/report`);
  }

  getAIDiagnostic(forceRefresh = false): Observable<any> {
    if (!this.diagnosticCache$ || forceRefresh) {
      this.diagnosticCache$ = this.http.get('/api/v1/learner/analytics/ai-diagnostic').pipe(
        shareReplay({ bufferSize: 1, refCount: false })
      );
    }
    return this.diagnosticCache$;
  }

  chatWithGardener(message: string, history: Array<{ role: string; content: string }> = []): Observable<any> {
    return this.http.post('/api/v1/learner/chatbot/chat', {
      message,
      history,
    });
  }
}
