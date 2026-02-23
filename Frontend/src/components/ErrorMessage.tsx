import React, { useState } from "react";
import "./ErrorMessage.css";

/** Severity level of the message */
export type MessageSeverity = "error" | "warning" | "info" | "success";

export interface ErrorMessageProps {
  /** Severity controls the icon and colour scheme */
  severity?: MessageSeverity;
  /** Short bold headline for the message */
  title?: string;
  /** Body text or JSX content */
  children: React.ReactNode;
  /** When true, renders an × button that hides the message */
  dismissible?: boolean;
  /** Callback fired when the user dismisses the message */
  onDismiss?: () => void;
  /** Optional action button label */
  actionLabel?: string;
  /** Callback fired when the action button is clicked */
  onAction?: () => void;
  /** Additional CSS class names */
  className?: string;
}

const ICONS: Record<MessageSeverity, React.ReactNode> = {
  error: (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
      <rect x="1" y="1" width="16" height="16" stroke="currentColor" strokeWidth="2" />
      <line x1="5.5" y1="5.5" x2="12.5" y2="12.5" stroke="currentColor" strokeWidth="2" strokeLinecap="square" />
      <line x1="12.5" y1="5.5" x2="5.5" y2="12.5" stroke="currentColor" strokeWidth="2" strokeLinecap="square" />
    </svg>
  ),
  warning: (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
      <polygon points="9,2 17,16 1,16" stroke="currentColor" strokeWidth="2" strokeLinejoin="miter" fill="none" />
      <line x1="9" y1="7" x2="9" y2="11" stroke="currentColor" strokeWidth="2" strokeLinecap="square" />
      <rect x="8" y="13" width="2" height="2" fill="currentColor" />
    </svg>
  ),
  info: (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
      <circle cx="9" cy="9" r="8" stroke="currentColor" strokeWidth="2" />
      <rect x="8" y="5" width="2" height="2" fill="currentColor" />
      <line x1="9" y1="9" x2="9" y2="13" stroke="currentColor" strokeWidth="2" strokeLinecap="square" />
    </svg>
  ),
  success: (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
      <rect x="1" y="1" width="16" height="16" stroke="currentColor" strokeWidth="2" />
      <polyline points="4,9 8,13 14,6" stroke="currentColor" strokeWidth="2" strokeLinecap="square" strokeLinejoin="miter" fill="none" />
    </svg>
  ),
};

const SEVERITY_LABELS: Record<MessageSeverity, string> = {
  error: "Error",
  warning: "Warning",
  info: "Information",
  success: "Success",
};

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  severity = "error",
  title,
  children,
  dismissible = false,
  onDismiss,
  actionLabel,
  onAction,
  className = "",
}) => {
  const [visible, setVisible] = useState(true);

  if (!visible) return null;

  const handleDismiss = () => {
    setVisible(false);
    onDismiss?.();
  };

  return (
    <div
      className={["f1-message", `f1-message--${severity}`, className]
        .filter(Boolean)
        .join(" ")}
      role={severity === "error" ? "alert" : "status"}
      aria-live={severity === "error" ? "assertive" : "polite"}
      aria-label={`${SEVERITY_LABELS[severity]}: ${title ?? ""}`}
    >
      {/* Left severity stripe */}
      <div className="f1-message__stripe" aria-hidden="true" />

      {/* Icon */}
      <div className="f1-message__icon" aria-hidden="true">
        {ICONS[severity]}
      </div>

      {/* Content */}
      <div className="f1-message__content">
        {title && (
          <p className="f1-message__title">{title}</p>
        )}
        <div className="f1-message__body">{children}</div>

        {actionLabel && onAction && (
          <button
            className="f1-message__action"
            onClick={onAction}
            type="button"
          >
            {actionLabel} →
          </button>
        )}
      </div>

      {/* Dismiss button */}
      {dismissible && (
        <button
          className="f1-message__dismiss"
          onClick={handleDismiss}
          type="button"
          aria-label="Dismiss this message"
        >
          ×
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;