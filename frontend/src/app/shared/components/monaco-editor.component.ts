import {
  AfterViewInit,
  Component,
  ElementRef,
  EventEmitter,
  Input,
  OnChanges,
  OnDestroy,
  Output,
  SimpleChanges,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

declare global {
  interface Window {
    require?: any;
    monaco?: any;
  }
}

let monacoLoadingPromise: Promise<any> | null = null;

function loadMonacoEditor(): Promise<any> {
  if (typeof window === 'undefined') return Promise.reject('SSR not supported');
  if (window.monaco) return Promise.resolve(window.monaco);
  if (monacoLoadingPromise) return monacoLoadingPromise;

  monacoLoadingPromise = new Promise((resolve, reject) => {
    const onGotAmdLoader = () => {
      window.require.config({ paths: { vs: '/assets/monaco/vs' } });
      window.require(['vs/editor/editor.main'], () => {
        resolve(window.monaco);
      });
    };

    if (window.require && window.require.config) {
      onGotAmdLoader();
      return;
    }

    const loaderScript = document.createElement('script');
    loaderScript.type = 'text/javascript';
    loaderScript.src = '/assets/monaco/vs/loader.js';
    loaderScript.addEventListener('load', onGotAmdLoader);
    loaderScript.addEventListener('error', (err) => reject(err));
    document.body.appendChild(loaderScript);
  });

  return monacoLoadingPromise;
}

@Component({
  selector: 'app-monaco-editor',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="flex flex-col h-full border border-slate-200 rounded-2xl overflow-hidden bg-white shadow-sm">
      <!-- Top Control Bar -->
      <div class="px-3 py-2 bg-slate-50 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2 text-xs">
        <div class="flex items-center gap-2">
          <label class="text-[11px] font-bold uppercase text-slate-500">Language:</label>
          <select
            [ngModel]="language"
            (ngModelChange)="onLanguageChange($event)"
            class="px-2.5 py-1 bg-white border border-slate-300 rounded-lg text-xs font-semibold text-slate-800 focus:outline-none focus:ring-1 focus:ring-[#008FBB]">
            <option value="python">Python 3</option>
            <option value="java">Java 21</option>
            <option value="javascript">JavaScript</option>
            <option value="cpp">C++ 20</option>
            <option value="c">C 17</option>
            <option value="sql">SQL</option>
          </select>

          <label class="ml-2 text-[11px] font-bold uppercase text-slate-500">Font:</label>
          <select
            [(ngModel)]="fontSize"
            (ngModelChange)="onFontSizeChange($event)"
            class="px-2 py-1 bg-white border border-slate-300 rounded-lg text-xs font-semibold text-slate-800 focus:outline-none focus:ring-1 focus:ring-[#008FBB]">
            <option [ngValue]="12">12px</option>
            <option [ngValue]="13">13px</option>
            <option [ngValue]="14">14px</option>
            <option [ngValue]="16">16px</option>
            <option [ngValue]="18">18px</option>
          </select>
        </div>

        <div class="flex items-center gap-2">
          <button
            type="button"
            (click)="onReset()"
            title="Reset code to default template"
            class="px-2.5 py-1 rounded-lg bg-rose-50 border border-rose-200 text-[#D7182A] hover:bg-rose-100 text-xs font-bold transition">
            Reset Code
          </button>
        </div>
      </div>

      <!-- Editor Container -->
      <div #editorContainer class="w-full flex-1 min-h-[360px] bg-white relative">
        @if (isLoading) {
          <div class="absolute inset-0 flex items-center justify-center bg-slate-50/50 text-xs text-slate-400">
            <span class="animate-spin mr-2">&#9696;</span> Loading Monaco Editor...
          </div>
        }
      </div>
    </div>
  `,
  styles: [
    `
      :host {
        display: block;
        width: 100%;
        height: 100%;
      }
    `,
  ],
})
export class MonacoEditorComponent implements AfterViewInit, OnChanges, OnDestroy {
  @ViewChild('editorContainer', { static: true }) editorContainer!: ElementRef<HTMLDivElement>;

  @Input() code: string = '';
  @Input() language: string = 'python';
  @Input() theme: string = 'csm-light';
  @Input() fontSize: number = 13;
  @Input() readOnly: boolean = false;

  @Output() codeChange = new EventEmitter<string>();
  @Output() languageChange = new EventEmitter<string>();
  @Output() reset = new EventEmitter<void>();

  currentTheme: string = 'csm-light';
  isLoading: boolean = true;
  private editorInstance?: any;
  private resizeObserver?: ResizeObserver;
  private isUpdatingValue: boolean = false;

  ngAfterViewInit(): void {
    this.currentTheme = this.theme;
    this.initMonaco();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (!this.editorInstance) return;

    if (changes['code'] && !this.isUpdatingValue) {
      const cur = this.editorInstance.getValue();
      if (cur !== this.code) {
        this.editorInstance.setValue(this.code || '');
      }
    }

    if (changes['language'] && this.language) {
      const model = this.editorInstance.getModel();
      if (model && window.monaco) {
        window.monaco.editor.setModelLanguage(model, this.normalizeMonacoLanguage(this.language));
      }
    }

    if (changes['fontSize'] && this.fontSize) {
      this.editorInstance.updateOptions({ fontSize: this.fontSize });
    }

    if (changes['readOnly']) {
      this.editorInstance.updateOptions({ readOnly: this.readOnly });
    }
  }

  ngOnDestroy(): void {
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }
    if (this.editorInstance) {
      this.editorInstance.dispose();
    }
  }

  private initMonaco(): void {
    loadMonacoEditor()
      .then((monaco) => {
        this.isLoading = false;

        // Define CSM Light theme
        try {
          monaco.editor.defineTheme('csm-light', {
            base: 'vs',
            inherit: true,
            rules: [
              { token: 'comment', foreground: '64748B', fontStyle: 'italic' },
              { token: 'keyword', foreground: '008FBB', fontStyle: 'bold' },
              { token: 'string', foreground: '16A34A' },
              { token: 'number', foreground: 'FAA634' },
              { token: 'type', foreground: 'D7182A', fontStyle: 'bold' },
            ],
            colors: {
              'editor.background': '#FFFFFF',
              'editor.foreground': '#0F172A',
              'editorLineNumber.foreground': '#94A3B8',
              'editorLineNumber.activeForeground': '#008FBB',
              'editor.lineHighlightBackground': '#F8FAFC',
              'editorCursor.foreground': '#008FBB',
              'editor.selectionBackground': '#BAE6FD50',
            },
          });
        } catch {
          // Theme already defined
        }

        const lang = this.normalizeMonacoLanguage(this.language);
        this.editorInstance = monaco.editor.create(this.editorContainer.nativeElement, {
          value: this.code || '',
          language: lang,
          theme: this.currentTheme,
          fontSize: this.fontSize,
          readOnly: this.readOnly,
          automaticLayout: true,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          tabSize: 4,
          lineNumbers: 'on',
          fontFamily: "'Fira Code', 'Courier New', monospace",
        });

        this.editorInstance.onDidChangeModelContent(() => {
          if (!this.editorInstance) return;
          this.isUpdatingValue = true;
          const val = this.editorInstance.getValue();
          this.code = val;
          this.codeChange.emit(val);
          this.isUpdatingValue = false;
        });

        if (window.ResizeObserver) {
          this.resizeObserver = new ResizeObserver(() => {
            this.editorInstance?.layout();
          });
          this.resizeObserver.observe(this.editorContainer.nativeElement);
        }
      })
      .catch((err) => {
        this.isLoading = false;
        console.error('Failed to initialize Monaco Editor:', err);
      });
  }

  private normalizeMonacoLanguage(lang: string): string {
    const l = (lang || '').toLowerCase().trim();
    if (l === 'js' || l === 'javascript' || l === 'web dev') return 'javascript';
    if (l === 'py' || l === 'python') return 'python';
    if (l === 'java') return 'java';
    if (l === 'c' || l === 'cpp' || l === 'c++') return 'cpp';
    if (l === 'sql') return 'sql';
    return 'plaintext';
  }

  onLanguageChange(newLang: string): void {
    this.language = newLang;
    this.languageChange.emit(newLang);
    if (this.editorInstance && window.monaco) {
      const model = this.editorInstance.getModel();
      if (model) {
        window.monaco.editor.setModelLanguage(model, this.normalizeMonacoLanguage(newLang));
      }
    }
  }

  onFontSizeChange(newSize: number): void {
    this.fontSize = newSize;
    this.editorInstance?.updateOptions({ fontSize: newSize });
  }

  onReset(): void {
    this.reset.emit();
  }
}
