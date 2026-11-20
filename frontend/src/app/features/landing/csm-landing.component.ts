import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-csm-landing',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="min-h-screen bg-white text-slate-900 flex flex-col font-sans selection:bg-[#008FBB] selection:text-white relative overflow-x-hidden">
      
      <!-- Ambient Diagonal Speed-Trails & Subtle Technical Grid (Exact csm.tech Visual Texture) -->
      <div class="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <!-- Fine Subtle Grid Pattern -->
        <div class="absolute inset-0 opacity-[0.035]" 
             style="background-image: linear-gradient(to right, #0f172a 1px, transparent 1px), linear-gradient(to bottom, #0f172a 1px, transparent 1px); background-size: 40px 40px;">
        </div>

        <!-- Official CSM Diagonal Streaks (Orange, Cyan, Red) Shooting Upward to Right -->
        <svg class="absolute -right-16 top-0 w-[1200px] h-[950px] opacity-45 pointer-events-none" viewBox="0 0 1200 950" fill="none">
          <line x1="180" y1="950" x2="880" y2="0" stroke="url(#streak-cyan)" stroke-width="2.5" stroke-linecap="round" />
          <line x1="320" y1="950" x2="1020" y2="0" stroke="url(#streak-orange)" stroke-width="2" stroke-linecap="round" />
          <line x1="480" y1="950" x2="1180" y2="0" stroke="url(#streak-cyan)" stroke-width="1.5" stroke-linecap="round" />
          <line x1="100" y1="950" x2="800" y2="0" stroke="url(#streak-red)" stroke-width="1.2" stroke-linecap="round" />
          <line x1="40" y1="950" x2="740" y2="0" stroke="url(#streak-soft)" stroke-width="3" stroke-linecap="round" opacity="0.5" />
          <line x1="420" y1="950" x2="1120" y2="0" stroke="url(#streak-soft)" stroke-width="4" stroke-linecap="round" opacity="0.35" />
          <defs>
            <linearGradient id="streak-cyan" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#008FBB" stop-opacity="0" />
              <stop offset="50%" stop-color="#008FBB" stop-opacity="0.85" />
              <stop offset="100%" stop-color="#008FBB" stop-opacity="0" />
            </linearGradient>
            <linearGradient id="streak-orange" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#FAA634" stop-opacity="0" />
              <stop offset="50%" stop-color="#FAA634" stop-opacity="0.9" />
              <stop offset="100%" stop-color="#FAA634" stop-opacity="0" />
            </linearGradient>
            <linearGradient id="streak-red" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#D7182A" stop-opacity="0" />
              <stop offset="50%" stop-color="#D7182A" stop-opacity="0.75" />
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

      <!-- Top Navbar (Matching Official csm.tech Navigation Exactly) -->
      <header class="relative z-30 bg-white/95 backdrop-blur-md border-b border-slate-100">
        <div class="max-w-[1440px] mx-auto px-6 sm:px-10">
          <div class="flex items-center justify-between h-20">
            
            <!-- Left: CSM Brand Logo + MOSIP PARTNER Emblem -->
            <div class="flex items-center gap-8">
              <a routerLink="/" class="flex items-center gap-1.5 focus:outline-none group">
                <!-- 3 Slashes (Orange, Red, Teal) -->
                <div class="flex items-center space-x-[2.5px] font-black italic tracking-tighter text-2xl select-none">
                  <span class="text-[#FAA634] font-black -rotate-12 inline-block">/</span>
                  <span class="text-[#D7182A] font-black -rotate-12 inline-block">/</span>
                  <span class="text-[#008FBB] font-black -rotate-12 inline-block">/</span>
                </div>
                <span class="text-2xl font-black italic tracking-tight text-slate-900 ml-1">CSM</span>
                <span class="text-[9px] font-bold text-slate-400 uppercase -mt-3">TM</span>
              </a>

              <!-- MOSIP Partner Logo Badge -->
              <div class="hidden sm:flex items-center gap-2 pl-4 border-l border-slate-200">
                <div class="w-6 h-6 rounded-full border border-slate-200 flex items-center justify-center p-0.5">
                  <div class="w-full h-full rounded-full bg-gradient-to-tr from-[#FAA634] via-[#D7182A] to-[#008FBB]"></div>
                </div>
                <div class="flex flex-col text-[9px] leading-tight font-extrabold tracking-wider text-slate-700">
                  <span>MOSIP</span>
                  <span class="text-[7.5px] font-semibold text-slate-400 tracking-widest">PARTNER</span>
                </div>
              </div>
            </div>

            <!-- Center Navigation Links (Matching Official CSM Header) -->
            <nav class="hidden lg:flex items-center gap-9 text-[13.5px] font-medium text-slate-700">
              <a routerLink="/login" class="hover:text-slate-950 transition cursor-pointer">Platforms</a>
              <a routerLink="/login" class="hover:text-slate-950 transition cursor-pointer">Industries</a>
              <a routerLink="/login" class="hover:text-slate-950 transition cursor-pointer">Services</a>
              <a routerLink="/login" class="hover:text-slate-950 transition cursor-pointer">Company</a>
              <a routerLink="/login" class="hover:text-slate-950 transition cursor-pointer">Careers</a>
              <a routerLink="/login" class="hover:text-slate-950 transition cursor-pointer">Investors</a>
            </nav>

            <!-- Right Controls: Search, Language Switcher, Contact / L&K Sign In -->
            <div class="flex items-center gap-4">
              <!-- Search Icon -->
              <button type="button" routerLink="/login" aria-label="Search" class="p-2 text-slate-600 hover:text-slate-950 transition">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>

              <!-- Language Pill (IN / AM / AF) -->
              <div class="hidden sm:flex items-center bg-slate-100 rounded-full p-1 text-[11px] font-bold text-slate-600">
                <span class="px-2.5 py-0.5 rounded-full bg-slate-950 text-white shadow-xs">IN</span>
                <span class="px-2 py-0.5 hover:text-slate-950 cursor-pointer">AM</span>
                <span class="px-2 py-0.5 hover:text-slate-950 cursor-pointer">AF</span>
              </div>

              <!-- Official "Contact ->" Pill Button (Direct Portal Entry) -->
              <a 
                routerLink="/login" 
                class="px-5 py-2.5 rounded-full bg-slate-950 hover:bg-slate-850 text-white text-xs font-semibold shadow-xs transition flex items-center gap-2">
                <span>Contact</span>
                <span>&rarr;</span>
              </a>

              <!-- L&K Platform Direct Button -->
              <a 
                routerLink="/login" 
                class="hidden md:flex px-4 py-2.5 rounded-full bg-sky-50 hover:bg-sky-100 text-[#008FBB] border border-sky-200 text-xs font-bold transition items-center gap-1.5">
                <span>L&amp;K Portal</span>
                <span>&rarr;</span>
              </a>

              <!-- Hamburger Menu Icon -->
              <button type="button" routerLink="/login" aria-label="Menu" class="p-2 text-slate-700 hover:text-slate-950 transition">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>

          </div>
        </div>
      </header>

      <!-- Hero Main Section (Matches Official csm.tech Typography, Gradient & Layout) -->
      <main class="relative z-10 flex-1 flex flex-col justify-between max-w-[1440px] w-full mx-auto px-6 sm:px-10 pt-16 sm:pt-24 pb-12">
        
        <!-- Big Hero Content -->
        <div class="space-y-8 max-w-4xl">
          
          <!-- Headline: "Intelligence you can audit." with Official Multi-Color Gradient on "audit." -->
          <h1 class="text-5xl sm:text-7xl lg:text-[100px] font-black text-slate-950 tracking-tight leading-[1.03]">
            Intelligence you<br />
            can <span class="bg-gradient-to-r from-[#FAA634] via-[#D7182A] to-[#008FBB] bg-clip-text text-transparent">audit.</span>
          </h1>

          <!-- Subheadline & Action Buttons Row -->
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8 pt-2">
            
            <!-- Description Paragraph (Exact CSM Official Copy) -->
            <p class="text-base sm:text-lg text-slate-600 max-w-lg leading-relaxed font-normal">
              Every barrier starts in the mind. We break it there first, then build AI that governments and enterprises can trust in the real world.
            </p>

            <!-- Dual Action CTAs -->
            <div class="flex flex-wrap items-center gap-4 shrink-0">
              <a 
                routerLink="/login" 
                class="px-7 py-3.5 rounded-xl bg-[#243949] hover:bg-[#1a2b38] text-white text-sm font-semibold shadow-lg shadow-slate-900/10 transition flex items-center gap-2">
                <span>See what we build</span>
                <span class="text-emerald-400 font-bold">&rarr;</span>
              </a>

              <a 
                routerLink="/login" 
                class="px-7 py-3.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-300 text-slate-800 text-sm font-semibold shadow-xs transition">
                Talk to an expert
              </a>
            </div>

          </div>

        </div>

        <!-- Vertical Scroll Indicator on Right (Official csm.tech element) -->
        <div class="hidden lg:flex items-center gap-2 absolute right-10 top-1/2 -translate-y-1/2 rotate-90 origin-right text-[10px] uppercase font-bold tracking-widest text-slate-400">
          <span>SCROLL</span>
          <div class="w-8 h-[1px] bg-slate-300"></div>
        </div>

        <!-- Bottom 5 Cards Strip (AI Foundry, Agentic GovTech, Digital Identity, Mining Technology, Cybersecurity) -->
        <div class="pt-20 sm:pt-28">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            
            <!-- Card 01: AI Foundry -->
            <a routerLink="/login" class="p-5 rounded-2xl bg-white border border-slate-200/90 border-t-2 border-t-[#008FBB] shadow-xs hover:shadow-md hover:-translate-y-1 transition flex flex-col justify-between h-40 group cursor-pointer">
              <div>
                <div class="text-[#008FBB] text-lg mb-2">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                </div>
                <h3 class="text-sm font-bold text-slate-900 group-hover:text-[#008FBB] transition">
                  AI Foundry
                </h3>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>01</span>
                <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-[#008FBB] group-hover:text-white transition">&rarr;</span>
              </div>
            </a>

            <!-- Card 02: Agentic GovTech -->
            <a routerLink="/login" class="p-5 rounded-2xl bg-white border border-slate-200/90 border-t-2 border-t-[#00BCD4] shadow-xs hover:shadow-md hover:-translate-y-1 transition flex flex-col justify-between h-40 group cursor-pointer">
              <div>
                <div class="text-[#00BCD4] text-lg mb-2">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <h3 class="text-sm font-bold text-slate-900 group-hover:text-[#00BCD4] transition">
                  Agentic GovTech
                </h3>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>02</span>
                <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-[#00BCD4] group-hover:text-white transition">&rarr;</span>
              </div>
            </a>

            <!-- Card 03: Digital Identity -->
            <a routerLink="/login" class="p-5 rounded-2xl bg-white border border-slate-200/90 border-t-2 border-t-[#FAA634] shadow-xs hover:shadow-md hover:-translate-y-1 transition flex flex-col justify-between h-40 group cursor-pointer">
              <div>
                <div class="text-[#FAA634] text-lg mb-2">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 004 11a7.962 7.962 0 001.378 4.542" />
                  </svg>
                </div>
                <h3 class="text-sm font-bold text-slate-900 group-hover:text-[#FAA634] transition">
                  Digital Identity
                </h3>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>03</span>
                <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-[#FAA634] group-hover:text-white transition">&rarr;</span>
              </div>
            </a>

            <!-- Card 04: Mining Technology -->
            <a routerLink="/login" class="p-5 rounded-2xl bg-white border border-slate-200/90 border-t-2 border-t-[#EAB308] shadow-xs hover:shadow-md hover:-translate-y-1 transition flex flex-col justify-between h-40 group cursor-pointer">
              <div>
                <div class="text-[#EAB308] text-lg mb-2">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 class="text-sm font-bold text-slate-900 group-hover:text-[#EAB308] transition">
                  Mining Technology
                </h3>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>04</span>
                <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-[#EAB308] group-hover:text-white transition">&rarr;</span>
              </div>
            </a>

            <!-- Card 05: Cybersecurity -->
            <a routerLink="/login" class="p-5 rounded-2xl bg-white border border-slate-200/90 border-t-2 border-t-[#D7182A] shadow-xs hover:shadow-md hover:-translate-y-1 transition flex flex-col justify-between h-40 group cursor-pointer">
              <div>
                <div class="text-[#D7182A] text-lg mb-2">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <h3 class="text-sm font-bold text-slate-900 group-hover:text-[#D7182A] transition">
                  Cybersecurity
                </h3>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>05</span>
                <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-[#D7182A] group-hover:text-white transition">&rarr;</span>
              </div>
            </a>

          </div>
        </div>

      </main>

      <!-- Official Clean Minimal Footer -->
      <footer class="border-t border-slate-100 bg-white py-6 text-xs text-slate-400">
        <div class="max-w-[1440px] mx-auto px-6 sm:px-10 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p>&copy; 2026 CSM Technologies. All rights reserved.</p>
          <div class="flex items-center gap-6">
            <a routerLink="/login" class="text-[#008FBB] font-bold hover:underline">Sign In to TRELLIS L&amp;K Portal &rarr;</a>
            <span class="text-slate-300">|</span>
            <span>Bhubaneswar &bull; Dubai &bull; Nairobi &bull; Indianapolis</span>
          </div>
        </div>
      </footer>

    </div>
  `,
})
export class CsmLandingComponent {}
