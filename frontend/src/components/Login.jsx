import { useState } from "react";
import {
  ShieldCheck,
  ArrowRight,
  Search,
  FileCheck2,
  Network,
  CheckCircle2,
  Building2,
} from "lucide-react";

import { signInWithGoogle } from "../lib/auth";
import "./Login.css";

export default function Login() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGoogleLogin = async () => {
    try {
      setLoading(true);
      setError("");

      await signInWithGoogle();
    } catch (err) {
      console.error("Google login error:", err);

      if (err?.code === "auth/popup-closed-by-user") {
        setError("The Google sign-in window was closed.");
      } else if (err?.code === "auth/popup-blocked") {
        setError(
          "Your browser blocked the sign-in popup. Please allow popups and try again."
        );
      } else {
        setError("Google sign-in failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">

      {/* Background decoration */}
      <div className="login-orb login-orb-one" />
      <div className="login-orb login-orb-two" />

      <div className="login-container">

        {/* =========================================
            LEFT SIDE
        ========================================= */}

        <div className="login-info">

          <div className="login-brand">
            <div className="login-brand-icon">
              <ShieldCheck size={25} />
            </div>

            <div>
              <div className="login-brand-name">
                CivicFlow
              </div>

              <div className="login-brand-tagline">
                Government Process Navigator
              </div>
            </div>
          </div>

          <div className="login-info-content">

            {/* <div className="login-small-badge">
              <span className="badge-dot" />
              AI-powered civic intelligence
            </div> */}

            <h1>
              Navigate government
              <span> processes with confidence.</span>
            </h1>

            <p className="login-info-description">
              CivicFlow helps you understand government procedures,
              identify requirements, discover official sources and
              verify the evidence behind each answer.
            </p>

            <div className="login-features">

              <div className="login-feature">
                <div className="feature-icon">
                  <Search size={18} />
                </div>

                <div>
                  <strong>Official source discovery</strong>
                  <span>
                    Find relevant government information
                    from trusted sources.
                  </span>
                </div>
              </div>

              <div className="login-feature">
                <div className="feature-icon">
                  <FileCheck2 size={18} />
                </div>

                <div>
                  <strong>Evidence-backed answers</strong>
                  <span>
                    Ground AI-generated guidance in
                    retrieved government evidence.
                  </span>
                </div>
              </div>

              <div className="login-feature">
                <div className="feature-icon">
                  <Network size={18} />
                </div>

                <div>
                  <strong>Process navigation</strong>
                  <span>
                    Turn complex requirements into
                    understandable procedures.
                  </span>
                </div>
              </div>

            </div>

          </div>

          {/* <div className="login-info-footer">
            <ShieldCheck size={15} />
            Evidence-first government research
          </div> */}

        </div>

        {/* =========================================
            RIGHT SIDE
        ========================================= */}

        <div className="login-panel">

          <div className="login-card">

            <div className="login-card-icon">
              <Building2 size={25} />
            </div>

            <div className="login-card-heading">
              <h2>Welcome to CivicFlow</h2>

              <p>
                Sign in to start navigating government
                processes with AI assistance.
              </p>
            </div>

            {/* Google button */}

            <button
              type="button"
              className="google-button"
              onClick={handleGoogleLogin}
              disabled={loading}
            >

              {loading ? (
                <div className="google-loading">
                  <div className="login-spinner" />
                  <span>Signing you in...</span>
                </div>
              ) : (
                <>
                  <div className="google-icon">

                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      aria-hidden="true"
                    >
                      <path
                        fill="#4285F4"
                        d="M21.35 12.27c0-.71-.06-1.39-.18-2.04H12v3.86h5.24a4.48 4.48 0 0 1-1.95 2.94v2.45h3.15c1.84-1.69 2.91-4.18 2.91-7.21z"
                      />

                      <path
                        fill="#34A853"
                        d="M12 21.5c2.63 0 4.84-.87 6.45-2.35l-3.15-2.45c-.87.58-1.98.93-3.3.93-2.54 0-4.69-1.72-5.46-4.03H3.29v2.53A9.74 9.74 0 0 0 12 21.5z"
                      />

                      <path
                        fill="#FBBC05"
                        d="M6.54 13.6a5.86 5.86 0 0 1 0-3.73V7.34H3.29a9.74 9.74 0 0 0 0 8.79l3.25-2.53z"
                      />

                      <path
                        fill="#EA4335"
                        d="M12 5.84c1.43 0 2.72.49 3.74 1.46l2.8-2.8C16.84 2.92 14.63 2 12 2a9.74 9.74 0 0 0-8.71 5.34l3.25 2.53C7.31 7.56 9.46 5.84 12 5.84z"
                      />
                    </svg>

                  </div>

                  <span>Continue with Google</span>

                  <ArrowRight
                    size={18}
                    className="google-arrow"
                  />
                </>
              )}

            </button>

            {error && (
              <div className="login-error">
                <span>!</span>
                {error}
              </div>
            )}

            <div className="login-divider">
              <span>SECURE ACCESS</span>
            </div>

            {/* Security information */}

            <div className="login-security">

              <div className="security-row">
                <div className="security-check">
                  <CheckCircle2 size={15} />
                </div>

                <span>
                  Secure Google authentication
                </span>
              </div>

              <div className="security-row">
                <div className="security-check">
                  <CheckCircle2 size={15} />
                </div>

                <span>
                  Your account stays protected
                </span>
              </div>

              <div className="security-row">
                <div className="security-check">
                  <CheckCircle2 size={15} />
                </div>

                <span>
                  No government credentials required
                </span>
              </div>

            </div>

            <p className="login-terms">
              By continuing, you agree to use CivicFlow
              responsibly for accessing and understanding
              government information.
            </p>

          </div>

        </div>

      </div>

      <div className="login-bottom">
        © 2026 CivicFlow · AI-powered Government Process Navigator
      </div>

    </div>
  );
}