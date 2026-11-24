import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from '../../shared/header/header.component';
import { AssistantComponent } from '../../shared/assistant/assistant.component';

@Component({
  selector: 'app-mentor-layout',
  standalone: true,
  imports: [CommonModule, RouterModule, HeaderComponent, AssistantComponent],
  template: `
    <div class="min-h-screen bg-slate-50 flex flex-col font-sans">
      <app-header />

      <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        <router-outlet />
      </main>

      <app-assistant />
    </div>
  `,
})
export class MentorLayoutComponent {}
