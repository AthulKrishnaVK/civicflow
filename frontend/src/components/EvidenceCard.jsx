import { useState } from "react";
import {
  CheckCircle2,
  ChevronDown,
  ExternalLink,
  Building2,
  FileCheck2,
  ShieldCheck
} from "lucide-react";
import "./EvidenceCard.css";
function cleanMarkdown(text = "") {
  return text
    .replace(/^#+\s*/gm, "")
    .replace(/\*\*/g, "")
    .replace(/Source Organization:/g, "")
    .replace(/Document Title:/g, "")
    .replace(/Official URL:/g, "")
    .replace(/Source Type:/g, "");
}

export default function EvidenceCard({ evidence }) {
  const [expanded, setExpanded] = useState(false);

  const title =
    evidence.document_title ||
    evidence.title ||
    "Government Source";

  const organization =
    evidence.organization ||
    "Government Authority";

  const sourceType =
    evidence.source_type ||
    "Official Government Source";

  const url =
    evidence.official_url ||
    evidence.source ||
    "";

  const excerpt = cleanMarkdown(
    evidence.excerpt ||
    evidence.evidence ||
    ""
  );

  return (
    <div className={`evidence-card ${expanded ? "expanded" : ""}`}>

      {/* Header */}
      <button
        className="evidence-header"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="evidence-header-left">

          <div className="verification-icon">
            <CheckCircle2 size={21} />
          </div>

          <div className="evidence-title-area">
            <h3>{title}</h3>

            <div className="evidence-subtitle">
              <Building2 size={14} />
              <span>{organization}</span>
            </div>
          </div>

        </div>

        <div className="evidence-header-right">

          <span className="verified-badge">
            <ShieldCheck size={14} />
            Verified
          </span>

          <div className="expand-button">
            <ChevronDown
              size={19}
              className={expanded ? "rotate" : ""}
            />
          </div>

        </div>
      </button>


      {/* Expanded content */}
      {expanded && (
        <div className="evidence-body">

          <div className="evidence-meta">

            <div className="meta-item">
              <FileCheck2 size={15} />
              <span>{sourceType}</span>
            </div>

            <div className="meta-item">
              <ShieldCheck size={15} />
              <span>Retrieved & verified</span>
            </div>

          </div>


          <div className="evidence-divider" />


          <div className="evidence-content">

            <div className="content-label">
              Retrieved evidence
            </div>

            <div className="evidence-excerpt">
              {excerpt}
            </div>

          </div>


          {url && (
            <div className="evidence-footer">

              <div className="source-info">
                <span className="source-dot" />
                Official government source
              </div>

              <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className="source-link"
                onClick={(e) => e.stopPropagation()}
              >
                View official source
                <ExternalLink size={15} />
              </a>

            </div>
          )}

        </div>
      )}

    </div>
  );
}