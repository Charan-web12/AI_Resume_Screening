import React, { useState } from 'react';
import { 
  Award, 
  Search, 
  Filter, 
  Eye, 
  Download, 
  ArrowUpDown, 
  Play, 
  CheckCircle, 
  XCircle, 
  GitCompare,
  ExternalLink
} from 'lucide-react';

export default function RankingsLeaderboard({
  rankings = [],
  onSelectCandidate,
  onRunAnalysis,
  selectedForCompare = [],
  onToggleCompare,
  onOpenCompareModal,
  loading,
  hasJD,
  hasCandidates
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [tierFilter, setTierFilter] = useState('ALL');
  const [sortBy, setSortBy] = useState('SCORE_DESC');

  // Filter & Search
  const filteredRankings = rankings.filter((r) => {
    // Tier filter
    if (tierFilter === 'HIGH' && r.overall_score < 75) return false;
    if (tierFilter === 'MODERATE' && (r.overall_score < 55 || r.overall_score >= 75)) return false;
    if (tierFilter === 'LOW' && r.overall_score >= 55) return false;

    // Search filter
    if (!searchTerm.trim()) return true;
    const term = searchTerm.toLowerCase();
    const nameMatch = r.candidate_name?.toLowerCase().includes(term);
    const skillMatch = r.matched_skills?.some((s) => s.toLowerCase().includes(term)) ||
                       r.all_skills?.some((s) => s.toLowerCase().includes(term));
    const missingMatch = r.missing_skills?.some((s) => s.toLowerCase().includes(term));
    return nameMatch || skillMatch || missingMatch;
  });

  // Sorting
  const sortedRankings = [...filteredRankings].sort((a, b) => {
    if (sortBy === 'SCORE_DESC') return b.overall_score - a.overall_score;
    if (sortBy === 'SCORE_ASC') return a.overall_score - b.overall_score;
    if (sortBy === 'EXP_DESC') return b.experience_years - a.experience_years;
    if (sortBy === 'NAME_ASC') return a.candidate_name.localeCompare(b.candidate_name);
    return 0;
  });

  const getRankBadgeClass = (rank) => {
    if (rank === 1) return 'rank-badge rank-gold';
    if (rank === 2) return 'rank-badge rank-silver';
    if (rank === 3) return 'rank-badge rank-bronze';
    return 'rank-badge rank-default';
  };

  const getScoreBadgeClass = (score) => {
    if (score >= 75) return 'score-badge score-high';
    if (score >= 55) return 'score-badge score-med';
    return 'score-badge score-low';
  };

  return (
    <div className="panel-card" style={{ width: '100%' }}>
      <div className="panel-header" style={{ flexWrap: 'wrap', gap: '12px' }}>
        <div className="panel-title">
          <Award size={20} color="var(--primary-light)" />
          <span>Candidate Suitability Leaderboard</span>
          {rankings.length > 0 && (
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 400 }}>
              ({rankings.length} Ranked Applicants)
            </span>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {selectedForCompare.length > 1 && (
            <button
              className="btn btn-secondary btn-sm"
              onClick={onOpenCompareModal}
              style={{ borderColor: 'var(--accent-cyan)', color: 'var(--accent-cyan)' }}
            >
              <GitCompare size={14} />
              <span>Compare Selected ({selectedForCompare.length})</span>
            </button>
          )}

          <button
            className="btn btn-primary"
            onClick={onRunAnalysis}
            disabled={loading || !hasJD || !hasCandidates}
            title={!hasJD ? 'Please set a Job Description first' : (!hasCandidates ? 'Please upload resumes first' : 'Analyze resumes against JD')}
          >
            {loading ? <div className="spinner" /> : <Play size={14} />}
            <span>{rankings.length > 0 ? 'Recalculate Rankings' : 'Run AI Screening'}</span>
          </button>
        </div>
      </div>

      <div className="panel-body" style={{ gap: '16px' }}>
        {/* Filter Controls Bar */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px',
          background: 'var(--bg-main)',
          padding: '12px 16px',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-subtle)'
        }}>
          {/* Search Box */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: '1 1 240px', maxWidth: '360px' }}>
            <Search size={16} color="var(--text-muted)" />
            <input
              type="text"
              className="form-input"
              style={{ padding: '6px 10px', fontSize: '0.82rem' }}
              placeholder="Search candidate name, skills (e.g. Python, Docker)..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Tier Filter Buttons */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>Filter:</span>
            <button
              type="button"
              className={`btn btn-sm ${tierFilter === 'ALL' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setTierFilter('ALL')}
            >
              All
            </button>
            <button
              type="button"
              className={`btn btn-sm ${tierFilter === 'HIGH' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setTierFilter('HIGH')}
              style={tierFilter === 'HIGH' ? { background: 'var(--matched-green)', color: 'white' } : {}}
            >
              High Match (≥75%)
            </button>
            <button
              type="button"
              className={`btn btn-sm ${tierFilter === 'MODERATE' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setTierFilter('MODERATE')}
            >
              Moderate (55-74%)
            </button>
            <button
              type="button"
              className={`btn btn-sm ${tierFilter === 'LOW' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setTierFilter('LOW')}
            >
              Low (&lt;55%)
            </button>
          </div>

          {/* Sort Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <ArrowUpDown size={14} color="var(--text-muted)" />
            <select
              className="form-input"
              style={{ padding: '6px 10px', fontSize: '0.82rem', width: 'auto' }}
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="SCORE_DESC">Highest Match %</option>
              <option value="SCORE_ASC">Lowest Match %</option>
              <option value="EXP_DESC">Most Experience</option>
              <option value="NAME_ASC">Candidate Name</option>
            </select>
          </div>
        </div>

        {/* Empty State */}
        {sortedRankings.length === 0 && (
          <div className="empty-state">
            <Award size={48} color="var(--text-subtle)" />
            <h4 style={{ color: 'var(--text-main)', fontSize: '1.1rem' }}>No Screened Candidates Yet</h4>
            <p style={{ maxWidth: '400px', fontSize: '0.85rem' }}>
              {rankings.length === 0
                ? "Upload resumes or click '⚡ Load Sample Suite' in the top bar to run the automated AI matching engine."
                : "No candidates match the selected search and filter criteria."}
            </p>
          </div>
        )}

        {/* Table View */}
        {sortedRankings.length > 0 && (
          <div className="table-container">
            <table className="rankings-table">
              <thead>
                <tr>
                  <th style={{ width: '40px' }}>Compare</th>
                  <th style={{ width: '60px' }}>Rank</th>
                  <th>Candidate</th>
                  <th style={{ width: '130px' }}>Match Score</th>
                  <th>Matched Skills</th>
                  <th>Missing Skills</th>
                  <th style={{ width: '90px' }}>Experience</th>
                  <th style={{ width: '140px', textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {sortedRankings.map((cand) => {
                  const isChecked = selectedForCompare.some((c) => c.candidate_id === cand.candidate_id);
                  return (
                    <tr key={cand.candidate_id}>
                      {/* Compare Checkbox */}
                      <td>
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => onToggleCompare(cand)}
                          style={{ cursor: 'pointer', width: '16px', height: '16px' }}
                          title="Select to compare candidates side-by-side"
                        />
                      </td>

                      {/* Rank Medal */}
                      <td>
                        <div className={getRankBadgeClass(cand.rank)}>
                          #{cand.rank}
                        </div>
                      </td>

                      {/* Candidate Info */}
                      <td>
                        <div style={{ display: 'flex', flexDirection: 'column' }}>
                          <span style={{ fontWeight: 700, color: 'var(--text-main)', fontSize: '0.92rem' }}>
                            {cand.candidate_name}
                          </span>
                          <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
                            {cand.email} • {cand.phone}
                          </span>
                          <span style={{ fontSize: '0.7rem', color: 'var(--text-subtle)' }}>
                            File: {cand.filename} ({cand.file_type.toUpperCase()})
                          </span>
                        </div>
                      </td>

                      {/* Match Score */}
                      <td>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                          <div className={getScoreBadgeClass(cand.overall_score)}>
                            {cand.overall_score}%
                          </div>
                          {/* Mini progress bar */}
                          <div style={{
                            width: '100%',
                            height: '5px',
                            background: 'var(--bg-main)',
                            borderRadius: '3px',
                            overflow: 'hidden'
                          }}>
                            <div
                              style={{
                                width: `${cand.overall_score}%`,
                                height: '100%',
                                background: cand.overall_score >= 75 ? 'var(--matched-green)' : (cand.overall_score >= 55 ? 'var(--warning-amber)' : 'var(--missing-rose)'),
                                borderRadius: '3px'
                              }}
                            />
                          </div>
                        </div>
                      </td>

                      {/* Matched Skills */}
                      <td>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', maxWidth: '320px' }}>
                          {cand.matched_skills?.slice(0, 5).map((skill, idx) => (
                            <span key={idx} className="skill-pill skill-pill-matched">
                              {skill}
                            </span>
                          ))}
                          {cand.matched_skills?.length > 5 && (
                            <span className="skill-pill skill-pill-neutral" title={cand.matched_skills.slice(5).join(', ')}>
                              +{cand.matched_skills.length - 5} more
                            </span>
                          )}
                          {cand.matched_skills?.length === 0 && (
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-subtle)', fontStyle: 'italic' }}>
                              None matched
                            </span>
                          )}
                        </div>
                      </td>

                      {/* Missing Skills */}
                      <td>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', maxWidth: '280px' }}>
                          {cand.missing_skills?.slice(0, 4).map((skill, idx) => (
                            <span key={idx} className="skill-pill skill-pill-missing">
                              {skill}
                            </span>
                          ))}
                          {cand.missing_skills?.length > 4 && (
                            <span className="skill-pill skill-pill-neutral" title={cand.missing_skills.slice(4).join(', ')}>
                              +{cand.missing_skills.length - 4} more
                            </span>
                          )}
                          {cand.missing_skills?.length === 0 && (
                            <span style={{ fontSize: '0.75rem', color: 'var(--matched-green)', fontWeight: 600 }}>
                              ✓ Complete Match
                            </span>
                          )}
                        </div>
                      </td>

                      {/* Experience */}
                      <td>
                        <span style={{ fontWeight: 600, color: 'var(--text-main)' }}>
                          {cand.experience_years} yrs
                        </span>
                      </td>

                      {/* Actions */}
                      <td style={{ textAlign: 'right' }}>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '6px' }}>
                          <button
                            className="btn btn-secondary btn-sm"
                            onClick={() => onSelectCandidate(cand.candidate_id)}
                            title="View deep-dive profile and mathematical explainability"
                          >
                            <Eye size={13} />
                            <span>Profile</span>
                          </button>
                          <a
                            href={`/api/resumes/download/${cand.candidate_id}`}
                            className="btn btn-secondary btn-sm"
                            target="_blank"
                            rel="noopener noreferrer"
                            title="Download original resume file"
                          >
                            <Download size={13} />
                          </a>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
