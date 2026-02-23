import React from "react";
import "./LoadingSpinner.css";

/** Visual style of the spinner */
export type SpinnerVariant = "wheel" | "bars" | "dots";

/** Size preset */
export type SpinnerSize = "sm" | "md" | "lg";

export interface LoadingSpinnerProps {
  /** Visual style of the spinner animation */
  variant?: SpinnerVariant;
  /** Preset size */
  size?: SpinnerSize;
  /** Accessible label announced to screen readers (defaults to "Loading…") */
  label?: string;
  /** Optional status message displayed below the spinner */
  message?: string;
  /** When true, renders a full-screen overlay with the spinner centred */
  overlay?: boolean;
  /** Additional CSS class names */
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  variant = "wheel",
  size = "md",
  label = "Loading…",
  message,
  overlay = false,
  className = "",
}) => {
  const spinner = (
    <div
      className={[
        "f1-spinner",
        `f1-spinner--${variant}`,
        `f1-spinner--${size}`,
        className,
      ]
        .filter(Boolean)
        .join(" ")}
      role="status"
      aria-label={label}
      aria-live="polite"
    >
      {/* ── Wheel variant ──────────────────────────────────────────────────── */}
      {variant === "wheel" && (
        <svg
          className="f1-spinner__wheel"
          viewBox="0 0 40 40"
          aria-hidden="true"
          focusable="false"
        >
          {/* Outer ring */}
          <circle
            cx="20"
            cy="20"
            r="17"
            stroke="#e0d4bc"
            strokeWidth="3"
            fill="none"
          />
          {/* Spinning arc */}
          <circle
            cx="20"
            cy="20"
            r="17"
            stroke="#c8001a"
            strokeWidth="3"
            fill="none"
            strokeDasharray="54 54"
            strokeLinecap="square"
            className="f1-spinner__arc"
          />
          {/* Centre dot */}
          <circle cx="20" cy="20" r="3" fill="#1c1208" />
        </svg>
      )}

      {/* ── Bars variant (timing-board style) ─────────────────────────────── */}
      {variant === "bars" && (
        <div className="f1-spinner__bars" aria-hidden="true">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="f1-spinner__bar" style={{ animationDelay: `${i * 0.1}s` }} />
          ))}
        </div>
      )}

      {/* ── Dots variant ──────────────────────────────────────────────────── */}
      {variant === "dots" && (
        <div className="f1-spinner__dots" aria-hidden="true">
          {[0, 1, 2].map((i) => (
            <div key={i} className="f1-spinner__dot" style={{ animationDelay: `${i * 0.2}s` }} />
          ))}
        </div>
      )}

      {/* Visible status message */}
      {message && <p className="f1-spinner__message">{message}</p>}

      {/* Visually-hidden label for screen readers */}
      <span className="f1-spinner__sr-label">{label}</span>
    </div>
  );

  if (overlay) {
    return (
      <div className="f1-spinner__overlay" aria-modal="true">
        {spinner}
      </div>
    );
  }

  return spinner;
};

export default LoadingSpinner;