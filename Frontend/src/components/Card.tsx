import React from "react";
import "./Card.css";

/** Visual style of the card */
export type CardVariant = "default" | "dark" | "accent" | "ghost";

export interface CardProps {
  /** Visual variant that controls background and border colour */
  variant?: CardVariant;
  /** Content placed inside the card body */
  children: React.ReactNode;
  /** Additional CSS class names for the card root */
  className?: string;
  /** Removes default padding from the body when true — useful for flush content */
  noPadding?: boolean;
  /** Accessible label for screen readers when the card is interactive */
  ariaLabel?: string;
  /** Makes the entire card a clickable element */
  onClick?: () => void;
}

export interface CardHeaderProps {
  /** Title text or element displayed on the left */
  title: React.ReactNode;
  /** Optional badge or metadata displayed on the right */
  badge?: React.ReactNode;
  /** Additional CSS class names */
  className?: string;
}

export interface CardBodyProps {
  /** Inner content of the card body */
  children: React.ReactNode;
  /** Additional CSS class names */
  className?: string;
}

export interface CardFooterProps {
  /** Content displayed in the card footer */
  children: React.ReactNode;
  /** Aligns footer content — defaults to "between" */
  align?: "left" | "right" | "center" | "between";
  /** Additional CSS class names */
  className?: string;
}

/* ── Sub-components ─────────────────────────────────────────────────────────── */

export const CardHeader: React.FC<CardHeaderProps> = ({
  title,
  badge,
  className = "",
}) => (
  <div className={`f1-card__header ${className}`}>
    <span className="f1-card__title">{title}</span>
    {badge && <span className="f1-card__badge">{badge}</span>}
  </div>
);

export const CardBody: React.FC<CardBodyProps> = ({
  children,
  className = "",
}) => <div className={`f1-card__body ${className}`}>{children}</div>;

export const CardFooter: React.FC<CardFooterProps> = ({
  children,
  align = "between",
  className = "",
}) => (
  <div className={`f1-card__footer f1-card__footer--${align} ${className}`}>
    {children}
  </div>
);

/* ── Root Card ──────────────────────────────────────────────────────────────── */

export const Card: React.FC<CardProps> & {
  Header: typeof CardHeader;
  Body: typeof CardBody;
  Footer: typeof CardFooter;
} = ({
  variant = "default",
  children,
  className = "",
  noPadding = false,
  ariaLabel,
  onClick,
}) => {
  const classes = [
    "f1-card",
    `f1-card--${variant}`,
    noPadding ? "f1-card--no-padding" : "",
    onClick ? "f1-card--clickable" : "",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div
      className={classes}
      aria-label={ariaLabel}
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={
        onClick
          ? (e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onClick();
              }
            }
          : undefined
      }
    >
      {children}
    </div>
  );
};

Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;

export default Card;