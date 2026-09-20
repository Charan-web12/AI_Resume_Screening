import React, { useState } from 'react';
import { FileText, Sparkles, Check, ChevronDown, Layers } from 'lucide-react';

export default function JobDescriptionSection({
  templates = [],
  currentJD,
  onSubmitJD,
  loading
}) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [minExp, setMinExp] = useState(3.0);
  const [isCustomExpanded, setIsCustomExpanded] = useState(false);

  const handleSelectTemplate = (tpl) => {
    setTitle(tpl.title);
    setDescription(tpl.description);
    setMinExp(tpl.min_experience_years);
    onSubmitJD({
      title: tpl.title,
      description: tpl.description,
      min_experience_years: tpl.min_experience_years
    });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (!description.trim()) return;
    onSubmitJD({
      title: title.trim() || 'Custom Role',
      description: description.trim(),
      min_experience_years: parseFloat(minExp) || 0
    });
  };

  return (
    <div className="panel-card">
      <div className="panel-header">
        <div className="panel-title">
          <FileText size={18} color="var(--primary-light)" />
          <span>Target Job Description</span>
        </div>
        {currentJD && (
          <span style={{ fontSize: '0.75rem', color: 'var(--matched-green)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Check size={14} /> Active Role Loaded
          </span>
        )}
      </div>

      <div className="panel-body">
        {/* Quick Role Templates */}
        <div className="form-group">
          <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Sparkles size={13} color="var(--accent-cyan)" />
            <span>Quick Select Role Template:</span>
          </label>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {templates.map((tpl) => {
              const isSelected = currentJD && currentJD.title === tpl.title;
              return (
                <button
                  key={tpl.id}
                  type="button"
                  onClick={() => handleSelectTemplate(tpl)}
                  disabled={loading}
                  className={`btn btn-sm ${isSelected ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ borderRadius: 'var(--radius-full)', fontSize: '0.75rem' }}
                >
                  {tpl.title.split('(')[0].trim()}
                </button>
              );
            })}
          </div>
        </div>

        {/* Current Active JD Skills Overview */}
        {currentJD && (
          <div style={{
            background: 'var(--bg-main)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            padding: '14px',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-main)' }}>
                {currentJD.title}
              </span>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Min Experience: <strong style={{ color: 'var(--accent-cyan)' }}>{currentJD.min_experience_years} yrs</strong>
              </span>
            </div>

            <div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                Required Skills ({currentJD.required_skills?.length || 0}):
              </span>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                {currentJD.required_skills?.map((skill, idx) => (
                  <span key={idx} className="skill-pill skill-pill-matched">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {currentJD.optional_skills?.length > 0 && (
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                  Preferred / Bonus Skills ({currentJD.optional_skills.length}):
                </span>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {currentJD.optional_skills.map((skill, idx) => (
                    <span key={idx} className="skill-pill skill-pill-neutral">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Toggle Custom JD Input */}
        <div>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={() => setIsCustomExpanded(!isCustomExpanded)}
            style={{ width: '100%', justifyContent: 'space-between' }}
          >
            <span>{isCustomExpanded ? 'Hide Custom JD Input' : '✏️ Paste or Customize Job Description'}</span>
            <ChevronDown size={14} style={{ transform: isCustomExpanded ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }} />
          </button>
        </div>

        {isCustomExpanded && (
          <form onSubmit={handleFormSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div className="form-group">
              <label className="form-label">Job Title</label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. Senior Machine Learning Engineer"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Min. Experience (Years)</label>
              <input
                type="number"
                step="0.5"
                min="0"
                className="form-input"
                value={minExp}
                onChange={(e) => setMinExp(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Job Description Text</label>
              <textarea
                className="form-textarea"
                placeholder="Paste the full job description here (responsibilities, required skills, preferred qualifications)..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={6}
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !description.trim()}
            >
              {loading ? <div className="spinner" /> : <Layers size={14} />}
              <span>Extract Skills & Set Active Role</span>
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
