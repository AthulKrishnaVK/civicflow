import { useState } from "react";
import {
  CheckCircle2,
  ChevronDown,
  ShieldCheck
} from "lucide-react";

function cleanEvidenceText(text = "") {
  return text
    .replace(/^#+\s*/gm, "")
    .replace(/\*\*/g, "")
    .replace(/Source Organization:/g, "")
    .replace(/Document Title:/g, "")
    .replace(/Official URL:\s*\S+/g, "")
    .replace(/Source Type:/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

export default function VerificationCard({ item }) {

  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`verification-card ${expanded ? "expanded" : ""}`}>

      {/* Header */}
      <button
        className="verification-card-header"
        onClick={() => setExpanded(!expanded)}
      >

        <div className="verification-card-title">

          <div className="verification-check">
            <CheckCircle2 size={20} />
          </div>

          <div>
            <h3>{item.claim}</h3>

            <span>
              Verified against retrieved evidence
            </span>
          </div>

        </div>


        <div className="verification-card-actions">

          <div className="verification-status">
            <ShieldCheck size={13} />
            VERIFIED
          </div>

          <div className="verification-expand">
            <ChevronDown
              size={19}
              className={expanded ? "rotate" : ""}
            />
          </div>

        </div>

      </button>


      {/* Evidence */}
      {expanded && (

        <div className="verification-card-body">

          <div className="verification-label">
            Supporting evidence
          </div>

          <div className="verification-evidence">
            {cleanEvidenceText(item.evidence)}
          </div>

        </div>

      )}

    </div>
  );
}