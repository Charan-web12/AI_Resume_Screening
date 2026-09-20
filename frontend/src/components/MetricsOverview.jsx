import React from 'react';
import { Users, CheckCircle2, TrendingUp, Award } from 'lucide-react';

export default function MetricsOverview({ 
  totalCandidates = 0, 
  rankings = [] 
}) {
  const screenedCount = rankings.length;
  const highFitCount = rankings.filter(r => r.overall_score >= 75).length;
  const avgScore = screenedCount > 0 
    ? Math.round(rankings.reduce((sum, r) => sum + r.overall_score, 0) / screenedCount)
    : 0;

  return (
    <div className="metrics-row">
      <div className="metric-card">
        <div className="metric-icon-box" style={{ background: 'rgba(99, 102, 241, 0.15)', color: 'var(--primary-light)' }}>
          <Users size={24} />
        </div>
        <div className="metric-data">
          <span className="metric-label">Total Resumes</span>
          <span className="metric-value">{totalCandidates}</span>
        </div>
      </div>

      <div className="metric-card">
        <div className="metric-icon-box" style={{ background: 'rgba(6, 182, 212, 0.15)', color: 'var(--accent-cyan)' }}>
          <CheckCircle2 size={24} />
        </div>
        <div className="metric-data">
          <span className="metric-label">Screened & Ranked</span>
          <span className="metric-value">{screenedCount}</span>
        </div>
      </div>

      <div className="metric-card">
        <div className="metric-icon-box" style={{ background: 'var(--matched-green-bg)', color: 'var(--matched-green)' }}>
          <Award size={24} />
        </div>
        <div className="metric-data">
          <span className="metric-label">High Match (≥75%)</span>
          <span className="metric-value" style={{ color: 'var(--matched-green)' }}>{highFitCount}</span>
        </div>
      </div>

      <div className="metric-card">
        <div className="metric-icon-box" style={{ background: 'var(--warning-amber-bg)', color: 'var(--warning-amber)' }}>
          <TrendingUp size={24} />
        </div>
        <div className="metric-data">
          <span className="metric-label">Average Match Score</span>
          <span className="metric-value">{avgScore}%</span>
        </div>
      </div>
    </div>
  );
}
