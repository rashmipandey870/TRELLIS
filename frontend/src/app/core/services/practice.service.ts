import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface PracticeField {
  id: string;
  name: string;
  description: string;
  icon?: string;
}

export interface GeneratedPracticeQuestion {
  id: string;
  field: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  question_type: 'MCQ' | 'CODING';
  mode?: 'MCQ' | 'CODING';
  source?: 'llm' | 'template' | string;
  title: string;
  content: string;
  options?: Array<{ id: string; option_text: string }>;
  hints?: string[];
  explanation?: string;
  correct_answer?: string;
  starter_code?: Record<string, string>;
  constraints?: string;
  sample_cases?: Array<{ input: string; output: string }>;
  question_data?: any;
}

export interface PracticeAttemptResult {
  correct: boolean;
  score_delta: number;
  explanation: string;
  complexity_feedback?: string;
  progressive_hint?: string;
  current_streak: number;
}

export interface DedicationScoreSummary {
  field: string;
  active_days_30d: number;
  problems_attempted: number;
  weighted_accuracy: number;
  dedication_score: number;
  trend: 'UP' | 'STABLE' | 'DOWN';
  talent_spotlight_qualified: boolean;
}

export interface AssistantResponse {
  reply: string;
  suggested_actions?: Array<{ label: string; action: string; target: string }>;
}

@Injectable({
  providedIn: 'root',
})
export class PracticeService {
  private readonly http = inject(HttpClient);

  getFields(): Observable<PracticeField[]> {
    return this.http.get<PracticeField[]>('/api/v1/practice/fields');
  }

  generateQuestion(payload: {
    field: string;
    difficulty: 'EASY' | 'MEDIUM' | 'HARD';
    question_type: 'MCQ' | 'CODING';
  }): Observable<GeneratedPracticeQuestion> {
    return this.http.post<GeneratedPracticeQuestion>('/api/v1/practice/generate', payload);
  }

  submitAttempt(payload: {
    question_id: string;
    answer_text?: string;
    source_code?: string;
    language?: string;
    time_spent_seconds?: number;
  }): Observable<PracticeAttemptResult> {
    return this.http.post<PracticeAttemptResult>('/api/v1/practice/attempt', payload);
  }

  getDedicationScores(): Observable<DedicationScoreSummary[]> {
    return this.http.get<DedicationScoreSummary[]>('/api/v1/practice/dedication');
  }

  askAssistant(message: string, context?: Record<string, any>): Observable<AssistantResponse> {
    return this.http.post<AssistantResponse>('/api/v1/practice/assistant', {
      message,
      context,
    });
  }

  getWeeklyStudyPlan(): Observable<any> {
    return this.http.get<any>('/api/v1/practice/study-plan');
  }

  getPracticeHistory(): Observable<any[]> {
    return this.http.get<any[]>('/api/v1/practice/history');
  }
}
