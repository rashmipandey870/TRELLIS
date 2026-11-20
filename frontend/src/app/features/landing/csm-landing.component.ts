import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-csm-landing',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="min-h-screen bg-white text-slate-800 flex flex-col font-sans selection:bg-[#008FBB] selection:text-white">
      
      <!-- Top Announcement Ribbon (Official CSM Header Style) -->
      <div class="bg-slate-50 border-b border-slate-200 text-[11px] py-2 px-4 text-slate-600">
        <div class="max-w-7xl mx-auto flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="font-bold text-slate-800">CMMI Level 5 V2.0 Appraised</span>
            <span class="hidden sm:inline text-slate-400">&bull;</span>
            <span class="hidden sm:inline">25+ Years of Digital Transformation Excellence</span>
          </div>
          <div class="flex items-center gap-4 text-slate-500 font-medium">
            <span class="hidden md:inline">Global HQ: Bhubaneswar, India</span>
            <span class="hidden md:inline text-slate-300">|</span>
            <a routerLink="/login" class="text-[#FAA634] hover:text-[#d48419] font-bold flex items-center gap-1 transition">
              <span>Employee &amp; Learner Access &rarr;</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Main Navigation Bar (Clean White, Glassmorphic Shadow) -->
      <header class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex items-center justify-between h-20">
            
            <!-- CSM Technologies Brand Logo -->
            <a routerLink="/" class="flex items-center gap-3 group">
              <!-- Stylized 3-Slashes Emblem: Inward (Saffron), Outward (Signal Red), Upward (Cerulean) -->
              <div class="relative w-11 h-11 flex items-center justify-center">
                <div class="w-11 h-11 rounded-xl bg-slate-50 border border-slate-200 shadow-sm flex items-center justify-center p-2 group-hover:border-[#008FBB] transition">
                  <svg class="w-full h-full" viewBox="0 0 40 40" fill="none">
                    <!-- Saffron Slash (Inward) -->
                    <rect x="6" y="24" width="7" height="12" rx="3.5" transform="rotate(-30 6 24)" fill="#FAA634" />
                    <!-- Signal Red Slash (Outward) -->
                    <rect x="16" y="16" width="7" height="18" rx="3.5" transform="rotate(-30 16 16)" fill="#D7182A" />
                    <!-- Cerulean Slash (Upward) -->
                    <rect x="26" y="8" width="7" height="24" rx="3.5" transform="rotate(-30 26 8)" fill="#008FBB" />
                  </svg>
                </div>
              </div>

              <div class="flex flex-col">
                <div class="flex items-center gap-1.5">
                  <span class="text-xl font-black tracking-tight text-slate-900 leading-none">CSM</span>
                  <span class="text-xs font-bold text-slate-600 tracking-wider uppercase">Technologies</span>
                </div>
                <span class="text-[9px] font-bold text-[#FAA634] uppercase tracking-widest mt-0.5">
                  Breaking Thought Barriers
                </span>
              </div>
            </a>

            <!-- Corporate Nav Items -->
            <nav class="hidden lg:flex items-center gap-8 text-xs font-bold text-slate-600">
              <a href="#solutions" class="hover:text-[#008FBB] transition">Solutions</a>
              <a href="#ai-foundry" class="hover:text-[#008FBB] transition flex items-center gap-1.5">
                <span>AI Foundry</span>
                <span class="px-1.5 py-0.5 rounded text-[9px] font-black bg-sky-100 text-[#008FBB] border border-sky-200">NEW</span>
              </a>
              <a href="#industries" class="hover:text-[#008FBB] transition">Industries</a>
              <a href="#certifications" class="hover:text-[#008FBB] transition">Certifications</a>
              <a href="#trellis" class="hover:text-[#FAA634] transition text-amber-600">TRELLIS Portal</a>
            </nav>

            <!-- Action CTAs -->
            <div class="flex items-center gap-3">
              <a 
                routerLink="/login" 
                class="px-5 py-2.5 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-white text-xs font-bold shadow-md shadow-sky-900/10 transition transform hover:-translate-y-0.5 flex items-center gap-2">
                <span>Sign In to TRELLIS</span>
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </a>
            </div>

          </div>
        </div>
      </header>

      <!-- Hero Section (Clean Crisp White, High-Impact Typography) -->
      <section class="relative pt-16 pb-24 overflow-hidden bg-white">
        <!-- Subtle Ambient Background Glows -->
        <div class="pointer-events-none absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[400px] bg-gradient-to-r from-sky-100/50 via-amber-50/40 to-rose-50/30 blur-3xl rounded-full" aria-hidden="true"></div>

        <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          
          <!-- Pill Badge -->
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-50 border border-slate-200 text-xs text-slate-700 shadow-sm">
            <span class="w-2 h-2 rounded-full bg-[#FAA634]"></span>
            <span class="font-bold">GovTech &bull; Agentic AI &bull; Digital Identity</span>
            <span class="text-slate-300">|</span>
            <span class="text-xs text-[#008FBB] font-mono font-bold">CMMI Level 5 Dev V2.0</span>
          </div>

          <!-- Hero Headline -->
          <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black text-slate-950 tracking-tight max-w-4xl mx-auto leading-[1.08]">
            Intelligence you can answer for.
            <span class="block bg-gradient-to-r from-[#FAA634] via-[#D7182A] to-[#008FBB] bg-clip-text text-transparent mt-1">
              Audit. Explain. Sign off on.
            </span>
          </h1>

          <!-- Hero Subtitle -->
          <p class="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Pioneering GovTech, AI Foundry automation, and mission-critical public enterprise architectures for over two decades. Empowering governments, citizens, and modern engineering cohorts.
          </p>

          <!-- Action Buttons -->
          <div class="pt-4 flex flex-wrap items-center justify-center gap-4">
            <a 
              routerLink="/login" 
              class="px-8 py-3.5 rounded-xl bg-gradient-to-r from-[#FAA634] to-[#e09228] hover:from-[#e09228] hover:to-[#c67c1e] text-slate-950 font-black text-sm shadow-lg shadow-amber-500/20 transition transform active:scale-95 flex items-center gap-2">
              <span>Enter TRELLIS Portal</span>
              <span>&rarr;</span>
            </a>

            <a 
              href="#ai-foundry" 
              class="px-7 py-3.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 font-bold text-sm shadow-sm transition">
              Explore Enterprise Solutions
            </a>
          </div>

          <!-- Metrics Strip (Clean White Cards with Soft Borders) -->
          <div class="pt-16 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
            <div class="p-6 rounded-2xl bg-slate-50/80 border border-slate-200/90 shadow-sm hover:border-[#FAA634] transition">
              <span class="text-3xl sm:text-4xl font-black text-slate-900 block">25+</span>
              <span class="text-xs text-[#FAA634] font-bold block mt-1">Years of Innovation</span>
              <span class="text-[11px] text-slate-500 mt-1 block">Founded in 1998, Bhubaneswar</span>
            </div>

            <div class="p-6 rounded-2xl bg-slate-50/80 border border-slate-200/90 shadow-sm hover:border-[#008FBB] transition">
              <span class="text-3xl sm:text-4xl font-black text-slate-900 block">Level 5</span>
              <span class="text-xs text-[#008FBB] font-bold block mt-1">CMMI Dev V2.0</span>
              <span class="text-[11px] text-slate-500 mt-1 block">Highest process maturity</span>
            </div>

            <div class="p-6 rounded-2xl bg-slate-50/80 border border-slate-200/90 shadow-sm hover:border-purple-500 transition">
              <span class="text-3xl sm:text-4xl font-black text-slate-900 block">1,500+</span>
              <span class="text-xs text-purple-700 font-bold block mt-1">Technology Pioneers</span>
              <span class="text-[11px] text-slate-500 mt-1 block">Engineers &amp; domain consultants</span>
            </div>

            <div class="p-6 rounded-2xl bg-slate-50/80 border border-slate-200/90 shadow-sm hover:border-emerald-500 transition">
              <span class="text-3xl sm:text-4xl font-black text-slate-900 block">40M+</span>
              <span class="text-xs text-emerald-700 font-bold block mt-1">Citizens Empowered</span>
              <span class="text-[11px] text-slate-500 mt-1 block">Across 3 continents</span>
            </div>
          </div>

        </div>
      </section>

      <!-- Innovation Pillars: AI Foundry, MOSIP, Mining, Governance (Soft Light Gray Canvas) -->
      <section id="ai-foundry" class="py-20 bg-slate-50/70 border-y border-slate-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          
          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <span class="text-xs font-bold uppercase tracking-widest text-[#008FBB]">Core Capabilities</span>
              <h2 class="text-3xl font-black text-slate-950 tracking-tight mt-1">
                AI Foundry &amp; Enterprise Architecture
              </h2>
            </div>
            <p class="text-xs text-slate-600 max-w-md">
              From pilot to production: Sandboxed agents, verified inference pipelines, and immutable audit trails that comply with strict government standards.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <!-- Pillar 1: AI Foundry -->
            <div class="p-8 rounded-2xl bg-white border border-slate-200/90 hover:border-[#008FBB] shadow-sm hover:shadow-md transition space-y-4 group">
              <div class="w-12 h-12 rounded-xl bg-sky-50 border border-sky-200 flex items-center justify-center text-[#008FBB] font-black text-lg">
                🤖
              </div>
              <h3 class="text-lg font-black text-slate-900 group-hover:text-[#008FBB] transition">
                AI Foundry: Pilot to Production
              </h3>
              <p class="text-xs text-slate-600 leading-relaxed">
                Deploy autonomous AI agents that act while human officials decide. Full sandbox verification, guardrails, and role-based policy enforcement across models.
              </p>
              <div class="pt-2 flex flex-wrap gap-1.5 text-[10px] font-mono">
                <span class="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-slate-700 font-bold">Agentic GovTech</span>
                <span class="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-slate-700 font-bold">Audit Trails</span>
                <span class="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-slate-700 font-bold">Pre-Verified</span>
              </div>
            </div>

            <!-- Pillar 2: Digital Identity & MOSIP -->
            <div class="p-8 rounded-2xl bg-white border border-slate-200/90 hover:border-[#FAA634] shadow-sm hover:shadow-md transition space-y-4 group">
              <div class="w-12 h-12 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center text-[#FAA634] font-black text-lg">
                🆔
              </div>
              <h3 class="text-lg font-black text-slate-900 group-hover:text-[#FAA634] transition">
                Digital Identity &amp; MOSIP
              </h3>
              <p class="text-xs text-slate-600 leading-relaxed">
                National-scale biometric identity and accurate welfare delivery. Ensuring transparent, leak-proof citizen registry integration with international privacy standards.
              </p>
              <div class="pt-2 flex flex-wrap gap-1.5 text-[10px] font-mono">
                <span class="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-slate-700 font-bold">MOSIP Partner</span>
                <span class="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-slate-700 font-bold">Welfare Delivery</span>
                <span class="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-slate-700 font-bold">Zero Duplication</span>
              </div>
            </div>

            <!-- Pillar 3: Mining & Mineral Logistics -->
            <div class="p-8 rounded-2xl bg-white border border-slate-200/90 hover:border-[#D7182A] shadow-sm hover:shadow-md transition space-y-4 group">
              <div class="w-12 h-12 rounded-xl bg-rose-50 border border-rose-200 flex items-center justify-center text-[#D7182A] font-black text-lg">
                ⛏️
              </div>
              <h3 class="text-lg font-black text-slate-900 group-hover:text-[#D7182A] transition">
                Mining Tech &amp; Leakage Prevention
              </h3>
              <p class="text-xs text-slate-600 leading-relaxed">
                Real-time mineral logistics tracking, i3MS digital mines, RFID weighbridge integration, and revenue reconciliation that prevents billions in leaks.
              </p>
              <div class="pt-2 flex flex-wrap gap-1.5 text-[10px] font-mono">
                <span class="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-slate-700 font-bold">IoT Weighbridge</span>
                <span class="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-slate-700 font-bold">i3MS Tech</span>
                <span class="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-slate-700 font-bold">e-Pass Transit</span>
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- Industries We Transform (Crisp White Grid) -->
      <section id="industries" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          
          <div class="text-center space-y-2 max-w-2xl mx-auto">
            <span class="text-xs font-bold uppercase tracking-widest text-[#FAA634]">Sectors &amp; Impact</span>
            <h2 class="text-3xl font-black text-slate-950 tracking-tight">
              Transforming Key Economic Drivers
            </h2>
            <p class="text-xs text-slate-600">
              Proven GovTech and enterprise deployments trusted across public administrations and global enterprises.
            </p>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            
            <div class="p-6 rounded-2xl bg-slate-50/70 border border-slate-200/80 hover:border-[#008FBB] transition space-y-2">
              <span class="text-2xl block">🌾</span>
              <h4 class="text-sm font-bold text-slate-900">Agriculture &amp; AgriStack</h4>
              <p class="text-[11px] text-slate-500 leading-relaxed">Farmer registries, crop insurance automation, and supply chain transparency.</p>
            </div>

            <div class="p-6 rounded-2xl bg-slate-50/70 border border-slate-200/80 hover:border-[#008FBB] transition space-y-2">
              <span class="text-2xl block">🏛️</span>
              <h4 class="text-sm font-bold text-slate-900">Public Services &amp; GovTech</h4>
              <p class="text-[11px] text-slate-500 leading-relaxed">Citizen service portals, digital revenue records, and paperless administrative workflows.</p>
            </div>

            <div class="p-6 rounded-2xl bg-slate-50/70 border border-slate-200/80 hover:border-[#FAA634] transition space-y-2">
              <span class="text-2xl block">🎓</span>
              <h4 class="text-sm font-bold text-slate-900">Education &amp; Skilling</h4>
              <p class="text-[11px] text-slate-500 leading-relaxed">Curriculum lifecycle governance, talent spotlight tracking, and sandboxed assessments.</p>
            </div>

            <div class="p-6 rounded-2xl bg-slate-50/70 border border-slate-200/80 hover:border-[#D7182A] transition space-y-2">
              <span class="text-2xl block">🏥</span>
              <h4 class="text-sm font-bold text-slate-900">Healthcare &amp; Diagnostics</h4>
              <p class="text-[11px] text-slate-500 leading-relaxed">Integrated clinical databases, drug supply monitoring, and telemedicine systems.</p>
            </div>

            <div class="p-6 rounded-2xl bg-slate-50/70 border border-slate-200/80 hover:border-[#008FBB] transition space-y-2">
              <span class="text-2xl block">🏭</span>
              <h4 class="text-sm font-bold text-slate-900">Trade &amp; Industry</h4>
              <p class="text-[11px] text-slate-500 leading-relaxed">Single window clearance, investor facilitation, and industrial land bank GIS.</p>
            </div>

            <div class="p-6 rounded-2xl bg-slate-50/70 border border-slate-200/80 hover:border-[#FAA634] transition space-y-2">
              <span class="text-2xl block">⛰️</span>
              <h4 class="text-sm font-bold text-slate-900">Mining &amp; Natural Resources</h4>
              <p class="text-[11px] text-slate-500 leading-relaxed">End-to-end mineral logistics, concession mapping, and royalty reconciliation.</p>
            </div>

            <div class="p-6 rounded-2xl bg-slate-50/70 border border-slate-200/80 hover:border-[#008FBB] transition space-y-2">
              <span class="text-2xl block">🏖️</span>
              <h4 class="text-sm font-bold text-slate-900">Tourism &amp; Culture</h4>
              <p class="text-[11px] text-slate-500 leading-relaxed">Heritage asset digitisation, tourist booking portals, and smart destination kiosks.</p>
            </div>

            <div class="p-6 rounded-2xl bg-slate-50/70 border border-slate-200/80 hover:border-[#D7182A] transition space-y-2">
              <span class="text-2xl block">🛡️</span>
              <h4 class="text-sm font-bold text-slate-900">Cybersecurity &amp; Auditing</h4>
              <p class="text-[11px] text-slate-500 leading-relaxed">Vulnerability mitigation, compliance monitoring, and immutable ledger logging.</p>
            </div>

          </div>
        </div>
      </section>

      <!-- TRELLIS Internal Learning & Talent Portal Spotlight Banner -->
      <section id="trellis" class="py-16 bg-slate-50/60 border-t border-slate-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-8 sm:p-12 shadow-xl">
            
            <div class="pointer-events-none absolute -right-20 -bottom-20 w-80 h-80 rounded-full bg-sky-100/60 blur-3xl"></div>

            <div class="relative z-10 flex flex-col lg:flex-row items-center justify-between gap-8">
              
              <div class="space-y-3 text-center lg:text-left">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-xs font-bold text-[#FAA634]">
                  <span>🔒 INTERNAL EMPLOYEE &amp; LEARNER GATEWAY</span>
                </div>
                <h3 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
                  TRELLIS: Learning &amp; Knowledge Portal
                </h3>
                <p class="text-xs sm:text-sm text-slate-600 max-w-xl">
                  Authorized gateway for CSM Technology engineers, mentors, and program administrators. Access your assigned cohorts, timed coding sandbox, and AI Practice Lab.
                </p>
                <div class="flex flex-wrap items-center justify-center lg:justify-start gap-4 pt-2 text-xs text-slate-500 font-semibold">
                  <span class="flex items-center gap-1.5 text-emerald-600">&check; 3 Strictly Enforced Roles</span>
                  <span class="flex items-center gap-1.5 text-[#008FBB]">&check; AI Practice Lab</span>
                  <span class="flex items-center gap-1.5 text-[#FAA634]">&check; Sandboxed Code Verification</span>
                </div>
              </div>

              <div class="shrink-0 flex flex-col sm:flex-row items-center gap-3">
                <a 
                  routerLink="/login" 
                  class="px-8 py-3.5 rounded-xl bg-gradient-to-r from-[#FAA634] via-[#D7182A] to-[#008FBB] hover:opacity-95 text-white font-black text-sm shadow-xl transition transform hover:scale-105 active:scale-95 text-center">
                  Proceed to Login &rarr;
                </a>
              </div>

            </div>
          </div>
        </div>
      </section>

      <!-- Footer (Professional Corporate Footer matching CSM Standards) -->
      <footer class="mt-auto border-t border-slate-200 bg-slate-900 text-xs text-slate-400 py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          
          <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="space-y-3">
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-[#FAA634] via-[#D7182A] to-[#008FBB] flex items-center justify-center text-white font-black text-xs shadow-sm">
                  T
                </div>
                <span class="font-bold text-white text-sm">CSM Technologies</span>
              </div>
              <p class="text-[11px] text-slate-400 leading-relaxed">
                Headquartered in Bhubaneswar, India. Transforming governance and enterprise operations through cutting-edge technology and human-centric design.
              </p>
            </div>

            <div>
              <h5 class="font-bold text-slate-200 uppercase tracking-wider text-[11px] mb-3">Enterprise Capabilities</h5>
              <ul class="space-y-2 text-[11px]">
                <li><a href="#ai-foundry" class="hover:text-white transition">AI Foundry &amp; Agents</a></li>
                <li><a href="#solutions" class="hover:text-white transition">MOSIP Digital Identity</a></li>
                <li><a href="#solutions" class="hover:text-white transition">Mining Logistics (i3MS)</a></li>
                <li><a href="#solutions" class="hover:text-white transition">Cybersecurity Defence</a></li>
              </ul>
            </div>

            <div>
              <h5 class="font-bold text-slate-200 uppercase tracking-wider text-[11px] mb-3">Portals &amp; Workspaces</h5>
              <ul class="space-y-2 text-[11px]">
                <li><a routerLink="/login" class="text-[#FAA634] hover:underline font-bold">TRELLIS Portal Login</a></li>
                <li><a routerLink="/login" class="hover:text-white transition">Learner Coding Lab</a></li>
                <li><a routerLink="/login" class="hover:text-white transition">Mentor Command Center</a></li>
                <li><a routerLink="/login" class="hover:text-white transition">Admin Governance</a></li>
              </ul>
            </div>

            <div>
              <h5 class="font-bold text-slate-200 uppercase tracking-wider text-[11px] mb-3">Certifications &amp; Standards</h5>
              <p class="text-[11px] text-slate-400 leading-relaxed">
                CMMI Level 5 Dev V2.0 &bull; ISO 9001:2015 &bull; ISO 27001:2013 &bull; CMMI SVC Level 3.
              </p>
              <div class="pt-3 text-[11px]">
                Corporate Email: <span class="text-slate-200 font-mono">contact&#64;csm.tech</span>
              </div>
            </div>
          </div>

          <div class="pt-8 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px]">
            <p>&copy; 2026 CSM Technologies. All rights reserved. Breaking Thought Barriers.</p>
            <div class="flex items-center gap-4 text-slate-500">
              <a href="#" class="hover:text-slate-300">Privacy Policy</a>
              <span>&bull;</span>
              <a href="#" class="hover:text-slate-300">Terms of Service</a>
              <span>&bull;</span>
              <a href="#" class="hover:text-slate-300">Disclaimer</a>
            </div>
          </div>

        </div>
      </footer>

    </div>
  `,
})
export class CsmLandingComponent {}
