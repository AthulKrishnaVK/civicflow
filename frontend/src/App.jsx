

import { useState } from "react";
import axios from "axios";

import {
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  CircleAlert,
  FileCheck2,
  FileText,
  Globe2,
  Loader2,
  MapPin,
  Network,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  ExternalLink,
  Building2,
  Scale,
  ListChecks,
  ClipboardCheck,
} from "lucide-react";

import "./App.css";

/* =========================================================
   CONFIGURATION
========================================================= */

const API_URL = "http://127.0.0.1:8000";

/* =========================================================
   HELPERS
========================================================= */

function cleanEvidenceText(text = "") {
  if (!text) return "";

  return String(text)
    .replace(/^#+\s*/gm, "")
    .replace(/\*\*/g, "")
    .replace(/Source Organization:\s*/gi, "")
    .replace(/Document Title:\s*/gi, "")
    .replace(/Official URL:\s*\S+/gi, "")
    .replace(/Source Type:\s*/gi, "")
    .replace(/\s+/g, " ")
    .trim();
}

function getProcessName(process) {
  if (typeof process === "string") {
    return process;
  }

  if (process?.title) {
    return process.title;
  }

  if (process?.name) {
    return process.name;
  }

  return "Government Process";
}

function getEvidenceTitle(evidence) {
  return (
    evidence?.document_title ||
    evidence?.title ||
    "Government Source"
  );
}

function getEvidenceOrganization(evidence) {
  return (
    evidence?.organization ||
    "Government Authority"
  );
}

function getEvidenceUrl(evidence) {
  return evidence?.official_url || "";
}

/* =========================================================
   VERIFICATION CARD
========================================================= */

function VerificationCard({ item }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div
      className={`verification-card ${
        expanded ? "expanded" : ""
      }`}
    >
      <button
        type="button"
        className="verification-card-header"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="verification-card-title">
          <div className="verification-check">
            <CheckCircle2 size={20} />
          </div>

          <div>
            <h3>
              {item?.claim || "Verified claim"}
            </h3>

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

      {expanded && (
        <div className="verification-card-body">
          <div className="verification-label">
            Supporting evidence
          </div>

          <div className="verification-evidence">
            {cleanEvidenceText(item?.evidence)}
          </div>
        </div>
      )}
    </div>
  );
}

/* =========================================================
   EVIDENCE CARD
========================================================= */

