/**
 * Keyboard Shortcuts Handler
 * 
 * ELI5: Like hotkeys in video games - press a button combo to do something fast!
 * 
 * SHORTCUTS:
 * - Escape: Close modals, clear search
 * - Enter: Submit forms, confirm actions
 * - Ctrl+S: Save/Export (prevent default browser save)
 * - F5: Refresh data (prevent browser refresh)
 * - Tab: Navigate between elements
 * 
 * ACCESSIBILITY:
 * - Keyboard-only navigation
 * - Screen reader friendly
 * - Standard conventions
 */

export const setupKeyboardShortcuts = (handlers = {}) => {
  const handleKeyDown = (event) => {
    const { key, ctrlKey, metaKey, target } = event;
    
    // Don't interfere with typing in inputs
    const isTyping = target.tagName === 'INPUT' || 
                     target.tagName === 'TEXTAREA' || 
                     target.isContentEditable;

    // Escape key - Close modals, clear search
    if (key === 'Escape') {
      if (handlers.onEscape) {
        handlers.onEscape();
      }
    }

    // Ctrl+S or Cmd+S - Save/Export
    if ((ctrlKey || metaKey) && key === 's') {
      event.preventDefault();
      if (handlers.onSave) {
        handlers.onSave();
      }
    }

    // F5 - Refresh data
    if (key === 'F5') {
      event.preventDefault();
      if (handlers.onRefresh) {
        handlers.onRefresh();
      }
    }

    // Ctrl+/ - Show keyboard shortcuts help
    if ((ctrlKey || metaKey) && key === '/') {
      event.preventDefault();
      if (handlers.onShowHelp) {
        handlers.onShowHelp();
      }
    }

    // Enter - Submit/Confirm (only when not typing)
    if (key === 'Enter' && !isTyping) {
      if (handlers.onEnter) {
        handlers.onEnter();
      }
    }
  };

  // Add event listener
  document.addEventListener('keydown', handleKeyDown);

  // Return cleanup function
  return () => {
    document.removeEventListener('keydown', handleKeyDown);
  };
};

/**
 * Hook version for React components
 */
export const useKeyboardShortcuts = (handlers) => {
  React.useEffect(() => {
    return setupKeyboardShortcuts(handlers);
  }, [handlers]);
};

/**
 * Keyboard shortcuts reference
 */
export const KEYBOARD_SHORTCUTS = {
  general: [
    { keys: ['Esc'], description: 'Close modal or cancel action' },
    { keys: ['Tab'], description: 'Navigate between elements' },
    { keys: ['Shift', 'Tab'], description: 'Navigate backwards' },
    { keys: ['Ctrl', '/'], description: 'Show keyboard shortcuts' },
  ],
  actions: [
    { keys: ['Enter'], description: 'Submit form or confirm action' },
    { keys: ['Ctrl', 'S'], description: 'Save or export data' },
    { keys: ['F5'], description: 'Refresh data' },
  ],
  navigation: [
    { keys: ['Ctrl', '1'], description: 'Go to Dashboard' },
    { keys: ['Ctrl', '2'], description: 'Go to Upload' },
    { keys: ['Ctrl', '3'], description: 'Go to History' },
  ],
};
