import React, { useState } from 'react';
import { 
  X, 
  Mail, 
  Phone, 
  GraduationCap, 
  Briefcase, 
  CheckCircle2, 
  XCircle, 
  PlusCircle, 
  FileText, 
  Calculator, 
  Download,
  Check,
  Ban
} from 'lucide-react';

export default function CandidateDetailModal({
  candidate,
  ranking,
  onClose
}) {
  const [activeTab, setActiveTab] = useState('ANALYSIS'); // ANALYSIS or RAW_TEXT
  const [recruiterStatus, setRecruiterStatus] = useState('UNDER_REVIEW'); // SHORTLISTED, REJECTED, UNDER_REVIEW

  if (!candidate) return null;

  const expl = ranking?.explanation || {};
  const breakdown = expl.breakdown || {};
  const skillBreakdown = breakdown.skill_match || {};
  const textBreakdown = breakdown.text_similarity || {};
  const expBreakdown = breakdown.experience || {};

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div>
              <h3 style={{ fontSize: '1.25rem', color: 'var(--text-main)' }}>{candidate.name}</h3>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                {candidate.filename} • {candidate.file_type?.toUpperCase()} Document
              </p>
            </div>
            {ranking && (
              <div className={`score-badge ${ranking.overall_score >= 75 ? 'score-high' : (ranking.overall_score >= 55 ? 'score-med' : 'score-low')}`}>
                Match: {ranking.overall_score}%
              </div>
            )}
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <a
              href={`/api/resumes/download/${candidate.id}`}
              className="btn btn-secondary btn-sm"
              target="_blank"
              rel="noopener noreferrer"
              title="Download original file"
            >
              <Download size={14} />
              <span>Download</span>
            </a>
            <button className="btn btn-secondary btn-sm" onClick={onClose}>
              <X size={16} />
            </button>
          </div>
        </div>

        {/* Tab Controls */}
        <div style={{ padding: '12px 24px 0', background: 'var(--bg-surface-elevated)' }}>
          <div className="tab-list">
            <button
              className={`tab-btn ${activeTab === 'ANALYSIS' ? 'active' : ''}`}
              onClick={() => setActiveTab('ANALYSIS')}
            >
              AI Matching & Skills Breakdown
            </button>
            <button
              className={`tab-btn ${activeTab === 'RAW_TEXT' ? 'active' : ''}`}
              onClick={() => setActiveTab('RAW_TEXT')}
            >
              Extracted Resume Text
            </button>
          </div>
        </div>

        {/* Body */}
        <div className="modal-body">
          {activeTab === 'ANALYSIS' ? (
            <>
              {/* Contact & Bio Info Bar */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '12px',
                background: 'var(--bg-main)',
                padding: '14px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-subtle)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.82rem' }}>
                  <Mail size={15} color="var(--primary-light)" />
                  <span style={{ color: 'var(--text-main)', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {candidate.email || 'Not Provided'}
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.82rem' }}>
                  <Phone size={15} color="var(--accent-cyan)" />
                  <span style={{ color: 'var(--text-main)' }}>
                    {candidate.phone || 'Not Provided'}
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.82rem' }}>
                  <Briefcase size={15} color="var(--warning-amber)" />
                  <span style={{ color: 'var(--text-main)' }}>
                    {candidate.experience_years} Years Experience
                  </span>
                </div>
              </div>

              {/* Education */}
              {candidate.education?.length > 0 && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <GraduationCap size={15} color="var(--primary-light)" />
                    <span>Education Background:</span>
                  </span>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {candidate.education.map((edu, idx) => (
                      <span key={idx} style={{ fontSize: '0.82rem', color: 'var(--text-main)', background: 'rgba(30, 41, 59, 0.5)', padding: '6px 10px', borderRadius: 'var(--radius-sm)' }}>
                        {edu}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Explainable AI Scoring Section */}
              {ranking && (
                <div style={{
                  background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(6, 182, 212, 0.05))',
                  border: '1px solid rgba(99, 102, 241, 0.2)',
                  borderRadius: 'var(--radius-md)',
                  padding: '16px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '12px'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Calculator size={16} color="var(--primary-light)" />
                      <span>Explainable Score Breakdown:</span>
                    </span>
                    <span className={`score-badge ${ranking.overall_score >= 75 ? 'score-high' : 'score-med'}`}>
                      {expl.tier || 'Score'} ({ranking.overall_score}%)
                    </span>
                  </div>

                  <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    {expl.summary}
                  </p>

                  {/* Mathematical breakdown bars */}
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
                    {/* Skill Match Component */}
                    <div style={{ background: 'var(--bg-main)', padding: '10px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-muted)' }}>
                        <span>Skill Match (60% wt)</span>
                        <strong style={{ color: 'var(--matched-green)' }}>+{skillBreakdown.weighted_points} pts</strong>
                      </div>
                      <div style={{ fontSize: '0.85rem', fontWeight: 700, margin: '4px 0' }}>
                        {skillBreakdown.score_percent}% coverage
                      </div>
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-subtle)' }}>
                        {skillBreakdown.matched_count} of {skillBreakdown.total_required} required skills
                      </span>
                    </div>

                    {/* TF-IDF Text Similarity Component */}
                    <div style={{ background: 'var(--bg-main)', padding: '10px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-muted)' }}>
                        <span>TF-IDF Overlap (30% wt)</span>
                        <strong style={{ color: 'var(--accent-cyan)' }}>+{textBreakdown.weighted_points} pts</strong>
                      </div>
                      <div style={{ fontSize: '0.85rem', fontWeight: 700, margin: '4px 0' }}>
                        {textBreakdown.score_percent}% similarity
                      </div>
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-subtle)' }}>
                        Cosine score: {textBreakdown.cosine_similarity}
                      </span>
                    </div>

                    {/* Experience Component */}
                    <div style={{ background: 'var(--bg-main)', padding: '10px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-muted)' }}>
                        <span>Experience (10% wt)</span>
                        <strong style={{ color: 'var(--primary-light)' }}>+{expBreakdown.weighted_points} pts</strong>
                      </div>
                      <div style={{ fontSize: '0.85rem', fontWeight: 700, margin: '4px 0' }}>
                        {expBreakdown.candidate_years} / {expBreakdown.target_years} yrs target
                      </div>
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-subtle)' }}>
                        Tenure score: {expBreakdown.score_percent}%
                      </span>
                    </div>
                  </div>

                  {/* Formula */}
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-subtle)', background: 'rgba(0, 0, 0, 0.3)', padding: '6px 10px', borderRadius: 'var(--radius-sm)', fontFamily: 'monospace' }}>
                    Formula: {expl.formula}
                  </div>
                </div>
              )}

              {/* Skills Analysis Pill Grid */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {/* Matched Skills */}
                <div>
                  <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--matched-green)', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                    <CheckCircle2 size={16} />
                    <span>Matched Skills ({ranking?.matched_skills?.length || 0}):</span>
                  </span>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {ranking?.matched_skills?.map((skill, i) => (
                      <span key={i} className="skill-pill skill-pill-matched">
                        {skill}
                      </span>
                    ))}
                    {(!ranking?.matched_skills || ranking.matched_skills.length === 0) && (
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>None</span>
                    )}
                  </div>
                </div>

                {/* Missing Skills */}
                <div>
                  <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--missing-rose)', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                    <XCircle size={16} />
                    <span>Missing Skills ({ranking?.missing_skills?.length || 0}):</span>
                  </span>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {ranking?.missing_skills?.map((skill, i) => (
                      <span key={i} className="skill-pill skill-pill-missing">
                        {skill}
                      </span>
                    ))}
                    {(!ranking?.missing_skills || ranking.missing_skills.length === 0) && (
                      <span style={{ fontSize: '0.75rem', color: 'var(--matched-green)' }}>No missing skills! Candidate matches all required skills.</span>
                    )}
                  </div>
                </div>

                {/* Additional Skills */}
                <div>
                  <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--additional-blue)', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                    <PlusCircle size={16} />
                    <span>Additional Skills ({ranking?.additional_skills?.length || 0}):</span>
                  </span>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {ranking?.additional_skills?.map((skill, i) => (
                      <span key={i} className="skill-pill skill-pill-additional">
                        {skill}
                      </span>
                    ))}
                    {(!ranking?.additional_skills || ranking.additional_skills.length === 0) && (
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>None</span>
                    )}
                  </div>
                </div>

                {/* Skills Grouped by Domain Category */}
                {candidate.skills_by_category && Object.keys(candidate.skills_by_category).length > 0 && (
                  <div style={{ marginTop: '10px' }}>
                    <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: '8px' }}>
                      All Extracted Skills by Domain:
                    </span>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '10px' }}>
                      {Object.entries(candidate.skills_by_category).map(([cat, skills]) => (
                        <div key={cat} style={{ background: 'var(--bg-main)', padding: '10px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
                          <span style={{ fontSize: '0.72rem', color: 'var(--accent-cyan)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                            {cat} ({skills.length})
                          </span>
                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                            {skills.map((s, idx) => (
                              <span key={idx} className="skill-pill skill-pill-neutral" style={{ fontSize: '0.7rem' }}>
                                {s}
                              </span>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </>
          ) : (
            /* Raw Text Viewer */
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Normalized text extracted by document parser:
              </span>
              <pre style={{
                background: 'var(--bg-main)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '16px',
                fontSize: '0.8rem',
                color: 'var(--text-main)',
                whiteSpace: 'pre-wrap',
                maxHeight: '400px',
                overflowY: 'auto',
                lineHeight: '1.4'
              }}>
                {candidate.cleaned_text || candidate.raw_text}
              </pre>
            </div>
          )}
        </div>

        {/* Footer / Recruiter Actions */}
        <div className="modal-footer">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginRight: 'auto' }}>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>
              Recruiter Decision:
            </span>
            <button
              className={`btn btn-sm ${recruiterStatus === 'SHORTLISTED' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setRecruiterStatus('SHORTLISTED')}
              style={recruiterStatus === 'SHORTLISTED' ? { background: 'var(--matched-green)', borderColor: 'var(--matched-green)' } : {}}
            >
              <Check size={13} />
              <span>Shortlist</span>
            </button>
            <button
              className={`btn btn-sm ${recruiterStatus === 'REJECTED' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setRecruiterStatus('REJECTED')}
              style={recruiterStatus === 'REJECTED' ? { background: 'var(--missing-rose)', borderColor: 'var(--missing-rose)' } : {}}
            >
              <Ban size={13} />
              <span>Reject</span>
            </button>
          </div>

          <button className="btn btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
