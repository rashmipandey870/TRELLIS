import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-csm-landing',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-[#008FBB] selection:text-white">
      
      <!-- Top Announcement Ribbon -->
      <div class="bg-gradient-to-r from-slate-900 via-[#0B1A2A] to-slate-900 border-b border-slate-800 text-[11px] py-2 px-4 text-center text-slate-400">
        <div class="max-w-7xl mx-auto flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="font-semibold text-slate-200">CMMI Level 5 V2.0 Appraised</span>
            <span class="hidden sm:inline">&bull; 25+ Years of Digital Transformation Excellence</span>
          </div>
          <div class="flex items-center gap-4 text-slate-400">
            <span class="hidden md:inline">Global HQ: Bhubaneswar, India</span>
            <a routerLink="/login" class="text-[#FAA634] hover:underline font-bold flex items-center gap-1">
              <span>Employee &amp; Learner Access &rarr;</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Main Navigation Bar -->
      <header class="sticky top-0 z-50 bg-slate-950/85 backdrop-blur-md border-b border-slate-800/80">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex items-center justify-between h-20">
            
            <!-- CSM Technologies Brand Logo -->
            <a routerLink="/" class="flex items-center gap-3 group">
              <!-- Stylized 3-Slashes Emblem: Inward (Saffron), Outward (Signal Red), Upward (Cerulean) -->
              <div class="relative w-10 h-10 flex items-center justify-center">
                <div class="w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center p-2 shadow-inner group-hover:border-slate-700 transition">
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
                  <span class="text-xl font-black tracking-tight text-white leading-none">CSM</span>
                  <span class="text-xs font-bold text-slate-400 tracking-wider uppercase">Technologies</span>
                </div>
                <span class="text-[9px] font-bold text-[#FAA634] uppercase tracking-widest mt-0.5">
                  Breaking Thought Barriers
                </span>
              </div>
            </a>

            <!-- Corporate Nav Items -->
            <nav class="hidden lg:flex items-center gap-7 text-xs font-bold text-slate-300">
              <a href="#solutions" class="hover:text-white transition">Solutions</a>
              <a href="#ai-foundry" class="hover:text-white transition flex items-center gap-1.5">
                <span>AI Foundry</span>
                <span class="px-1.5 py-0.5 rounded text-[9px] font-black bg-[#008FBB]/20 text-[#008FBB] border border-[#008FBB]/40">NEW</span>
              </a>
              <a href="#industries" class="hover:text-white transition">Industries</a>
              <a href="#certifications" class="hover:text-white transition">Certifications</a>
              <a href="#trellis" class="hover:text-white transition text-[#FAA634]">TRELLIS Portal</a>
            </nav>

            <!-- Action CTAs -->
            <div class="flex items-center gap-3">
              <a 
                routerLink="/login" 
                class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#008FBB] via-[#007499] to-[#005e7c] hover:from-[#007499] hover:to-[#004e69] text-white text-xs font-bold shadow-lg shadow-sky-950/50 transition transform hover:-translate-y-0.5 flex items-center gap-2">
                <span>Sign In to TRELLIS</span>
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </a>
            </div>

          </div>
        </div>
      </header>

      <!-- Hero Section -->
      <section class="relative pt-16 pb-24 overflow-hidden">
        <!-- Background Lighting Glows -->
        <div class="pointer-events-none absolute top-10 left-1/2 -translate-x-1/2 w-[800px] h-[350px] bg-gradient-to-r from-[#008FBB]/15 via-[#FAA634]/10 to-[#D7182A]/10 blur-3xl rounded-full" aria-hidden="true"></div>

        <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          
          <!-- Badge -->
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs text-slate-300 shadow-sm">
            <span class="w-2 h-2 rounded-full bg-[#FAA634]"></span>
            <span class="font-bold text-slate-200">GovTech &bull; Agentic AI &bull; Digital Identity</span>
            <span class="text-slate-500">|</span>
            <span class="text-xs text-[#008FBB] font-mono font-bold">CMMI Level 5 Dev V2.0</span>
          </div>

          <!-- Hero Headline -->
          <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black text-white tracking-tight max-w-4xl mx-auto leading-[1.08]">
            Intelligence you can answer for.
            <span class="block bg-gradient-to-r from-[#FAA634] via-[#D7182A] to-[#008FBB] bg-clip-text text-transparent mt-1">
              Audit. Explain. Sign off on.
            </span>
          </h1>

          <!-- Hero Subtitle -->
          <p class="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Pioneering GovTech, AI Foundry automation, and mission-critical public enterprise architectures for over two decades. Empowering governments, citizens, and modern engineering cohorts.
          </p>

          <!-- Action Buttons -->
          <div class="pt-4 flex flex-wrap items-center justify-center gap-4">
            <a 
              routerLink="/login" 
              class="px-8 py-3.5 rounded-xl bg-gradient-to-r from-[#FAA634] to-[#e09228] hover:from-[#e09228] hover:to-[#c67c1e] text-slate-950 font-black text-sm shadow-xl shadow-amber-950/40 transition transform active:scale-95 flex items-center gap-2">
              <span>Enter TRELLIS Portal</span>
              <span>&rarr;</span>
            </a>

            <a 
              href="#ai-foundry" 
              class="px-7 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800/80 border border-slate-800 text-slate-200 font-bold text-sm transition">
              Explore Enterprise Solutions
            </a>
          </div>

          <!-- Metrics Strip -->
          <div class="pt-16 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-sm">
              <span class="text-3xl font-black text-white block">25+</span>
              <span class="text-xs text-[#FAA634] font-bold block mt-0.5">Years of Innovation</span>
              <span class="text-[11px] text-slate-400 mt-1 block">Founded in 1998, Bhubaneswar</span>
            </div>

            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-sm">
              <span class="text-3xl font-black text-white block">Level 5</span>
              <span class="text-xs text-[#008FBB] font-bold block mt-0.5">CMMI Dev V2.0</span>
              <span class="text-[11px] text-slate-400 mt-1 block">Highest process maturity</span>
            </div>

            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-sm">
              <span class="text-3xl font-black text-white block">1,500+</span>
              <span class="text-xs text-purple-400 font-bold block mt-0.5">Technology Pioneers</span>
              <span class="text-[11px] text-slate-400 mt-1 block">Engineers &amp; domain consultants</span>
            </div>

            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-sm">
              <span class="text-3xl font-black text-white block">40M+</span>
              <span class="text-xs text-emerald-400 font-bold block mt-0.5">Citizens Empowered</span>
              <span class="text-[11px] text-slate-400 mt-1 block">Across 3 continents</span>
            </div>
          </div>

        </div>
      </section>

      <!-- Innovation Pillars: AI Foundry, MOSIP, Mining, Governance -->
      <section id="ai-foundry" class="py-20 bg-slate-900/50 border-y border-slate-800/80">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          
          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <span class="text-xs font-bold uppercase tracking-widest text-[#008FBB]">Core Capabilities</span>
              <h2 class="text-3xl font-black text-white tracking-tight mt-1">
                AI Foundry &amp; Enterprise Architecture
              </h2>
            </div>
            <p class="text-xs text-slate-400 max-w-md">
              From pilot to production: Sandboxed agents, verified inference pipelines, and immutable audit trails that comply with strict government standards.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <!-- Pillar 1: AI Foundry -->
            <div class="p-7 rounded-2xl bg-slate-950 border border-slate-800 hover:border-[#008FBB] transition space-y-4 group">
              <div class="w-12 h-12 rounded-xl bg-sky-950/70 border border-sky-800 flex items-center justify-center text-[#008FBB] font-black text-lg">
                🤖
              </div>
              <h3 class="text-lg font-black text-white group-hover:text-[#008FBB] transition">
                AI Foundry: Pilot to Production
              </h3>
              <p class="text-xs text-slate-400 leading-relaxed">
                Deploy autonomous AI agents that act while human officials decide. Full sandbox verification, guardrails, and role-based policy enforcement across models.
              </p>
              <div class="pt-2 flex flex-wrap gap-1.5 text-[10px] font-mono">
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">Agentic GovTech</span>
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">Audit Trails</span>
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">Pre-Verified</span>
              </div>
            </div>

            <!-- Pillar 2: Digital Identity & MOSIP -->
            <div class="p-7 rounded-2xl bg-slate-950 border border-slate-800 hover:border-[#FAA634] transition space-y-4 group">
              <div class="w-12 h-12 rounded-xl bg-amber-950/70 border border-amber-800 flex items-center justify-center text-[#FAA634] font-black text-lg">
                🆔
              </div>
              <h3 class="text-lg font-black text-white group-hover:text-[#FAA634] transition">
                Digital Identity &amp; MOSIP
              </h3>
              <p class="text-xs text-slate-400 leading-relaxed">
                National-scale biometric identity and accurate welfare delivery. Ensuring transparent, leak-proof citizen registry integration with international privacy standards.
              </p>
              <div class="pt-2 flex flex-wrap gap-1.5 text-[10px] font-mono">
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">MOSIP Partner</span>
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">Welfare Delivery</span>
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">Zero Duplication</span>
              </div>
            </div>

            <!-- Pillar 3: Mining & Mineral Logistics -->
            <div class="p-7 rounded-2xl bg-slate-950 border border-slate-800 hover:border-[#D7182A] transition space-y-4 group">
              <div class="w-12 h-12 rounded-xl bg-rose-950/70 border border-rose-800 flex items-center justify-center text-[#D7182A] font-black text-lg">
                ⛏️
              </div>
              <h3 class="text-lg font-black text-white group-hover:text-[#D7182A] transition">
                Mining Tech &amp; Leakage Prevention
              </h3>
              <p class="text-xs text-slate-400 leading-relaxed">
                Real-time mineral logistics tracking, i3MS digital mines, RFID weighbridge integration, and revenue reconciliation that prevents billions in leaks.
              </p>
              <div class="pt-2 flex flex-wrap gap-1.5 text-[10px] font-mono">
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">IoT Weighbridge</span>
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">i3MS Tech</span>
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">e-Pass Transit</span>
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- Industries We Transform -->
      <section id="industries" class="py-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          
          <div class="text-center space-y-2 max-w-2xl mx-auto">
            <span class="text-xs font-bold uppercase tracking-widest text-[#FAA634]">Sectors &amp; Impact</span>
            <h2 class="text-3xl font-black text-white tracking-tight">
              Transforming Key Economic Drivers
            </h2>
            <p class="text-xs text-slate-400">
              Proven GovTech and enterprise deployments trusted across public administrations and global enterprises.
            </p>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            
            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
              <span class="text-2xl block">🌾</span>
              <h4 class="text-sm font-bold text-white">Agriculture &amp; AgriStack</h4>
              <p class="text-[11px] text-slate-400">Farmer registries, crop insurance automation, and supply chain transparency.</p>
            </div>

            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
              <span class="text-2xl block">🏛️</span>
              <h4 class="text-sm font-bold text-white">Public Services &amp; GovTech</h4>
              <p class="text-[11px] text-slate-400">Citizen service portals, digital revenue records, and paperless administrative workflows.</p>
            </div>

            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
              <span class="text-2xl block">🎓</span>
              <h4 class="text-sm font-bold text-white">Education &amp; Skilling</h4>
              <p class="text-[11px] text-slate-400">Curriculum lifecycle governance, talent spotlight tracking, and sandboxed assessments.</p>
            </div>

            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
              <span class="text-2xl block">🏥</span>
              <h4 class="text-sm font-bold text-white">Healthcare &amp; Diagnostics</h4>
              <p class="text-[11px] text-slate-400">Integrated clinical databases, drug supply monitoring, and telemedicine systems.</p>
            </div>

            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
              <span class="text-2xl block">🏭</span>
              <h4 class="text-sm font-bold text-white">Trade &amp; Industry</h4>
              <p class="text-[11px] text-slate-400">Single window clearance, investor facilitation, and industrial land bank GIS.</p>
            </div>

            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
              <span class="text-2xl block">⛰️</span>
              <h4 class="text-sm font-bold text-white">Mining &amp; Natural Resources</h4>
              <p class="text-[11px] text-slate-400">End-to-end mineral logistics, concession mapping, and royalty reconciliation.</p>
            </div>

            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
              <span class="text-2xl block">🏖️</span>
              <h4 class="text-sm font-bold text-white">Tourism &amp; Culture</h4>
              <p class="text-[11px] text-slate-400">Heritage asset digitisation, tourist booking portals, and smart destination kiosks.</p>
            </div>

            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
              <span class="text-2xl block">🛡️</span>
              <h4 class="text-sm font-bold text-white">Cybersecurity &amp; Auditing</h4>
              <p class="text-[11px] text-slate-400">Vulnerability mitigation, compliance monitoring, and immutable ledger logging.</p>
            </div>

          </div>
        </div>
      </section>

      <!-- TRELLIS Internal Learning & Talent Portal Spotlight Banner -->
      <section id="trellis" class="py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900 via-[#0B1A2A] to-slate-900 p-8 sm:p-12 shadow-2xl">
            
            <div class="pointer-events-none absolute -right-20 -bottom-20 w-80 h-80 rounded-full bg-[#008FBB]/10 blur-3xl"></div>

            <div class="relative z-10 flex flex-col lg:flex-row items-center justify-between gap-8">
              
              <div class="space-y-3 text-center lg:text-left">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FAA634]/10 border border-[#FAA634]/30 text-xs font-bold text-[#FAA634]">
                  <span>🔒 INTERNAL EMPLOYEE &amp; LEARNER GATEWAY</span>
                </div>
                <h3 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
                  TRELLIS: Learning &amp; Knowledge Portal
                </h3>
                <p class="text-xs sm:text-sm text-slate-400 max-w-xl">
                  Authorized gateway for CSM Technology engineers, mentors, and program administrators. Access your assigned cohorts, timed coding sandbox, and AI Practice Lab.
                </p>
                <div class="flex flex-wrap items-center justify-center lg:justify-start gap-4 pt-2 text-xs text-slate-400">
                  <span class="flex items-center gap-1.5">&check; 3 Strictly Enforced Roles</span>
                  <span class="flex items-center gap-1.5">&check; AI Practice Lab</span>
                  <span class="flex items-center gap-1.5">&check; Sandboxed Code Verification</span>
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

      <!-- Footer -->
      <footer class="mt-auto border-t border-slate-800/80 bg-slate-950 py-12 text-xs text-slate-500">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          
          <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="space-y-3">
              <div class="flex items-center gap-2">
                <div class="w-7 h-7 rounded-lg bg-gradient-to-tr from-[#FAA634] via-[#D7182A] to-[#008FBB] flex items-center justify-center text-white font-black text-xs">
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
                <li><a href="#ai-foundry" class="hover:text-slate-300">AI Foundry &amp; Agents</a></li>
                <li><a href="#solutions" class="hover:text-slate-300">MOSIP Digital Identity</a></li>
                <li><a href="#solutions" class="hover:text-slate-300">Mining Logistics (i3MS)</a></li>
                <li><a href="#solutions" class="hover:text-slate-300">Cybersecurity Defence</a></li>
              </ul>
            </div>

            <div>
              <h5 class="font-bold text-slate-200 uppercase tracking-wider text-[11px] mb-3">Portals &amp; Workspaces</h5>
              <ul class="space-y-2 text-[11px]">
                <li><a routerLink="/login" class="text-[#FAA634] hover:underline font-bold">TRELLIS Portal Login</a></li>
                <li><a routerLink="/login" class="hover:text-slate-300">Learner Coding Lab</a></li>
                <li><a routerLink="/login" class="hover:text-slate-300">Mentor Command Center</a></li>
                <li><a routerLink="/login" class="hover:text-slate-300">Admin Governance</a></li>
              </ul>
            </div>

            <div>
              <h5 class="font-bold text-slate-200 uppercase tracking-wider text-[11px] mb-3">Certifications &amp; Standards</h5>
              <p class="text-[11px] text-slate-400 leading-relaxed">
                CMMI Level 5 Dev V2.0 &bull; ISO 9001:2015 &bull; ISO 27001:2013 &bull; CMMI SVC Level 3.
              </p>
              <div class="pt-3 text-[11px]">
                Email: <span class="text-slate-300 font-mono">contact&#64;csm.tech</span>
              </div>
            </div>
          </div>

          <div class="pt-8 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px]">
            <p>&copy; 2026 CSM Technologies. All rights reserved. Breaking Thought Barriers.</p>
            <div class="flex items-center gap-4 text-slate-400">
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
