import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface CodingProblemSummary {
  id: string;
  title: string;
  slug: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  category: string;
  tags: string[];
}

export interface CodingProblemDetail extends CodingProblemSummary {
  statement: string;
  constraints: string;
  examples: Array<{ input: string; output: string; explanation?: string }>;
  starter_code: Record<string, string>;
  time_limit_ms: number;
  memory_limit_mb: number;
}

export interface RunCodeResult {
  status: string;
  stdout: string;
  stderr: string;
  execution_time_ms: number;
  passed?: boolean;
}

export interface SubmitCodeResult {
  id: string;
  verdict: 'ACCEPTED' | 'WRONG_ANSWER' | 'TIME_LIMIT_EXCEEDED' | 'RUNTIME_ERROR' | 'COMPILATION_ERROR' | string;
  passed_cases: number;
  total_cases: number;
  score: number;
  max_score: number;
  runtime_ms: number;
  memory_mb: number;
  runtime_percentile: number;
  failing_case?: {
    input: string;
    expected: string;
    actual: string;
  } | null;
  created_at: string;
}

@Injectable({
  providedIn: 'root',
})
export class CodingService {
  private readonly http = inject(HttpClient);

  getProblems(category?: string, difficulty?: string): Observable<CodingProblemSummary[]> {
    let params = new HttpParams();
    if (category) params = params.set('category', category);
    if (difficulty) params = params.set('difficulty', difficulty);
    return this.http.get<CodingProblemSummary[]>('/api/v1/coding/problems', { params });
  }

  getProblem(id: string): Observable<CodingProblemDetail> {
    return this.http.get<CodingProblemDetail>(`/api/v1/coding/problems/${id}`);
  }

  runCode(payload: {
    source_code: string;
    language: string;
    custom_input?: string;
    expected_output?: string;
  }): Observable<RunCodeResult> {
    return this.http.post<RunCodeResult>('/api/v1/coding/run', payload);
  }

  submitCode(payload: {
    problem_id: string;
    source_code: string;
    language: string;
    assessment_attempt_id?: string;
  }): Observable<SubmitCodeResult> {
    return this.http.post<SubmitCodeResult>('/api/v1/coding/submit', payload);
  }

  getSubmissions(problemId?: string): Observable<SubmitCodeResult[]> {
    let params = new HttpParams();
    if (problemId) params = params.set('problem_id', problemId);
    return this.http.get<SubmitCodeResult[]>('/api/v1/coding/submissions', { params });
  }
}
