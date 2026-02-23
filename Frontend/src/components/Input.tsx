import React, { useId } from "react";
import "./Input.css";

/** Input field type */
export type InputType = "text" | "number" | "email" | "password" | "search" | "tel" | "url";

/** Visual state of the input */
export type InputStatus = "default" | "error" | "success";

/* ─── Shared Option type for Select ─────────────────────────────────────────── */

export interface SelectOption {
  /** The value submitted with the form */
  value: string;
  /** Human-readable label shown in the dropdown */
  label: string;
  /** Disables this individual option */
  disabled?: boolean;
}

/* ─── Text / Number Input ────────────────────────────────────────────────────── */

export interface InputProps {
  /** HTML input type */
  type?: InputType;
  /** Visible field label — always required for accessibility */
  label: string;
  /** Hides the visible label while keeping it accessible to screen readers */
  hideLabel?: boolean;
  /** Controlled value */
  value?: string | number;
  /** Change handler */
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  /** Placeholder hint text */
  placeholder?: string;
  /** Disables the input */
  disabled?: boolean;
  /** Marks the field as required */
  required?: boolean;
  /** Validation status that controls colour */
  status?: InputStatus;
  /** Helper text shown below the input */
  helperText?: string;
  /** Error message — shown below the input when status is "error" */
  errorText?: string;
  /** Makes the input fill its container */
  fullWidth?: boolean;
  /** Additional CSS class names */
  className?: string;
  /** Optional prefix text/icon rendered inside the left edge */
  prefixSlot?: React.ReactNode;
  /** Optional suffix text/icon rendered inside the right edge */
  suffixSlot?: React.ReactNode;
  /** HTML name attribute */
  name?: string;
  /** Minimum value (for number inputs) */
  min?: number;
  /** Maximum value (for number inputs) */
  max?: number;
  /** Step value (for number inputs) */
  step?: number;
  /** Auto-complete behaviour */
  autoComplete?: string;
}

export const Input: React.FC<InputProps> = ({
  type = "text",
  label,
  hideLabel = false,
  value,
  onChange,
  placeholder,
  disabled = false,
  required = false,
  status = "default",
  helperText,
  errorText,
  fullWidth = false,
  className = "",
  prefixSlot,
  suffixSlot,
  name,
  min,
  max,
  step,
  autoComplete,
}) => {
  const uid = useId();
  const errorId = `${uid}-error`;
  const helperId = `${uid}-helper`;
  const hasError = status === "error" && errorText;

  return (
    <div
      className={[
        "f1-input-wrap",
        fullWidth ? "f1-input-wrap--full" : "",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <label
        htmlFor={uid}
        className={`f1-input__label${hideLabel ? " sr-only" : ""}`}
      >
        {label}
        {required && (
          <span className="f1-input__required" aria-hidden="true">
            {" "}*
          </span>
        )}
      </label>

      <div className={`f1-input__field-wrap f1-input__field-wrap--${status}`}>
        {prefixSlot && (
          <span className="f1-input__prefix" aria-hidden="true">
            {prefixSlot}
          </span>
        )}

        <input
          id={uid}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          min={min}
          max={max}
          step={step}
          autoComplete={autoComplete}
          className={[
            "f1-input__field",
            prefixSlot ? "f1-input__field--has-prefix" : "",
            suffixSlot ? "f1-input__field--has-suffix" : "",
          ]
            .filter(Boolean)
            .join(" ")}
          aria-describedby={
            [hasError ? errorId : "", helperText ? helperId : ""]
              .filter(Boolean)
              .join(" ") || undefined
          }
          aria-invalid={hasError ? "true" : undefined}
          aria-required={required}
        />

        {suffixSlot && (
          <span className="f1-input__suffix" aria-hidden="true">
            {suffixSlot}
          </span>
        )}
      </div>

      {hasError && (
        <p id={errorId} className="f1-input__error" role="alert">
          ⚠ {errorText}
        </p>
      )}

      {helperText && !hasError && (
        <p id={helperId} className="f1-input__helper">
          {helperText}
        </p>
      )}
    </div>
  );
};

/* ─── Select ─────────────────────────────────────────────────────────────────── */

export interface SelectProps {
  /** Visible field label — always required for accessibility */
  label: string;
  /** Hides the visible label while keeping it accessible to screen readers */
  hideLabel?: boolean;
  /** Array of options to display */
  options: SelectOption[];
  /** Controlled selected value */
  value?: string;
  /** Change handler */
  onChange?: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  /** Placeholder option shown when no value is selected */
  placeholder?: string;
  /** Disables the select */
  disabled?: boolean;
  /** Marks the field as required */
  required?: boolean;
  /** Validation status */
  status?: InputStatus;
  /** Helper text shown below the select */
  helperText?: string;
  /** Error message shown when status is "error" */
  errorText?: string;
  /** Makes the select fill its container */
  fullWidth?: boolean;
  /** Additional CSS class names */
  className?: string;
  /** HTML name attribute */
  name?: string;
}

export const Select: React.FC<SelectProps> = ({
  label,
  hideLabel = false,
  options,
  value,
  onChange,
  placeholder,
  disabled = false,
  required = false,
  status = "default",
  helperText,
  errorText,
  fullWidth = false,
  className = "",
  name,
}) => {
  const uid = useId();
  const errorId = `${uid}-error`;
  const helperId = `${uid}-helper`;
  const hasError = status === "error" && errorText;

  return (
    <div
      className={[
        "f1-input-wrap",
        fullWidth ? "f1-input-wrap--full" : "",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <label
        htmlFor={uid}
        className={`f1-input__label${hideLabel ? " sr-only" : ""}`}
      >
        {label}
        {required && (
          <span className="f1-input__required" aria-hidden="true">
            {" "}*
          </span>
        )}
      </label>

      <div className={`f1-input__field-wrap f1-input__field-wrap--${status}`}>
        <select
          id={uid}
          name={name}
          value={value}
          onChange={onChange}
          disabled={disabled}
          required={required}
          className="f1-input__field f1-input__field--select"
          aria-describedby={
            [hasError ? errorId : "", helperText ? helperId : ""]
              .filter(Boolean)
              .join(" ") || undefined
          }
          aria-invalid={hasError ? "true" : undefined}
          aria-required={required}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((opt) => (
            <option key={opt.value} value={opt.value} disabled={opt.disabled}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      {hasError && (
        <p id={errorId} className="f1-input__error" role="alert">
          ⚠ {errorText}
        </p>
      )}
      {helperText && !hasError && (
        <p id={helperId} className="f1-input__helper">
          {helperText}
        </p>
      )}
    </div>
  );
};

export default Input;