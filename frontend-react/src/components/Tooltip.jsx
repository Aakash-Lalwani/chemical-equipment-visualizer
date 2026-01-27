import React, { useState } from 'react';
import '../styles/Tooltip.css';

/**
 * Reusable Tooltip Component
 * 
 * ELI5: Like a helpful sticky note that appears when you hover over something!
 * 
 * USAGE:
 * <Tooltip text="Explanation here">
 *   <span>Technical Term</span>
 * </Tooltip>
 * 
 * ACCESSIBILITY:
 * - Uses aria-describedby for screen readers
 * - Keyboard accessible (focus shows tooltip)
 * - High contrast for visibility
 */
const Tooltip = ({ children, text, position = 'top' }) => {
  const [isVisible, setIsVisible] = useState(false);
  const [tooltipId] = useState(`tooltip-${Math.random().toString(36).substr(2, 9)}`);

  return (
    <span 
      className="tooltip-wrapper"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      onFocus={() => setIsVisible(true)}
      onBlur={() => setIsVisible(false)}
      aria-describedby={isVisible ? tooltipId : undefined}
    >
      {children}
      {isVisible && (
        <span 
          id={tooltipId}
          className={`tooltip-content tooltip-${position}`}
          role="tooltip"
        >
          {text}
        </span>
      )}
    </span>
  );
};

export default Tooltip;
