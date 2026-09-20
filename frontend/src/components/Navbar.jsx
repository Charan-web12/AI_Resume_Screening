import React from 'react';
import { Sparkles, Sliders, RotateCcw, Briefcase, Moon, Sun } from 'lucide-react';

export default function Navbar({ 
  activeJD, 
  onLoadSamples, 
  onOpenWeights, 
  onReset, 
  loading,
  theme,
  onToggleTheme
}) {
  return (
    <header className="navbar">
      <div className="brand-wrapper">
        <div className="brand-logo-badge">
          <Sparkles size={22} />
        </div>
        <div className="brand-info">
          <h1>TalentPulse AI</h1>
          <span className="brand-tagline">Intelligent Screening & Candidate Matching</span>
        </div>
      </div>

      <div className="nav-actions">
        {activeJD && (
          <div style={{
            display: 'flex', 
            alignItems: 'center', 
            gap: '8px', 
            background: 'rgba(99, 102, 241, 0.1)', 
            padding: '6px 14px', 
            borderRadius: 'var(--radius-full)', 
            border: '1px solid rgba(99, 102, 241, 0.25)',
            fontSize: '0.8rem',
            color: 'var(--text-main)'
          }}>
            <Briefcase size={14} color="var(--primary-light)" />
            <span>Active Role: <strong style={{ color: 'var(--primary-light)' }}>{activeJD.title}</strong></span>
          </div>
        )}

        <button
          className="btn btn-secondary btn-sm"
          onClick={onToggleTheme}
          title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
          {theme === 'light' ? <Moon size={14} /> : <Sun size={14} />}
          <span>{theme === 'light' ? 'Dark' : 'Light'}</span>
        </button>

        <button 
          className="btn btn-secondary btn-sm"
          onClick={onOpenWeights}
          title="Adjust scoring weights"
        >
          <Sliders size={14} />
          <span>Weights</span>
        </button>

        <button 
          className="btn btn-primary btn-sm"
          onClick={onLoadSamples}
          disabled={loading}
          title="Load 5 realistic PDF/DOCX resumes and sample JD"
        >
          {loading ? <div className="spinner" /> : <Sparkles size={14} />}
          <span>⚡ Load Sample Suite</span>
        </button>

        <button 
          className="btn btn-danger-outline btn-sm"
          onClick={onReset}
          disabled={loading}
          title="Clear all uploaded data"
        >
          <RotateCcw size={14} />
          <span>Reset</span>
        </button>
      </div>
    </header>
  );
}
