import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-csm-landing',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="min-h-screen bg-white text-slate-900 flex flex-col font-sans selection:bg-[#008FBB] selection:text-white relative overflow-x-hidden">
      
      <!-- Ambient Diagonal Speed-Trails & Grid Background (Official csm.tech Visual Look) -->
      <div class="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <!-- Fine Grid Pattern -->
        <div class="absolute inset-0 opacity-[0.035]" 
             style="background-image: linear-gradient(to right, #0f172a 1px, transparent 1px), linear-gradient(to bottom, #0f172a 1px, transparent 1px); background-size: 40px 40px;">
        </div>

        <!-- Diagonal Color Streaks (Cyan, Saffron, Red Trails) -->
        <svg class="absolute -right-20 top-0 w-[1100px] h-[900px] opacity-40" viewBox="0 0 1100 900" fill="none">
          <line x1="200" y1="900" x2="850" y2="0" stroke="url(#streak-cyan)" stroke-width="2.5" stroke-linecap="round" />
          <line x1="320" y1="900" x2="970" y2="0" stroke="url(#streak-orange)" stroke-width="2" stroke-linecap="round" />
          <line x1="450" y1="900" x2="1100" y2="0" stroke="url(#streak-cyan)" stroke-width="1.5" stroke-linecap="round" />
          <line x1="120" y1="900" x2="770" y2="0" stroke="url(#streak-red)" stroke-width="1" stroke-linecap="round" />
          <line x1="50" y1="900" x2="700" y2="0" stroke="url(#streak-soft)" stroke-width="3" stroke-linecap="round" />
          <line x1="400" y1="900" x2="1050" y2="0" stroke="url(#streak-soft)" stroke-width="4" stroke-linecap="round" opacity="0.4" />
          <defs>
            <linearGradient id="streak-cyan" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#008FBB" stop-opacity="0" />
              <stop offset="50%" stop-color="#008FBB" stop-opacity="0.8" />
              <stop offset="100%" stop-color="#008FBB" stop-opacity="0" />
            </linearGradient>
            <linearGradient id="streak-orange" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#FAA634" stop-opacity="0" />
              <stop offset="50%" stop-color="#FAA634" stop-opacity="0.9" />
              <stop offset="100%" stop-color="#FAA634" stop-opacity="0" />
            </linearGradient>
            <linearGradient id="streak-red" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#D7182A" stop-opacity="0" />
              <stop offset="50%" stop-color="#D7182A" stop-opacity="0.7" />
              <stop offset="100%" stop-color="#D7182A" stop-opacity="0" />
            </linearGradient>
            <linearGradient id="streak-soft" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#94a3b8" stop-opacity="0" />
              <stop offset="50%" stop-color="#cbd5e1" stop-opacity="0.6" />
              <stop offset="100%" stop-color="#94a3b8" stop-opacity="0" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      <!-- Top Navbar (Matching Official csm.tech Style) -->
      <header class="relative z-30 bg-white/90 backdrop-blur-md border-b border-slate-100">
        <div class="max-w-[1400px] mx-auto px-6 sm:px-8">
          <div class="flex items-center justify-between h-20">
            
            <!-- Left: CSM Brand Logo + TRELLIS L&K Subtitle -->
            <div class="flex items-center gap-6">
              <a routerLink="/" class="flex items-center gap-1.5 focus:outline-none">
                <!-- 3 Slashes (Orange, Red, Teal) -->
                <div class="flex items-center space-x-[3px] font-black italic tracking-tighter text-2xl select-none">
                  <span class="text-[#FAA634] font-black -rotate-12 inline-block">/</span>
                  <span class="text-[#D7182A] font-black -rotate-12 inline-block">/</span>
                  <span class="text-[#008FBB] font-black -rotate-12 inline-block">/</span>
                </div>
                <span class="text-2xl font-black italic tracking-tight text-slate-900 ml-1">CSM</span>
                <span class="text-[9px] font-bold text-slate-400 uppercase -mt-2.5">TM</span>
              </a>

              <!-- Divider -->
              <div class="hidden sm:block h-7 w-[1px] bg-slate-200"></div>

              <!-- L&K Platform Badge -->
              <div class="hidden sm:flex items-center gap-2">
                <div class="w-6 h-6 rounded-lg bg-gradient-to-tr from-[#FAA634] via-[#D7182A] to-[#008FBB] p-[1.5px] flex items-center justify-center">
                  <div class="w-full h-full bg-white rounded-[7px] flex items-center justify-center text-[10px] font-black text-slate-800">
                    T
                  </div>
                </div>
                <div class="flex flex-col text-[10px] leading-tight">
                  <span class="font-extrabold tracking-wider text-slate-900">TRELLIS</span>
                  <span class="text-[8px] tracking-widest text-[#008FBB] uppercase font-bold">L&amp;K PLATFORM</span>
                </div>
              </div>
            </div>

            <!-- Center Navigation Links (L&K Modules) -->
            <nav class="hidden xl:flex items-center gap-8 text-[13px] font-medium text-slate-700">
              <a routerLink="/login" class="hover:text-slate-950 transition">Learning Pathways</a>
              <a routerLink="/login" class="hover:text-slate-950 transition flex items-center gap-1.5">
                <span>AI Practice Lab</span>
                <span class="px-1.5 py-0.5 rounded text-[9px] font-black bg-sky-100 text-[#008FBB] border border-sky-200">8 FIELDS</span>
              </a>
              <a routerLink="/login" class="hover:text-slate-950 transition">Coding Sandbox</a>
              <a routerLink="/login" class="hover:text-slate-950 transition">Assessments</a>
              <a routerLink="/login" class="hover:text-slate-950 transition text-[#FAA634] font-bold">Talent Spotlight</a>
            </nav>

            <!-- Right Controls: Role Selector, Search, Login CTA -->
            <div class="flex items-center gap-3">
              <!-- Persona Quick Pills -->
              <div class="hidden md:flex items-center bg-slate-100 rounded-full p-1 text-[11px] font-bold text-slate-500">
                <a routerLink="/login" class="px-2.5 py-0.5 rounded-full bg-slate-900 text-white shadow-sm">Learner</a>
                <a routerLink="/login" class="px-2.5 py-0.5 hover:text-slate-900">Mentor</a>
                <a routerLink="/login" class="px-2.5 py-0.5 hover:text-slate-900">Admin</a>
              </div>

              <!-- Login CTA Button -->
              <a 
                routerLink="/login" 
                class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#008FBB] via-[#007499] to-[#005e7c] hover:from-[#007499] hover:to-[#004e69] text-white text-xs font-bold shadow-md shadow-sky-900/10 transition transform hover:-translate-y-0.5 flex items-center gap-2">
                <span>Sign In to TRELLIS</span>
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </a>
            </div>

          </div>
        </div>
      </header>

      <!-- Hero Main Section -->
      <main class="relative z-10 flex-1 flex flex-col justify-between max-w-[1400px] w-full mx-auto px-6 sm:px-8 pt-12 sm:pt-20 pb-12">
        
        <!-- Big Hero Content -->
        <div class="space-y-8 max-w-4xl">
          
          <!-- Headline with Gradient Word matching official csm.tech style -->
          <h1 class="text-5xl sm:text-7xl lg:text-[96px] font-black text-slate-950 tracking-tight leading-[1.04]">
            Intelligence you<br />
            can <span class="bg-gradient-to-r from-[#FAA634] via-[#D7182A] to-[#008FBB] bg-clip-text text-transparent">master.</span>
          </h1>

          <!-- Subheadline & Action Buttons Row -->
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8 pt-2">
            
            <!-- Description -->
            <p class="text-base sm:text-lg text-slate-600 max-w-lg leading-relaxed font-normal">
              Every barrier starts in the mind. We break it with structured engineering pathways, sandboxed verification, and real-time AI practice across 8 technical disciplines.
            </p>

            <!-- Dual Action CTAs -->
            <div class="flex flex-wrap items-center gap-4 shrink-0">
              <a 
                routerLink="/login" 
                class="px-7 py-3.5 rounded-xl bg-[#243949] hover:bg-[#1a2b38] text-white text-sm font-semibold shadow-lg shadow-slate-900/10 transition flex items-center gap-2">
                <span>Enter TRELLIS Portal</span>
                <span class="text-emerald-400">&rarr;</span>
              </a>

              <a 
                routerLink="/login" 
                class="px-7 py-3.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-300 text-slate-800 text-sm font-semibold shadow-sm transition">
                Sign In with Corporate ID
              </a>
            </div>

          </div>

        </div>

        <!-- Vertical Scroll Indicator on Right -->
        <div class="hidden lg:flex items-center gap-2 absolute right-8 top-1/2 -translate-y-1/2 rotate-90 origin-right text-[10px] uppercase font-bold tracking-widest text-slate-400">
          <span>L&amp;K ENGINE</span>
          <div class="w-8 h-[1px] bg-slate-300"></div>
        </div>

        <!-- Bottom 5 Sleek Feature Cards Strip (Adapted specifically to L&K Capabilities) -->
        <div class="pt-16 sm:pt-24">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            
            <!-- Card 01: AI Practice Lab -->
            <a routerLink="/login" class="p-5 rounded-2xl bg-white border border-slate-200/90 border-t-2 border-t-[#008FBB] shadow-sm hover:shadow-md hover:-translate-y-1 transition flex flex-col justify-between h-40 group cursor-pointer">
              <div>
                <div class="text-[#008FBB] text-lg mb-2">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                </div>
                <h3 class="text-sm font-bold text-slate-900 group-hover:text-[#008FBB] transition">
                  AI Practice Lab
                </h3>
                <p class="text-[11px] text-slate-400 mt-1 line-clamp-1">8 technical disciplines &bull; Ungraded</p>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>01</span>
                <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-[#008FBB] group-hover:text-white transition">&rarr;</span>
              </div>
            </a>

            <!-- Card 02: Coding Sandbox -->
            <a routerLink="/login" class="p-5 rounded-2xl bg-white border border-slate-200/90 border-t-2 border-t-[#00BCD4] shadow-sm hover:shadow-md hover:-translate-y-1 transition flex flex-col justify-between h-40 group cursor-pointer">
              <div>
                <div class="text-[#00BCD4] text-lg mb-2">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
                <h3 class="text-sm font-bold text-slate-900 group-hover:text-[#00BCD4] transition">
                  Coding Sandbox
                </h3>
                <p class="text-[11px] text-slate-400 mt-1 line-clamp-1">Isolated sub-process execution</p>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>02</span>
                <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-[#00BCD4] group-hover:text-white transition">&rarr;</span>
              </div>
            </a>

            <!-- Card 03: Assessments & Palettes -->
            <a routerLink="/login" class="p-5 rounded-2xl bg-white border border-slate-200/90 border-t-2 border-t-[#FAA634] shadow-sm hover:shadow-md hover:-translate-y-1 transition flex flex-col justify-between h-40 group cursor-pointer">
              <div>
                <div class="text-[#FAA634] text-lg mb-2">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </div>
                <h3 class="text-sm font-bold text-slate-900 group-hover:text-[#FAA634] transition">
                  Timed Assessments
                </h3>
                <p class="text-[11px] text-slate-400 mt-1 line-clamp-1">Autosave &bull; Tab switch monitoring</p>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>03</span>
                <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-[#FAA634] group-hover:text-white transition">&rarr;</span>
              </div>
            </a>

            <!-- Card 04: Talent Spotlight -->
            <a routerLink="/login" class="p-5 rounded-2xl bg-white border border-slate-200/90 border-t-2 border-t-[#F59E0B] shadow-sm hover:shadow-md hover:-translate-y-1 transition flex flex-col justify-between h-40 group cursor-pointer">
              <div>
                <div class="text-[#F59E0B] text-lg mb-2">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 class="text-sm font-bold text-slate-900 group-hover:text-[#F59E0B] transition">
                  Talent Spotlight
                </h3>
                <p class="text-[11px] text-slate-400 mt-1 line-clamp-1">Automated dedication thresholds</p>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>04</span>
                <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-[#F59E0B] group-hover:text-white transition">&rarr;</span>
              </div>
            </a>

            <!-- Card 05: Evidence Ledger -->
            <a routerLink="/login" class="p-5 rounded-2xl bg-white border border-slate-200/90 border-t-2 border-t-[#D7182A] shadow-sm hover:shadow-md hover:-translate-y-1 transition flex flex-col justify-between h-40 group cursor-pointer">
              <div>
                <div class="text-[#D7182A] text-lg mb-2">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <h3 class="text-sm font-bold text-slate-900 group-hover:text-[#D7182A] transition">
                  Evidence Ledger
                </h3>
                <p class="text-[11px] text-slate-400 mt-1 line-clamp-1">Cryptographic tamper-evidence</p>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>05</span>
                <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-[#D7182A] group-hover:text-white transition">&rarr;</span>
              </div>
            </a>

          </div>
        </div>

      </main>

      <!-- Minimal Official Footer -->
      <footer class="border-t border-slate-100 bg-white py-6 text-xs text-slate-400">
        <div class="max-w-[1400px] mx-auto px-6 sm:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p>&copy; 2026 CSM Technologies. All rights reserved. TRELLIS Learning &amp; Knowledge Governance.</p>
          <div class="flex items-center gap-6">
            <a routerLink="/login" class="text-[#008FBB] font-bold hover:underline">TRELLIS Portal Login &rarr;</a>
            <span class="text-slate-300">|</span>
            <span>Bhubaneswar, India</span>
          </div>
        </div>
      </footer>

    </div>
  `,
})
export class CsmLandingComponent {}
