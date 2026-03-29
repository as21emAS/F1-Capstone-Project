import React from "react";
import "./Button.css";

/** Visual style of the button */
export type ButtonVariant = "primary" | "secondary" | "danger" | "ghost";

/** Size of the button */
export type ButtonSize = "sm" | "md" | "lg";

export interface ButtonProps {
  /** Visual variant that controls colour and styling */
  variant?: ButtonVariant;
  /** Controls padding and font-size */
  size?: ButtonSize;
  /** Click handler */
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  /** Button label or inner content */
  children: React.ReactNode;
  /** Disables interaction and dims the button */
  disabled?: boolean;
  /** Renders a spinner and blocks clicks while true */
  loading?: boolean;
  /** Sets the HTML button type (defaults to "button") */
  type?: "button" | "submit" | "reset";
  /** Accessible label override when children is not descriptive text */
  ariaLabel?: string;
  /** Additional CSS class names */
  className?: string;
  /** Makes the button stretch to fill its container */
  fullWidth?: boolean;
  /** Optional icon rendered before children */
  iconLeft?: React.ReactNode;
  /** Optional icon rendered after children */
  iconRight?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = "primary",
  size = "md",
  onClick,
  children,
  disabled = false,
  loading = false,
  type = "button",
  ariaLabel,
  className = "",
  fullWidth = false,
  iconLeft,
  iconRight,
}) => {
  const isDisabled = disabled || loading;

  const classes = [
    "f1-btn",
    `f1-btn--${variant}`,
    `f1-btn--${size}`,
    fullWidth ? "f1-btn--full" : "",
    isDisabled ? "f1-btn--disabled" : "",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button
      type={type}
      className={classes}
      onClick={isDisabled ? undefined : onClick}
      disabled={isDisabled}
      aria-label={ariaLabel}
      aria-busy={loading}
      aria-disabled={isDisabled}
    >
      {loading && (
        <span className="f1-btn__spinner" aria-hidden="true">
          <svg
            width="14"
            height="14"
            viewBox="0 0 14 14"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              cx="7"
              cy="7"
              r="5.5"
              stroke="currentColor"
              strokeWidth="2"
              strokeDasharray="20 14"
              strokeLinecap="square"
            />
          </svg>
        </span>
      )}

      {!loading && iconLeft && (
        <span className="f1-btn__icon f1-btn__icon--left" aria-hidden="true">
          {iconLeft}
        </span>
      )}

      <span className="f1-btn__label">{children}</span>

      {!loading && iconRight && (
        <span className="f1-btn__icon f1-btn__icon--right" aria-hidden="true">
          {iconRight}
        </span>
      )}
    </button>
  );
};

export default Button;