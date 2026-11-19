import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth.service';
import { PracticeService } from '../../core/services/practice.service';

interface ChatMessage {
  sender: 'user' | 'assistant';
  text: string;
  time: string;
  actions?: Array<{ label: string; action: string; target: string }>;
}

@Component({
  selector: 'app-assistant',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <!-- Floating Trigger Button -->
    <div class="fixed bottom-6 right-6 z-50">
      @if (!isOpen()) {
        <button 
          (click)="toggleOpen()" 
          class="flex items-center gap-2.5 px-4 py-3 rounded-full bg-gradient-to-r from-[#FAA634] via-[#D7182A] to-[#008FBB] text-white font-bold text-xs shadow-2xl hover:scale-105 active:scale-95 transition focus:outline-none">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          <span>Ask TRELLIS AI</span>
          <span class="px-1.5 py-0.5 rounded-full bg-white/20 text-[10px] uppercase font-bold">{{ roleName() }}</span>
        </button>
      }
    </div>

    <!-- Assistant Chat Window -->
    @if (isOpen()) {
      <div class="fixed bottom-6 right-6 z-50 w-96 max-w-[calc(100vw-2rem)] bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-200">
        
        <!-- Header -->
        <div class="px-4 py-3 bg-gradient-to-r from-[#008FBB] to-[#005e7c] text-white flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div class="w-7 h-7 rounded-lg bg-white/20 flex items-center justify-center font-black text-xs">
              AI
            </div>
            <div>
              <h3 class="text-xs font-bold leading-tight">TRELLIS Assistant</h3>
              <p class="text-[10px] text-sky-100 uppercase tracking-wider font-semibold">Role-Governed: {{ roleName() }}</p>
            </div>
          </div>
          <button (click)="toggleOpen()" class="p-1 rounded-lg hover:bg-white/20 text-white transition">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Chat History -->
        <div class="p-4 h-80 overflow-y-auto space-y-3 bg-slate-50 dark:bg-slate-950 text-xs">
          @for (msg of messages(); track msg.time) {
            <div [ngClass]="msg.sender === 'user' ? 'flex justify-end' : 'flex justify-start'">
              <div 
                [ngClass]="msg.sender === 'user' 
                  ? 'bg-[#008FBB] text-white rounded-2xl rounded-tr-none px-3.5 py-2 max-w-[85%]' 
                  : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 border border-slate-200 dark:border-slate-700 rounded-2xl rounded-tl-none px-3.5 py-2 max-w-[85%] shadow-sm'">
                <p class="whitespace-pre-wrap">{{ msg.text }}</p>
                <span class="block text-[9px] mt-1 text-right" [ngClass]="msg.sender === 'user' ? 'text-sky-200' : 'text-slate-400'">{{ msg.time }}</span>
              </div>
            </div>
          }
          @if (loading()) {
            <div class="flex items-center gap-2 text-slate-400 italic text-[11px] p-2">
              <div class="w-1.5 h-1.5 rounded-full bg-[#008FBB] animate-bounce"></div>
              <div class="w-1.5 h-1.5 rounded-full bg-[#FAA634] animate-bounce [animation-delay:0.2s]"></div>
              <div class="w-1.5 h-1.5 rounded-full bg-[#D7182A] animate-bounce [animation-delay:0.4s]"></div>
              <span>Querying verified enterprise knowledge...</span>
            </div>
          }
        </div>

        <!-- Role-based Prompt Suggestions -->
        <div class="px-3 py-2 bg-slate-100 dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex gap-1.5 overflow-x-auto text-[10px]">
          @for (prompt of suggestedPrompts(); track prompt) {
            <button 
              type="button" 
              (click)="sendQuickPrompt(prompt)"
              class="whitespace-nowrap px-2.5 py-1 rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:border-[#008FBB] hover:text-[#008FBB] transition">
              {{ prompt }}
            </button>
          }
        </div>

        <!-- Input Bar -->
        <form (ngSubmit)="sendMessage()" class="p-2.5 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex gap-2">
          <input 
            type="text" 
            [(ngModel)]="userInput" 
            name="message" 
            [disabled]="loading()"
            placeholder="Ask anything about your curriculum, meetings, stats..."
            class="flex-1 px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-[#008FBB]" />
          <button 
            type="submit" 
            [disabled]="loading() || !userInput.trim()"
            class="px-3 py-2 bg-[#008FBB] hover:bg-[#007499] disabled:opacity-50 text-white rounded-xl font-bold text-xs transition">
            Send
          </button>
        </form>

      </div>
    }
  `,
})
export class AssistantComponent {
  private readonly authService = inject(AuthService);
  private readonly practiceService = inject(PracticeService);

  readonly isOpen = signal<boolean>(false);
  readonly loading = signal<boolean>(false);
  userInput = '';

  readonly roleName = computed(() => {
    return this.authService.primaryRole() || 'LEARNER';
  });

  readonly suggestedPrompts = computed(() => {
    const role = this.roleName();
    if (role === 'ADMIN') {
      return ['Department dashboard summary', 'Review Talent Spotlight alerts', 'Assessments conducted per mentor'];
    }
    if (role === 'MENTOR') {
      return ['Which learners need attention?', 'Upcoming meetings today', 'Pending assessment submissions'];
    }
    return ['My upcoming meetings', 'What are my weak topics?', 'My coding streak status'];
  });

  readonly messages = signal<ChatMessage[]>([
    {
      sender: 'assistant',
      text: 'Hello! I am your TRELLIS assistant. I provide role-governed intelligence for your learning, assessments, and metrics at CSM Technologies.',
      time: 'Now',
    },
  ]);

  toggleOpen(): void {
    this.isOpen.update((v) => !v);
  }

  sendQuickPrompt(prompt: string): void {
    this.userInput = prompt;
    this.sendMessage();
  }

  sendMessage(): void {
    const query = this.userInput.trim();
    if (!query) return;

    this.messages.update((list) => [
      ...list,
      {
        sender: 'user',
        text: query,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);
    this.userInput = '';
    this.loading.set(true);

    this.practiceService.askAssistant(query).subscribe({
      next: (res) => {
        this.loading.set(false);
        this.messages.update((list) => [
          ...list,
          {
            sender: 'assistant',
            text: res.reply,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            actions: res.suggested_actions,
          },
        ]);
      },
      error: (err) => {
        this.loading.set(false);
        this.messages.update((list) => [
          ...list,
          {
            sender: 'assistant',
            text: err.error?.detail || 'Unable to retrieve answer right now. Please try again.',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          },
        ]);
      },
    });
  }
}
