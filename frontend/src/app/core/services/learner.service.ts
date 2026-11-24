import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

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

  getDashboard(): Observable<LearnerDashboardData> {
    return this.http.get<LearnerDashboardData>('/api/v1/learner/dashboard');
  }

  getMeetings(): Observable<LearnerMeetingItem[]> {
    return this.http.get<LearnerMeetingItem[]>('/api/v1/learner/meetings');
  }

  downloadIcs(meetingId: string): Observable<string> {
    return this.http.get(`/api/v1/learner/meetings/${meetingId}/ics`, { responseType: 'text' });
  }

  getAssessments(): Observable<any[]> {
    return this.http.get<any[]>('/api/v1/learner/assessments');
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
    });
  }

  getResults(): Observable<any[]> {
    return this.http.get<any[]>('/api/v1/learner/results');
  }

  getResultDetail(attemptId: string): Observable<any> {
    return this.http.get(`/api/v1/learner/results/${attemptId}`);
  }

  getAssessmentReport(attemptId: string): Observable<any> {
    return this.http.get(`/api/v1/learner/results/${attemptId}/report`);
  }

  getAIDiagnostic(): Observable<any> {
    return this.http.get('/api/v1/learner/analytics/ai-diagnostic');
  }

  chatWithGardener(message: string, history: Array<{ role: string; content: string }> = []): Observable<any> {
    return this.http.post('/api/v1/learner/chatbot/chat', {
      message,
      history,
    });
  }
}
