import React, { ReactNode } from 'react';
import './EmptyState.css';

export interface EmptyStateProps {
  title: string;
  message: string;
  icon?: ReactNode;
}

export function EmptyState({ title, message, icon }: EmptyStateProps) {
  return (
    <div className="empty-state relative overflow-hidden">
      {/* Telemetry Scanline Background */}
      <div className="empty-state-scanlines absolute inset-0 pointer-events-none" />
      
      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center">
        {icon && (
          <div className="empty-state-icon flex items-center justify-center mb-4">
            {icon}
          </div>
        )}
        <h3 className="empty-state-title text-xl font-bold uppercase tracking-widest mb-2">
          {title}
        </h3>
        <p className="empty-state-message text-sm text-center font-medium max-w-sm">
          {message}
        </p>
      </div>
    </div>
  );
}