import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, shareReplay, tap } from 'rxjs';

export interface RecommendedReadingItem {
  title: string;
  url?: string;
  description?: string;
}

export interface AssessmentNote {
  id: string;
  assessment_id: string;
  assessment_title?: string;
  assessment_field?: string;
  author_id: string;
  author_name?: string;
  title: string;
  module_name: string;
  summary?: string;
  content: string;
  key_takeaways: string[];
  recommended_reading: RecommendedReadingItem[];
  estimated_read_time_minutes: number;
  is_published: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateAssessmentNoteRequest {
  title: string;
  module_name?: string;
  summary?: string;
  content: string;
  key_takeaways?: string[];
  recommended_reading?: RecommendedReadingItem[];
  estimated_read_time_minutes?: number;
  is_published?: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class NotesService {
  private readonly http = inject(HttpClient);
  private notesCache$?: Observable<AssessmentNote[]>;

  // Learner methods with instantaneous client-side cache
  getLearnerNotes(search?: string, field?: string, forceRefresh = false): Observable<AssessmentNote[]> {
    if (!search && !field && this.notesCache$ && !forceRefresh) {
      return this.notesCache$;
    }
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (field) params = params.set('field', field);
    const req$ = this.http.get<AssessmentNote[]>('/api/v1/learner/notes', { params }).pipe(
      shareReplay({ bufferSize: 1, refCount: false })
    );
    if (!search && !field) {
      this.notesCache$ = req$;
    }
    return req$;
  }

  getLearnerAssessmentNotes(assessmentId: string): Observable<AssessmentNote[]> {
    return this.http.get<AssessmentNote[]>(`/api/v1/learner/assessments/${assessmentId}/notes`).pipe(
      shareReplay({ bufferSize: 1, refCount: false })
    );
  }

  // Mentor methods
  getMentorAssessmentNotes(assessmentId: string): Observable<AssessmentNote[]> {
    return this.http.get<AssessmentNote[]>(`/api/v1/mentor/assessments/${assessmentId}/notes`);
  }

  createAssessmentNote(assessmentId: string, note: CreateAssessmentNoteRequest): Observable<AssessmentNote> {
    return this.http.post<AssessmentNote>(`/api/v1/mentor/assessments/${assessmentId}/notes`, note).pipe(
      tap(() => {
        this.notesCache$ = undefined;
      })
    );
  }

  updateAssessmentNote(noteId: string, note: Partial<CreateAssessmentNoteRequest>): Observable<AssessmentNote> {
    return this.http.put<AssessmentNote>(`/api/v1/mentor/notes/${noteId}`, note).pipe(
      tap(() => {
        this.notesCache$ = undefined;
      })
    );
  }

  deleteAssessmentNote(noteId: string): Observable<{ status: string; message: string; id: string }> {
    return this.http.delete<{ status: string; message: string; id: string }>(`/api/v1/mentor/notes/${noteId}`).pipe(
      tap(() => {
        this.notesCache$ = undefined;
      })
    );
  }
}
