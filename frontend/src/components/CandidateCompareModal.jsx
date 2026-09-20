import React from 'react';
import { X, GitCompare, Check, Minus } from 'lucide-react';

export default function CandidateCompareModal({
  candidates = [],
  activeJD,
  onClose
}) {
  if (!candidates || candidates.length === 0) return null;

  const reqSkills = activeJD?.required_skills || [];

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" style={{ maxWidth: '1000px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="panel-title">
            <GitCompare size={18} color="var(--accent-cyan)" />
            <span>Side-by-Side Candidate Comparison Matrix</span>
          </div>
          <button className="btn btn-secondary btn-sm" onClick={onClose}>
            <X size={16} />
          </button>
        </div>

        <div className="modal-body" style={{ overflowX: 'auto' }}>
          <table className="rankings-table" style={{ minWidth: '600px' }}>
            <thead>
              <tr>
                <th style={{ width: '180px' }}>Evaluation Metric</th>
                {candidates.map((c) => (
                  <th key={c.candidate_id} style={{ textAlign: 'center' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-main)' }}>
                      {c.candidate_name}
                    </div>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                      Rank #{c.rank}
                    </span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {/* Overall Match */}
              <tr>
                <td style={{ fontWeight: 600 }}>Overall Match Score</td>
                {candidates.map((c) => (
                  <td key={c.candidate_id} style={{ textAlign: 'center' }}>
                    <span className={`score-badge ${c.overall_score >= 75 ? 'score-high' : (c.overall_score >= 55 ? 'score-med' : 'score-low')}`}>
                      {c.overall_score}%
                    </span>
                  </td>
                ))}
              </tr>

              {/* Skill Match Coverage */}
              <tr>
                <td style={{ fontWeight: 600 }}>Skill Coverage Score</td>
                {candidates.map((c) => (
                  <td key={c.candidate_id} style={{ textAlign: 'center', fontWeight: 600, color: 'var(--matched-green)' }}>
                    {c.skill_score}% ({c.matched_skills?.length}/{reqSkills.length})
                  </td>
                ))}
              </tr>

              {/* Text Similarity */}
              <tr>
                <td style={{ fontWeight: 600 }}>TF-IDF Text Similarity</td>
                {candidates.map((c) => (
                  <td key={c.candidate_id} style={{ textAlign: 'center', color: 'var(--accent-cyan)', fontWeight: 600 }}>
                    {c.text_similarity_score}%
                  </td>
                ))}
              </tr>

              {/* Experience Tenure */}
              <tr>
                <td style={{ fontWeight: 600 }}>Experience Tenure</td>
                {candidates.map((c) => (
                  <td key={c.candidate_id} style={{ textAlign: 'center', fontWeight: 600 }}>
                    {c.experience_years} Years
                  </td>
                ))}
              </tr>

              {/* Required Skills Checklist Matrix */}
              {reqSkills.length > 0 && (
                <>
                  <tr style={{ background: 'var(--bg-surface-elevated)' }}>
                    <td colSpan={candidates.length + 1} style={{ fontWeight: 700, fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                      Required Skill Overlap Matrix
                    </td>
                  </tr>
                  {reqSkills.map((skill) => (
                    <tr key={skill}>
                      <td style={{ fontSize: '0.8rem', color: 'var(--text-main)' }}>{skill}</td>
                      {candidates.map((c) => {
                        const hasSkill = c.matched_skills?.includes(skill);
                        return (
                          <td key={c.candidate_id} style={{ textAlign: 'center' }}>
                            {hasSkill ? (
                              <span style={{ color: 'var(--matched-green)', display: 'inline-flex', alignItems: 'center', gap: '4px', fontWeight: 600, fontSize: '0.78rem' }}>
                                <Check size={16} /> Yes
                              </span>
                            ) : (
                              <span style={{ color: 'var(--missing-rose)', display: 'inline-flex', alignItems: 'center', gap: '4px', fontSize: '0.78rem' }}>
                                <Minus size={16} /> Missing
                              </span>
                            )}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </>
              )}
            </tbody>
          </table>
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
