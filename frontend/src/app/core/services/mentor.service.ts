import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface MentorDashboardData {
  assigned_learners_count: number;
  upcoming_meetings: any[];
  live_assessments: any[];
  new_practice_alerts: any[];
  learners_needing_attention: any[];
}

export interface MeetingItem {
  id: string;
  title: string;
  description?: string;
  meeting_link: string;
  start_time: string;
  end_time: string;
  status: string;
  batch_id?: string;
  audience_type: string;
}

export interface AssessmentItem {
  id: string;
  title: string;
  field: string;
  duration_minutes: number;
  passing_score: number;
  is_published: boolean;
  version: number;
  questions_count: number;
  total_marks?: number;
  submissions_count: number;
  batch_id?: string;
  batch_name?: string;
  instructions?: string;
  status?: string;
  start_window?: string;
  end_window?: string;
  questions?: any[];
}

export interface QuestionBankItem {
  id: string;
  title: string;
  type: 'MCQ' | 'CODING';
  field: string;
  difficulty: string;
  tags: string[];
  content: string;
}

@Injectable({
  providedIn: 'root',
})
export class MentorService {
  private readonly http = inject(HttpClient);

  getDashboard(): Observable<MentorDashboardData> {
    return this.http.get<MentorDashboardData>('/api/v1/mentor/dashboard');
  }

  getMeetings(): Observable<MeetingItem[]> {
    return this.http.get<MeetingItem[]>('/api/v1/mentor/meetings');
  }

  createMeeting(payload: {
    title: string;
    description?: string;
    meeting_link: string;
    start_time: string;
    end_time: string;
    batch_id?: string;
    learner_ids?: string[];
  }): Observable<MeetingItem> {
    return this.http.post<MeetingItem>('/api/v1/mentor/meetings', payload);
  }

  updateMeeting(id: string, payload: Partial<MeetingItem>): Observable<MeetingItem> {
    return this.http.put<MeetingItem>(`/api/v1/mentor/meetings/${id}`, payload);
  }

  cancelMeeting(id: string): Observable<{ status: string }> {
    return this.http.delete<{ status: string }>(`/api/v1/mentor/meetings/${id}`);
  }

  markAttendance(meetingId: string, attendances: Array<{ learner_id: string; attended: boolean; notes?: string }>): Observable<any> {
    return this.http.post(`/api/v1/mentor/meetings/${meetingId}/attendance`, { attendances });
  }

  getAssessments(): Observable<AssessmentItem[]> {
    return this.http.get<AssessmentItem[]>('/api/v1/mentor/assessments');
  }

  createAssessment(payload: {
    title: string;
    field: string;
    instructions?: string;
    duration_minutes: number;
    passing_score: number;
    start_window?: string;
    end_window?: string;
    questions?: any[];
  }): Observable<AssessmentItem> {
    return this.http.post<AssessmentItem>('/api/v1/mentor/assessments', payload);
  }

  publishAssessment(id: string): Observable<AssessmentItem> {
    return this.http.post<AssessmentItem>(`/api/v1/mentor/assessments/${id}/publish`, {});
  }

  getAssessmentResults(id: string): Observable<any> {
    return this.http.get(`/api/v1/mentor/assessments/${id}/results`);
  }

  exportAssessmentCsv(id: string): Observable<string> {
    return this.http.get(`/api/v1/mentor/assessments/${id}/results/export`, { responseType: 'text' });
  }

  getQuestionBank(field?: string, difficulty?: string): Observable<QuestionBankItem[]> {
    return this.http.get<QuestionBankItem[]>('/api/v1/mentor/questions');
  }

  addQuestionToBank(payload: any): Observable<QuestionBankItem> {
    return this.http.post<QuestionBankItem>('/api/v1/mentor/questions', payload);
  }

  getAssessmentQuestions(assessmentId: string): Observable<any[]> {
    return this.http.get<any[]>(`/api/v1/mentor/assessments/${assessmentId}/questions`);
  }

  attachQuestionToAssessment(assessmentId: string, payload: { question_id: string; marks: number; order?: number }): Observable<any> {
    return this.http.post<any>(`/api/v1/mentor/assessments/${assessmentId}/questions`, payload);
  }

  updateAssessmentQuestions(assessmentId: string, questions: any[]): Observable<any> {
    return this.http.put<any>(`/api/v1/mentor/assessments/${assessmentId}/questions`, { questions });
  }

  removeQuestionFromAssessment(assessmentId: string, aqId: string): Observable<any> {
    return this.http.delete<any>(`/api/v1/mentor/assessments/${assessmentId}/questions/${aqId}`);
  }

  updateAssessment(id: string, payload: any): Observable<AssessmentItem> {
    return this.http.put<AssessmentItem>(`/api/v1/mentor/assessments/${id}`, payload);
  }

  getBatches(): Observable<any[]> {
    return this.http.get<any[]>('/api/v1/mentor/batches');
  }

  getLearners(): Observable<any[]> {
    return this.http.get<any[]>('/api/v1/mentor/learners');
  }

  addLearnerRemark(learnerId: string, remark: string, category: string): Observable<any> {
    return this.http.post(`/api/v1/mentor/learners/${learnerId}/remarks`, {
      remark,
      category,
    });
  }

  getTalentAlerts(): Observable<any[]> {
    return this.http.get<any[]>('/api/v1/mentor/spotlight');
  }

  actOnAlert(alertId: string, action: 'INVITE_TEST' | 'SCHEDULE_INTERVIEW' | 'RECOMMEND_PROMOTION' | 'DISMISS', notes?: string): Observable<any> {
    return this.http.post(`/api/v1/mentor/spotlight/${alertId}/action`, {
      action,
      notes,
    });
  }
}
