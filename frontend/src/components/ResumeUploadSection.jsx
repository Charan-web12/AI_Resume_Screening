import React, { useRef, useState } from 'react';
import { UploadCloud, File, AlertCircle, Sparkles, CheckCircle, FileText } from 'lucide-react';

export default function ResumeUploadSection({
  candidates = [],
  onUploadFiles,
  onLoadSamples,
  rankings = [],
  selectedForCompare = [],
  onToggleCompare,
  onOpenCompareModal,
  loading
}) {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploadError, setUploadError] = useState('');

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      processFiles(e.dataTransfer.files);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      processFiles(e.target.files);
    }
  };

  const processFiles = (fileList) => {
    setUploadError('');
    const validFiles = [];
    const invalidFiles = [];

    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];
      const name = file.name.toLowerCase();
      if (name.endsWith('.pdf') || name.endsWith('.docx') || name.endsWith('.doc')) {
        validFiles.push(file);
      } else {
        invalidFiles.push(file.name);
      }
    }

    if (invalidFiles.length > 0) {
      setUploadError(`Ignored unsupported file(s): ${invalidFiles.join(', ')}. Only PDF and DOCX are accepted.`);
    }

    if (validFiles.length > 0) {
      onUploadFiles(validFiles);
    }
  };

  return (
    <div className="panel-card">
      <div className="panel-header">
        <div className="panel-title">
          <UploadCloud size={18} color="var(--primary-light)" />
          <span>Resume Ingestion</span>
        </div>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          {candidates.length} Candidate{candidates.length === 1 ? '' : 's'} Ingested
        </span>
      </div>

      <div className="panel-body">
        {/* Drag and Drop Zone */}
        <div
          className={`dropzone-container ${dragActive ? 'active' : ''}`}
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".pdf,.docx,.doc"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <div className="dropzone-icon">
            <UploadCloud size={24} />
          </div>
          <div>
            <p style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-main)', marginBottom: '4px' }}>
              Drag & Drop Resumes Here, or <span style={{ color: 'var(--primary-light)' }}>Browse</span>
            </p>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Supports multiple <strong>PDF</strong> and <strong>DOCX</strong> files (Max 15MB each)
            </p>
          </div>
        </div>

        {uploadError && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            background: 'var(--missing-rose-bg)',
            border: '1px solid var(--missing-rose-border)',
            padding: '10px 14px',
            borderRadius: 'var(--radius-md)',
            color: 'var(--missing-rose)',
            fontSize: '0.8rem'
          }}>
            <AlertCircle size={16} />
            <span>{uploadError}</span>
          </div>
        )}

        {/* Quick Sample Button */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            Need test data?
          </span>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={onLoadSamples}
            disabled={loading}
          >
            <Sparkles size={13} color="var(--primary-light)" />
            <span>Load 5 Sample Resumes</span>
          </button>
        </div>

        {/* Uploaded Candidates List Preview */}
        {candidates.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)' }}>
              Ingested Candidates ({candidates.length}):
            </span>
            <div style={{ maxHeight: '160px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {candidates.map((cand) => (
                <div
                  key={cand.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '8px 12px',
                    background: 'var(--bg-main)',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--border-subtle)',
                    fontSize: '0.8rem'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflow: 'hidden' }}>
                    <input
                      type="checkbox"
                      checked={selectedForCompare.some((item) => item.candidate_id === cand.id)}
                      onChange={() => onToggleCompare(cand)}
                      onClick={(event) => event.stopPropagation()}
                      disabled={!rankings.some((item) => item.candidate_id === cand.id)}
                      title="Select this screened resume for comparison"
                      style={{ cursor: 'pointer', width: '16px', height: '16px' }}
                    />
                    <FileText size={14} color="var(--accent-cyan)" />
                    <span style={{ fontWeight: 600, color: 'var(--text-main)' }}>{cand.name}</span>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-subtle)' }}>({cand.filename})</span>
                  </div>
                  <span className="skill-pill skill-pill-neutral" style={{ fontSize: '0.7rem' }}>
                    {cand.all_skills?.length || 0} skills
                  </span>
                </div>
              ))}
            </div>
            {selectedForCompare.length > 1 && (
              <button type="button" className="btn btn-secondary btn-sm" onClick={onOpenCompareModal}>
                Compare Selected ({selectedForCompare.length})
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
