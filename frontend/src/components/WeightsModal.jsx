import React, { useState } from 'react';
import { X, Sliders, RotateCcw, Check } from 'lucide-react';

export default function WeightsModal({
  currentWeights,
  onSaveWeights,
  onClose
}) {
  const [skillWeight, setSkillWeight] = useState(Math.round((currentWeights?.skill_weight || 0.60) * 100));
  const [textWeight, setTextWeight] = useState(Math.round((currentWeights?.text_weight || 0.30) * 100));
  const [expWeight, setExpWeight] = useState(Math.round((currentWeights?.experience_weight || 0.10) * 100));

  const total = skillWeight + textWeight + expWeight;

  const handleReset = () => {
    setSkillWeight(60);
    setTextWeight(30);
    setExpWeight(10);
  };

  const handleSave = () => {
    onSaveWeights({
      skill_weight: skillWeight / 100,
      text_weight: textWeight / 100,
      experience_weight: expWeight / 100
    });
    onClose();
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" style={{ maxWidth: '520px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="panel-title">
            <Sliders size={18} color="var(--primary-light)" />
            <span>Tune Scoring Algorithm Weights</span>
          </div>
          <button className="btn btn-secondary btn-sm" onClick={onClose}>
            <X size={16} />
          </button>
        </div>

        <div className="modal-body" style={{ gap: '20px' }}>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            Customize the weighting of each component in the candidate scoring pipeline according to your team's hiring priorities.
          </p>

          {/* Skill Weight Slider */}
          <div className="slider-group">
            <div className="slider-header">
              <span style={{ fontWeight: 600, color: 'var(--matched-green)' }}>
                Skill Match Weight
              </span>
              <span style={{ fontWeight: 700 }}>{skillWeight}%</span>
            </div>
            <input
              type="range"
              min="10"
              max="90"
              step="5"
              className="slider-input"
              value={skillWeight}
              onChange={(e) => setSkillWeight(Number(e.target.value))}
            />
            <span style={{ fontSize: '0.72rem', color: 'var(--text-subtle)' }}>
              Evaluates direct overlap between candidate skills and JD requirements.
            </span>
          </div>

          {/* Text Similarity Slider */}
          <div className="slider-group">
            <div className="slider-header">
              <span style={{ fontWeight: 600, color: 'var(--accent-cyan)' }}>
                TF-IDF Text Similarity Weight
              </span>
              <span style={{ fontWeight: 700 }}>{textWeight}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="60"
              step="5"
              className="slider-input"
              value={textWeight}
              onChange={(e) => setTextWeight(Number(e.target.value))}
            />
            <span style={{ fontSize: '0.72rem', color: 'var(--text-subtle)' }}>
              Evaluates overall semantic and keyword phrasing similarity.
            </span>
          </div>

          {/* Experience Tenure Slider */}
          <div className="slider-group">
            <div className="slider-header">
              <span style={{ fontWeight: 600, color: 'var(--primary-light)' }}>
                Experience Qualification Weight
              </span>
              <span style={{ fontWeight: 700 }}>{expWeight}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="40"
              step="5"
              className="slider-input"
              value={expWeight}
              onChange={(e) => setExpWeight(Number(e.target.value))}
            />
            <span style={{ fontSize: '0.72rem', color: 'var(--text-subtle)' }}>
              Compares candidate tenure against role seniority requirements.
            </span>
          </div>

          {/* Summary Box */}
          <div style={{
            background: 'var(--bg-main)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            padding: '12px 14px',
            fontSize: '0.8rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <span style={{ color: 'var(--text-muted)' }}>Normalized Formula Total:</span>
            <strong style={{ color: total === 100 ? 'var(--matched-green)' : 'var(--warning-amber)' }}>
              {skillWeight}% + {textWeight}% + {expWeight}% = {total}%
            </strong>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={handleReset}>
            <RotateCcw size={14} />
            <span>Default (60/30/10)</span>
          </button>
          <button className="btn btn-primary" onClick={handleSave}>
            <Check size={14} />
            <span>Apply Weights</span>
          </button>
        </div>
      </div>
    </div>
  );
}
