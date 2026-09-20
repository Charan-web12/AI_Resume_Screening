import React from 'react';
import { ShieldCheck, Info } from 'lucide-react';

export default function EthicalDisclaimer() {
  return (
    <div className="disclaimer-banner">
      <div className="disclaimer-content">
        <ShieldCheck size={16} color="var(--matched-green)" />
        <span>
          <strong>Ethical AI Recruiter Disclaimer:</strong> TalentPulse AI provides explainable recommendation scoring based strictly on technical skills, experience tenure, and job description semantic overlap. Protected characteristics (gender, race, religion, age, nationality) are excluded from scoring. Final hiring decisions must always be made by human recruiters.
        </span>
      </div>
      <span style={{ fontSize: '0.75rem', opacity: 0.8, whiteSpace: 'nowrap' }}>
        Compliance Standard: EEOC & AI Ethics
      </span>
    </div>
  );
}
