import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import EthicalDisclaimer from './components/EthicalDisclaimer';
import MetricsOverview from './components/MetricsOverview';
import JobDescriptionSection from './components/JobDescriptionSection';
import ResumeUploadSection from './components/ResumeUploadSection';
import RankingsLeaderboard from './components/RankingsLeaderboard';
import CandidateDetailModal from './components/CandidateDetailModal';
import CandidateCompareModal from './components/CandidateCompareModal';
import WeightsModal from './components/WeightsModal';

import {
  fetchTemplates,
  fetchLatestJD,
  fetchCandidates,
  fetchCandidateDetail,
  fetchRankings,
  submitJobDescription,
  uploadResumes,
  analyzeCandidates,
  loadSampleData,
  clearAllData
} from './api';

export default function App() {
  const [templates, setTemplates] = useState([]);
  const [activeJD, setActiveJD] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);

  // Scoring Weights
  const [weights, setWeights] = useState({
    skill_weight: 0.60,
    text_weight: 0.30,
    experience_weight: 0.10
  });

  // Modals state
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [selectedRanking, setSelectedRanking] = useState(null);
  const [selectedForCompare, setSelectedForCompare] = useState([]);
  const [isCompareModalOpen, setIsCompareModalOpen] = useState(false);
  const [isWeightsModalOpen, setIsWeightsModalOpen] = useState(false);
  const [theme, setTheme] = useState(() => localStorage.getItem('talentpulse-theme') || 'light');

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('talentpulse-theme', theme);
  }, [theme]);

  // Auto-dismiss toast
  useEffect(() => {
    if (toast) {
      const timer = setTimeout(() => setToast(null), 4500);
      return () => clearTimeout(timer);
    }
  }, [toast]);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
  };

  // Initial Data Fetch
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [tplData, jdData, candData, rankData] = await Promise.all([
        fetchTemplates().catch(() => []),
        fetchLatestJD().catch(() => ({ active: false, job_description: null })),
        fetchCandidates().catch(() => ({ count: 0, candidates: [] })),
        fetchRankings().catch(() => ({ rankings: [] }))
      ]);

      setTemplates(tplData || []);
      if (jdData?.active) {
        setActiveJD(jdData.job_description);
      }
      setCandidates(candData?.candidates || []);
      setRankings(rankData?.rankings || []);
    } catch (err) {
      console.error('Initial load error:', err);
    } finally {
      setLoading(false);
    }
  };

  // 1. Submit Job Description
  const handleSubmitJD = async (payload) => {
    try {
      setLoading(true);
      const res = await submitJobDescription(payload);
      setActiveJD(res.job_description);
      showToast(`Job Description '${res.job_description.title}' activated!`);

      // If candidates exist, prompt or auto-run analysis
      if (candidates.length > 0) {
        await handleRunAnalysis(res.job_description.id);
      }
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  // 2. Upload Resumes
  const handleUploadFiles = async (files) => {
    try {
      setLoading(true);
      const res = await uploadResumes(files);
      showToast(`Successfully uploaded & parsed ${res.uploaded_count} resume(s)!`);
      
      // Refresh candidates
      const candRes = await fetchCandidates();
      setCandidates(candRes.candidates || []);

      // If JD is active, analyze immediately
      if (activeJD) {
        await handleRunAnalysis(activeJD.id);
      }
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  // 3. Run Matching Analysis
  const handleRunAnalysis = async (jdId = null, customWeights = null) => {
    try {
      setLoading(true);
      const targetJdId = jdId || activeJD?.id;
      const targetWeights = customWeights || weights;

      const res = await analyzeCandidates({
        jd_id: targetJdId,
        weights: targetWeights
      });

      setRankings(res.rankings || []);
      showToast(`Ranked ${res.candidate_count} candidates against '${res.job_title}'!`);
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  // 4. One-Click Sample Loader
  const handleLoadSamples = async () => {
    try {
      setLoading(true);
      const res = await loadSampleData();
      setActiveJD(res.job_description);
      setRankings(res.rankings || []);

      const candRes = await fetchCandidates();
      setCandidates(candRes.candidates || []);

      showToast('Sample suite loaded! 5 realistic candidates analyzed and ranked.');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  // 5. Reset All Data
  const handleReset = async () => {
    if (!window.confirm('Are you sure you want to clear all candidate and job description data?')) {
      return;
    }
    try {
      setLoading(true);
      await clearAllData();
      setActiveJD(null);
      setCandidates([]);
      setRankings([]);
      setSelectedForCompare([]);
      setIsCompareModalOpen(false);
      showToast('All screening data cleared.');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  // 6. View Candidate Details
  const handleSelectCandidate = async (candidateId) => {
    try {
      setLoading(true);
      const cand = await fetchCandidateDetail(candidateId);
      const matchingRank = rankings.find((r) => r.candidate_id === candidateId);
      setSelectedCandidate(cand);
      setSelectedRanking(matchingRank);
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  // 7. Toggle Candidate for Compare
  const handleToggleCompare = (candidate) => {
    const candidateId = candidate.candidate_id ?? candidate.id;
    const rankingItem = rankings.find((item) => item.candidate_id === candidateId) || candidate;
    const compareItem = rankingItem.candidate_id
      ? rankingItem
      : { ...rankingItem, candidate_id: rankingItem.id, candidate_name: rankingItem.name };
    const exists = selectedForCompare.some((c) => c.candidate_id === candidateId);
    if (exists) {
      setSelectedForCompare(selectedForCompare.filter((c) => c.candidate_id !== candidateId));
    } else {
      if (selectedForCompare.length >= 3) {
        showToast('You can compare a maximum of 3 candidates at once.', 'error');
        return;
      }
      if (!rankings.some((item) => item.candidate_id === candidateId)) {
        showToast('Run screening before comparing this resume.', 'error');
        return;
      }
      setSelectedForCompare([...selectedForCompare, compareItem]);
    }
  };

  // 8. Save Weights
  const handleSaveWeights = (newWeights) => {
    setWeights(newWeights);
    if (activeJD && candidates.length > 0) {
      handleRunAnalysis(activeJD.id, newWeights);
    }
  };

  return (
    <div className="app-container">
      {/* Toast Notification */}
      {toast && (
        <div style={{
          position: 'fixed',
          top: '20px',
          right: '24px',
          zIndex: 9999,
          background: toast.type === 'error' ? 'var(--missing-rose-bg)' : 'var(--bg-surface-elevated)',
          color: toast.type === 'error' ? 'var(--missing-rose)' : 'var(--matched-green)',
          border: `1px solid ${toast.type === 'error' ? 'var(--missing-rose-border)' : 'var(--matched-green-border)'}`,
          borderRadius: 'var(--radius-md)',
          padding: '12px 20px',
          boxShadow: '0 10px 25px rgba(0,0,0,0.5)',
          fontSize: '0.85rem',
          fontWeight: 600
        }}>
          {toast.message}
        </div>
      )}

      {/* Top Navbar */}
      <Navbar
        activeJD={activeJD}
        onLoadSamples={handleLoadSamples}
        onOpenWeights={() => setIsWeightsModalOpen(true)}
        onReset={handleReset}
        theme={theme}
        onToggleTheme={() => setTheme(theme === 'light' ? 'dark' : 'light')}
        loading={loading}
      />

      {/* Ethical AI Disclaimer Banner */}
      <EthicalDisclaimer />

      {/* Main Content Area */}
      <main className="main-content">
        {/* KPI Metrics */}
        <MetricsOverview
          totalCandidates={candidates.length}
          rankings={rankings}
        />

        {/* Workspace Grid */}
        <div className="workspace-grid">
          {/* Left Column: Job Description & Upload */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <JobDescriptionSection
              templates={templates}
              currentJD={activeJD}
              onSubmitJD={handleSubmitJD}
              loading={loading}
            />

            <ResumeUploadSection
              candidates={candidates}
              onUploadFiles={handleUploadFiles}
              onLoadSamples={handleLoadSamples}
              rankings={rankings}
              selectedForCompare={selectedForCompare}
              onToggleCompare={handleToggleCompare}
              onOpenCompareModal={() => setIsCompareModalOpen(true)}
              loading={loading}
            />
          </div>

          {/* Right Column: Ranked Candidate Leaderboard */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <RankingsLeaderboard
              rankings={rankings}
              onSelectCandidate={handleSelectCandidate}
              onRunAnalysis={() => handleRunAnalysis()}
              selectedForCompare={selectedForCompare}
              onToggleCompare={handleToggleCompare}
              onOpenCompareModal={() => setIsCompareModalOpen(true)}
              loading={loading}
              hasJD={!!activeJD}
              hasCandidates={candidates.length > 0}
            />
          </div>
        </div>
      </main>

      {/* Candidate Deep-Dive Modal */}
      {selectedCandidate && (
        <CandidateDetailModal
          candidate={selectedCandidate}
          ranking={selectedRanking}
          onClose={() => {
            setSelectedCandidate(null);
            setSelectedRanking(null);
          }}
        />
      )}

      {/* Candidate Comparison Matrix Modal */}
      {isCompareModalOpen && (
        <CandidateCompareModal
          candidates={selectedForCompare}
          activeJD={activeJD}
          onClose={() => setIsCompareModalOpen(false)}
        />
      )}

      {/* Scoring Weights Tuner Modal */}
      {isWeightsModalOpen && (
        <WeightsModal
          currentWeights={weights}
          onSaveWeights={handleSaveWeights}
          onClose={() => setIsWeightsModalOpen(false)}
        />
      )}
    </div>
  );
}