function EvidenceCard({ evidence }) {
  const [expanded, setExpanded] = useState(false);

  const title = getEvidenceTitle(evidence);

  const organization =
    getEvidenceOrganization(evidence);

  const sourceType =
    evidence?.source_type ||
    "Official Government Source";

  const url = getEvidenceUrl(evidence);

  /*
   * Important:
   * Different backend agents may return the evidence
   * under different fields.
   *
   * We therefore check:
   * excerpt → evidence → text
   */
  const excerpt = cleanEvidenceText(
    evidence?.excerpt ||
      evidence?.evidence ||
      evidence?.text ||
      ""
  );

  return (
    <div
      className={`evidence-card ${
        expanded ? "expanded" : ""
      }`}
    >
      {/* Evidence header */}
      <button
        type="button"
        className="evidence-header"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="evidence-header-left">
          <div className="verification-icon">
            <CheckCircle2 size={20} />
          </div>

          <div className="evidence-title-area">
            <h3>{title}</h3>

            <div className="evidence-subtitle">
              <Building2 size={14} />

              <span>
                {organization}
              </span>
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
              className={
                expanded ? "rotate" : ""
              }
            />
          </div>
        </div>
      </button>

      {/* Expanded evidence */}
      {expanded && (
        <div className="evidence-body">

          {/* Metadata */}
          <div className="evidence-meta">
            <div className="meta-item">
              <FileCheck2 size={15} />

              <span>
                {sourceType}
              </span>
            </div>

            <div className="meta-item">
              <ShieldCheck size={15} />

              <span>
                Retrieved and verified
              </span>
            </div>
          </div>

          <div className="evidence-divider" />

          {/* Actual retrieved evidence */}
          <div className="evidence-content">

            <div className="content-label">
              RETRIEVED EVIDENCE
            </div>

            <div className="evidence-excerpt">
              {excerpt ? (
                excerpt
              ) : (
                <span className="evidence-empty">
                  No evidence excerpt is available
                  for this source.
                </span>
              )}
            </div>
          </div>

          {/* Official source */}
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
                onClick={(event) =>
                  event.stopPropagation()
                }
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

/* =========================================================
   PROCESS CARD
========================================================= */

function ProcessCard({
  process,
  index,
}) {
  return (
    <div className="process-card">
      <div className="process-number">
        {String(index + 1).padStart(2, "0")}
      </div>

      <div className="process-content">
        <div className="process-icon">
          <CheckCircle2 size={18} />
        </div>

        <div>
          <h3>
            {getProcessName(process)}
          </h3>

          <p>
            Identified as an applicable government
            process from the retrieved evidence.
          </p>
        </div>
      </div>
    </div>
  );
}

/* =========================================================
   PROCEDURE STEP
========================================================= */

function ProcedureStep({
  step,
  index,
}) {
  const [expanded, setExpanded] =
    useState(false);

  const documents =
    step?.required_documents || [];

  const evidence =
    step?.evidence || [];

  return (
    <div className="procedure-step">

      <div className="procedure-line">

        <div className="procedure-step-number">
          {index + 1}
        </div>

        <div className="procedure-connector" />
      </div>

      <div className="procedure-content">

        <button
          type="button"
          className="procedure-header"
          onClick={() =>
            setExpanded(!expanded)
          }
        >
          <div>

            <span className="procedure-label">
              STEP {index + 1}
            </span>

            <h3>
              {step?.title ||
                "Procedure step"}
            </h3>

            <p>
              {step?.description ||
                "No description available."}
            </p>

          </div>

          <ChevronDown
            size={20}
            className={
              expanded
                ? "procedure-chevron rotate"
                : "procedure-chevron"
            }
          />
        </button>

        {expanded && (
          <div className="procedure-details">

            {/* Required documents */}
            {documents.length > 0 && (
              <div className="procedure-detail-block">

                <div className="procedure-detail-title">
                  <FileText size={15} />

                  Required documents
                </div>

                <ul>
                  {documents.map(
                    (
                      document,
                      documentIndex
                    ) => (
                      <li
                        key={documentIndex}
                      >
                        {document}
                      </li>
                    )
                  )}
                </ul>
              </div>
            )}

            {/* Supporting evidence */}
            {evidence.length > 0 && (
              <div className="procedure-detail-block">

                <div className="procedure-detail-title">
                  <ShieldCheck size={15} />

                  Supporting evidence
                </div>

                {evidence.map(
                  (
                    item,
                    evidenceIndex
                  ) => (
                    <div
                      className="procedure-mini-evidence"
                      key={evidenceIndex}
                    >
                      {cleanEvidenceText(
                        item?.excerpt ||
                          item?.evidence ||
                          item?.text ||
                          ""
                      )}
                    </div>
                  )
                )}
              </div>
            )}

          </div>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   STAT CARD
========================================================= */

function StatCard({
  icon,
  number,
  label,
}) {
  return (
    <div className="result-stat">

      <div className="result-stat-icon">
        {icon}
      </div>

      <div>
        <div className="result-stat-number">
          {number}
        </div>

        <div className="result-stat-label">
          {label}
        </div>
      </div>

    </div>
  );
}

/* =========================================================
   MAIN APP
========================================================= */

export default function App() {

  /* =======================================================
     STATE
  ======================================================= */

  const [goal, setGoal] =
    useState("");

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [loadingStage, setLoadingStage] =
    useState(0);

  /* =======================================================
     LOADING STAGES
  ======================================================= */

  const loadingStages = [
    "Understanding your request",
    "Finding official government sources",
    "Checking applicable requirements",
    "Building the procedure",
    "Verifying the evidence",
  ];

  /* =======================================================
     ANALYZE
  ======================================================= */

  async function analyzeGoal() {

    if (!goal.trim()) {
      setError(
        "Please describe what you want to accomplish."
      );

      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setLoadingStage(0);

    const stageTimer =
      setInterval(() => {

        setLoadingStage(
          (current) => {

            if (
              current <
              loadingStages.length - 1
            ) {
              return current + 1;
            }

            return current;
          }
        );

      }, 3500);

    try {

      const response =
        await axios.post(
          `${API_URL}/analyze`,
          {
            goal: goal.trim(),
          }
        );

      setResult(response.data);

    } catch (err) {

      console.error(
        "CivicFlow API error:",
        err
      );

      if (
        err?.response?.data?.detail
      ) {

        setError(
          err.response.data.detail
        );

      } else {

        setError(
          "Unable to connect to CivicFlow. Make sure the FastAPI backend is running."
        );
      }

    } finally {

      clearInterval(stageTimer);
      setLoading(false);
    }
  }

  /* =======================================================
     RESET
  ======================================================= */

  function resetAnalysis() {

    setResult(null);
    setError("");
    setGoal("");
    setLoadingStage(0);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  /* =======================================================
     ENTER KEY
  ======================================================= */

  function handleKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      analyzeGoal();
    }
  }

  /* =======================================================
     DERIVED DATA
  ======================================================= */

  const intent =
    result?.intent || {};

  const eligibility =
    result?.eligibility || {};

  const documents =
    result?.documents || {};

  const regulations =
    result?.regulations || {};

  const procedure =
    result?.procedure || {};

  const verification =
    result?.verification || {};

  const sources =
    result?.sources || [];

  const research =
    result?.research || [];

  const processes =
    eligibility?.processes || [];

  const verifiedClaims =
    verification?.verified || [];

  const unsupportedClaims =
    verification?.unsupported || [];

  /* =======================================================
     RENDER
  ======================================================= */

  return (
    <div className="app">

      {/* =================================================
          HEADER
      ================================================= */}

      <header className="app-header">

        <div className="header-inner">

          <div className="brand">

            <div className="brand-mark">
              <Network size={21} />
            </div>

            <div>

              <div className="brand-name">
                CivicFlow
              </div>

              <div className="brand-tagline">
                Government Process Navigator
              </div>

            </div>

          </div>

          {result && (
            <button
              type="button"
              className="new-analysis-button"
              onClick={resetAnalysis}
            >
              <RefreshCw size={15} />

              New analysis
            </button>
          )}

        </div>

      </header>

      {/* =================================================
          HERO
      ================================================= */}

      {!result && !loading && (
        <main className="hero">

          <div className="hero-content">

            <div className="hero-badge">
              <Sparkles size={15} />

              AI-powered government research
            </div>

            <h1>
              Navigate government
              <span>
                {" "}
                processes with confidence.
              </span>
            </h1>

            <p className="hero-description">
              Tell CivicFlow what you want to
              accomplish. It researches official
              sources, identifies applicable
              requirements, builds the procedure,
              and verifies the evidence.
            </p>

            <div className="goal-box">

              <div className="goal-input-wrapper">

                <Search
                  size={21}
                  className="goal-search-icon"
                />

                <textarea
                  value={goal}
                  onChange={(event) =>
                    setGoal(event.target.value)
                  }
                  onKeyDown={handleKeyDown}
                  placeholder="What do you want to accomplish?"
                  rows={4}
                />

              </div>

              <div className="goal-box-footer">

                <span>
                  Example: "I want to start a
                  small food business in Kerala."
                </span>

                <button
                  type="button"
                  className="analyze-button"
                  onClick={analyzeGoal}
                  disabled={!goal.trim()}
                >
                  Analyze

                  <ArrowRight size={17} />
                </button>

              </div>

            </div>

            <div className="hero-features">

              <div>
                <ShieldCheck size={17} />
                Official sources
              </div>

              <div>
                <Network size={17} />
                Process mapping
              </div>

              <div>
                <ClipboardCheck size={17} />
                Evidence verification
              </div>

            </div>

          </div>

        </main>
      )}

      {/* =================================================
          LOADING
      ================================================= */}

      {loading && (
        <main className="loading-page">

          <div className="loading-container">

            <div className="loading-icon">
              <Loader2
                size={30}
                className="spin"
              />
            </div>

            <h2>
              Analyzing your request
            </h2>

            <p>
              CivicFlow is researching official
              government information.
            </p>

            <div className="loading-progress">

              {loadingStages.map(
                (stage, index) => (

                  <div
                    className={`loading-stage ${
                      index <= loadingStage
                        ? "active"
                        : ""
                    } ${
                      index === loadingStage
                        ? "current"
                        : ""
                    }`}
                    key={stage}
                  >

                    <div className="loading-stage-icon">

                      {index <
                      loadingStage ? (
                        <CheckCircle2 size={15} />
                      ) : index ===
                        loadingStage ? (
                        <Loader2
                          size={15}
                          className="spin"
                        />
                      ) : (
                        <span />
                      )}

                    </div>

                    <span>
                      {stage}
                    </span>

                  </div>
                )
              )}

            </div>

          </div>

        </main>
      )}

      {/* =================================================
          ERROR
      ================================================= */}

      {error && !loading && (

        <div className="error-container">

          <div className="error-card">

            <CircleAlert size={22} />

            <div>

              <h3>
                Analysis could not be completed
              </h3>

              <p>
                {error}
              </p>

            </div>

          </div>

          <button
            type="button"
            className="retry-button"
            onClick={analyzeGoal}
          >
            Try again
          </button>

        </div>
      )}

      {/* =================================================
          RESULTS
      ================================================= */}

      {result && !loading && (

        <main className="results-page">

          {/* =============================================
              RESULT HEADER
          ============================================= */}

          <section className="result-header">

            <div className="result-header-content">

              <div className="result-eyebrow">
                ANALYSIS COMPLETE
              </div>

              <h1>
                Your government process guide
              </h1>

              <p>
                Based on your request and the
                government evidence retrieved
                by CivicFlow.
              </p>

            </div>

            <div className="result-status">

              <CheckCircle2 size={18} />

              Evidence checked

            </div>

          </section>

          {/* =============================================
              REQUEST SUMMARY
          ============================================= */}

          <section className="result-section">

            <div className="section-heading">

              <div className="section-number">
                01
              </div>

              <div>

                <h2>
                  Request summary
                </h2>

                <p>
                  What CivicFlow understood
                  from your request.
                </p>

              </div>

            </div>

            <div className="intent-card">

              <div className="intent-main">

                <div className="intent-icon">
                  <Sparkles size={21} />
                </div>

                <div>

                  <div className="intent-label">
                    YOUR GOAL
                  </div>

                  <h3>
                    {intent.goal ||
                      result.input ||
                      goal}
                  </h3>

                </div>

              </div>

              <div className="intent-details">

                <div className="intent-detail">

                  <MapPin size={16} />

                  <div>
                    <span>
                      Location
                    </span>

                    <strong>
                      {intent.location ||
                        "Not specified"}
                    </strong>
                  </div>

                </div>

                <div className="intent-detail">

                  <Scale size={16} />

                  <div>
                    <span>
                      Domain
                    </span>

                    <strong>
                      {intent.domain ||
                        "Government process"}
                    </strong>
                  </div>

                </div>

                <div className="intent-detail">

                  <ListChecks size={16} />

                  <div>
                    <span>
                      Process type
                    </span>

                    <strong>
                      {intent.process_type ||
                        "Not specified"}
                    </strong>
                  </div>

                </div>

              </div>

            </div>

          </section>

          {/* =============================================
              QUICK STATS
          ============================================= */}

          <section className="result-stats">

            <StatCard
              icon={<CheckCircle2 size={19} />}
              number={processes.length}
              label="applicable processes"
            />

            <StatCard
              icon={<FileText size={19} />}
              number={
                documents?.documents?.length ||
                0
              }
              label="document requirements"
            />

            <StatCard
              icon={<ShieldCheck size={19} />}
              number={verifiedClaims.length}
              label="verified claims"
            />

            <StatCard
              icon={<Globe2 size={19} />}
              number={sources.length}
              label="official sources"
            />

          </section>

          {/* =============================================
              APPLICABLE PROCESSES
          ============================================= */}

          <section className="result-section">

            <div className="section-heading">

              <div className="section-number">
                02
              </div>

              <div>

                <h2>
                  Applicable processes
                </h2>

                <p>
                  Processes identified from
                  the available evidence.
                </p>

              </div>

            </div>

            {processes.length > 0 ? (

              <div className="process-grid">

                {processes.map(
                  (process, index) => (

                    <ProcessCard
                      key={index}
                      process={process}
                      index={index}
                    />

                  )
                )}

              </div>

            ) : (

              <div className="empty-result">
                No specific processes were
                identified from the retrieved
                evidence.
              </div>

            )}

          </section>

          {/* =============================================
              ELIGIBILITY
          ============================================= */}

          <section className="result-section">

            <div className="section-heading">

              <div className="section-number">
                03
              </div>

              <div>

                <h2>
                  Eligibility
                </h2>

                <p>
                  Conditions and information
                  relevant to your request.
                </p>

              </div>

            </div>

            <div className="eligibility-layout">

              <div className="eligibility-status-card">

                <div className="eligibility-icon">
                  <CheckCircle2 size={23} />
                </div>

                <div>

                  <span>
                    STATUS
                  </span>

                  <h3>
                    {eligibility.applicable
                      ? "Applicable"
                      : "Not determined"}
                  </h3>

                </div>

              </div>

              {eligibility.conditions?.length >
                0 && (

                <div className="conditions-card">

                  <h3>
                    Conditions
                  </h3>

                  <ul>

                    {eligibility.conditions.map(
                      (condition, index) => (

                        <li key={index}>

                          <CheckCircle2
                            size={15}
                          />

                          {condition}

                        </li>

                      )
                    )}

                  </ul>

                </div>
              )}

              {eligibility.missing_information
                ?.length > 0 && (

                <div className="missing-card">

                  <div className="missing-title">

                    <CircleAlert size={17} />

                    Information still needed

                  </div>

                  <ul>

                    {eligibility.missing_information.map(
                      (item, index) => (

                        <li key={index}>
                          {item}
                        </li>

                      )
                    )}

                  </ul>

                </div>
              )}

            </div>

          </section>

          {/* =============================================
              PROCEDURE
          ============================================= */}

          <section className="result-section">

            <div className="section-heading">

              <div className="section-number">
                04
              </div>

              <div>

                <h2>
                  Procedure
                </h2>

                <p>
                  A step-by-step process
                  constructed from the
                  retrieved evidence.
                </p>

              </div>

            </div>

            {procedure?.steps?.length > 0 ? (

              <div className="procedure-timeline">

                {procedure.steps.map(
                  (step, index) => (

                    <ProcedureStep
                      key={index}
                      step={step}
                      index={index}
                    />

                  )
                )}

              </div>

            ) : (

              <div className="empty-result">
                No procedure steps were
                generated.
              </div>

            )}

          </section>

          {/* =============================================
              DOCUMENTS
          ============================================= */}

          <section className="result-section">

            <div className="section-heading">

              <div className="section-number">
                05
              </div>

              <div>

                <h2>
                  Documents
                </h2>

                <p>
                  Document-related requirements
                  identified during the analysis.
                </p>

              </div>

            </div>

            {documents?.documents?.length > 0 ? (

              <div className="documents-grid">

                {documents.documents.map(
                  (document, index) => (

                    <div
                      className="document-card"
                      key={index}
                    >

                      <div className="document-icon">
                        <FileText size={20} />
                      </div>

                      <div>

                        <h3>
                          {document}
                        </h3>

                        <span>
                          Identified from
                          retrieved evidence
                        </span>

                      </div>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="empty-result">
                No specific document
                requirements were identified
                from the current evidence.
              </div>

            )}

          </section>

          {/* =============================================
              REGULATIONS
          ============================================= */}

          <section className="result-section">

            <div className="section-heading">

              <div className="section-number">
                06
              </div>

              <div>

                <h2>
                  Regulations
                </h2>

                <p>
                  Regulatory requirements
                  identified from the available
                  evidence.
                </p>

              </div>

            </div>

            {regulations?.regulations?.length >
            0 ? (

              <div className="regulations-list">

                {regulations.regulations.map(
                  (regulation, index) => (

                    <div
                      className="regulation-card"
                      key={index}
                    >

                      <div className="regulation-icon">
                        <Scale size={19} />
                      </div>

                      <div>

                        <h3>
                          {regulation.title}
                        </h3>

                        <p>
                          {regulation.description}
                        </p>

                      </div>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="empty-result">
                No specific regulations were
                identified from the current
                evidence.
              </div>

            )}

          </section>

          {/* =============================================
              VERIFICATION
          ============================================= */}

          <section className="result-section verification-section">

            <div className="section-heading">

              <div className="section-number">
                07
              </div>

              <div>

                <h2>
                  Verification
                </h2>

                <p>
                  Claims checked against the
                  research evidence.
                </p>

              </div>

            </div>

            {/* Verification statistics */}

            <div className="verification-stats">

              <div className="verification-stat verified-stat">

                <div className="stat-number">
                  {verifiedClaims.length}
                </div>

                <div className="stat-label">
                  verified claims
                </div>

              </div>

              <div className="verification-stat unsupported-stat">

                <div className="stat-number">
                  {unsupportedClaims.length}
                </div>

                <div className="stat-label">
                  unsupported claims
                </div>

              </div>

            </div>

            {/* Verification list */}

            <div className="verification-list">

              {verifiedClaims.map(
                (item, index) => (

                  <VerificationCard
                    key={`verified-${index}`}
                    item={item}
                  />

                )
              )}

              {/* Unsupported claims */}

              {unsupportedClaims.length > 0 && (

                <div className="unsupported-container">

                  <div className="unsupported-heading">

                    <CircleAlert size={16} />

                    Unsupported claims

                  </div>

                  {unsupportedClaims.map(
                    (item, index) => (

                      <div
                        className="unsupported-card"
                        key={`unsupported-${index}`}
                      >

                        <div className="unsupported-card-title">
                          {item.claim}
                        </div>

                        <div className="unsupported-card-text">
                          {cleanEvidenceText(
                            item.evidence
                          )}
                        </div>

                      </div>

                    )
                  )}

                </div>
              )}

            </div>

          </section>

          {/* =============================================
              OFFICIAL SOURCES
          ============================================= */}

          <section className="result-section">

            <div className="section-heading">

              <div className="section-number">
                08
              </div>

              <div>

                <h2>
                  Official sources
                </h2>

                <p>
                  Government sources discovered
                  for this analysis.
                </p>

              </div>

            </div>

            {sources.length > 0 ? (

              <div className="sources-list">

                {sources.map(
                  (source, index) => (

                    <div
                      className="source-card"
                      key={index}
                    >

                      <div className="source-card-icon">
                        <Globe2 size={19} />
                      </div>

                      <div className="source-card-content">

                        <h3>
                          {source.title ||
                            "Government source"}
                        </h3>

                        <p>
                          {source.organization ||
                            "Government authority"}
                        </p>

                        {source.reason && (
                          <span>
                            {source.reason}
                          </span>
                        )}

                      </div>

                      {source.url && (

                        <a
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="source-open-button"
                        >
                          Open

                          <ExternalLink
                            size={14}
                          />
                        </a>

                      )}

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="empty-result">
                No source information is
                available.
              </div>

            )}

          </section>

          {/* =============================================
              RESEARCH EVIDENCE
          ============================================= */}

          {research.length > 0 && (

            <section className="result-section">

              <div className="section-heading">

                <div className="section-number">
                  09
                </div>

                <div>

                  <h2>
                    Research evidence
                  </h2>

                  <p>
                    Retrieved evidence used
                    during the analysis.
                  </p>

                </div>

              </div>

              <div className="evidence-list">

                {research.map(
                  (evidence, index) => (

                    <EvidenceCard
                      evidence={evidence}
                      key={index}
                    />

                  )
                )}

              </div>

            </section>
          )}

          {/* =============================================
              ELIGIBILITY EVIDENCE
          ============================================= */}

          {eligibility?.evidence?.length >
            0 && (

            <section className="result-section">

              <div className="section-heading">

                <div className="section-number">
                  10
                </div>

                <div>

                  <h2>
                    Eligibility evidence
                  </h2>

                  <p>
                    Evidence supporting the
                    identified eligibility
                    conditions.
                  </p>

                </div>

              </div>

              <div className="evidence-list">

                {eligibility.evidence.map(
                  (evidence, index) => (

                    <EvidenceCard
                      evidence={evidence}
                      key={index}
                    />

                  )
                )}

              </div>

            </section>
          )}

          {/* =============================================
              UNCERTAINTIES
          ============================================= */}

          {(
            eligibility?.uncertainties
              ?.length > 0 ||
            procedure?.uncertainties
              ?.length > 0 ||
            regulations?.uncertainties
              ?.length > 0 ||
            verification?.uncertainties
              ?.length > 0
          ) && (

            <section className="result-section">

              <div className="section-heading">

                <div className="section-number">
                  11
                </div>

                <div>

                  <h2>
                    Uncertainties
                  </h2>

                  <p>
                    Areas where additional
                    information or verification
                    may be required.
                  </p>

                </div>

              </div>

              <div className="uncertainty-card">

                <div className="uncertainty-header">

                  <CircleAlert size={20} />

                  <div>

                    <h3>
                      Review before proceeding
                    </h3>

                    <p>
                      These items were flagged
                      during the analysis.
                    </p>

                  </div>

                </div>

                <ul>

                  {[
                    ...(eligibility?.uncertainties ||
                      []),

                    ...(procedure?.uncertainties ||
                      []),

                    ...(regulations?.uncertainties ||
                      []),

                    ...(verification?.uncertainties ||
                      []),
                  ].map(
                    (item, index) => (

                      <li key={index}>
                        {item}
                      </li>

                    )
                  )}

                </ul>

              </div>

            </section>
          )}

          {/* =============================================
              FOOTER
          ============================================= */}

          <div className="results-footer">

            <div className="footer-verification">

              <ShieldCheck size={18} />

              <div>

                <strong>
                  Evidence-first analysis
                </strong>

                <span>
                  CivicFlow separates retrieved
                  evidence from generated
                  explanations.
                </span>

              </div>

            </div>

            <button
              type="button"
              className="new-analysis-footer"
              onClick={resetAnalysis}
            >
              Start another analysis

              <ArrowRight size={16} />
            </button>

          </div>

        </main>
      )}

    </div>
  );
}