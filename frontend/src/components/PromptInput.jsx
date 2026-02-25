import React, { useRef, useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './PromptInput.css';

const PromptInput = ({ 
  prompt, 
  setPrompt, 
  onGenerate, 
  loading, 
  disabled,
  // Response A parameters
  temperatureA,
  setTemperatureA,
  maxTokensA,
  setMaxTokensA,
  topPA,
  setTopPA,
  frequencyPenaltyA,
  setFrequencyPenaltyA,
  presencePenaltyA,
  setPresencePenaltyA,
  // Response B parameters
  temperatureB,
  setTemperatureB,
  maxTokensB,
  setMaxTokensB,
  topPB,
  setTopPB,
  frequencyPenaltyB,
  setFrequencyPenaltyB,
  presencePenaltyB,
  setPresencePenaltyB
}) => {
  const textareaRef = useRef(null);
  const [showAdvanced, setShowAdvanced] = useState(false);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [prompt]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      if (!disabled && prompt.trim()) {
        onGenerate();
      }
    }
  };

  return (
    <motion.div 
      className="prompt-input-container"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.4 }}
    >
      <div className="prompt-card glass">
        <div className="prompt-header">
          <h2 className="prompt-title">Enter Your Prompt</h2>
          <p className="prompt-subtitle">Generate two AI responses and choose your preference</p>
        </div>

        <div className="prompt-input-wrapper">
          <textarea
            ref={textareaRef}
            className="prompt-textarea"
            placeholder="Type your prompt here... (⌘/Ctrl + Enter to generate)"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            rows={3}
          />
        </div>

        <div className="temperature-controls">
          <div className="temperature-group">
            <label className="temperature-label">
              <span className="temperature-title">Response A Temperature</span>
              <span className="temperature-value">{temperatureA.toFixed(2)}</span>
            </label>
            <input
              type="range"
              min="0"
              max="2"
              step="0.1"
              value={temperatureA}
              onChange={(e) => setTemperatureA(parseFloat(e.target.value))}
              className="temperature-slider"
              disabled={disabled}
            />
          </div>
          <div className="temperature-group">
            <label className="temperature-label">
              <span className="temperature-title">Response B Temperature</span>
              <span className="temperature-value">{temperatureB.toFixed(2)}</span>
            </label>
            <input
              type="range"
              min="0"
              max="2"
              step="0.1"
              value={temperatureB}
              onChange={(e) => setTemperatureB(parseFloat(e.target.value))}
              className="temperature-slider"
              disabled={disabled}
            />
          </div>
        </div>

        <button 
          className="advanced-toggle"
          onClick={() => setShowAdvanced(!showAdvanced)}
          type="button"
        >
          <span>{showAdvanced ? 'Hide' : 'Show'} Advanced Settings</span>
          <svg 
            width="16" 
            height="16" 
            viewBox="0 0 16 16" 
            fill="none"
            style={{ 
              transform: showAdvanced ? 'rotate(180deg)' : 'rotate(0deg)',
              transition: 'transform 0.3s ease'
            }}
          >
            <path 
              d="M4 6L8 10L12 6" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            />
          </svg>
        </button>

        <AnimatePresence>
          {showAdvanced && (
            <motion.div 
              className="advanced-controls"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="advanced-columns">
                {/* Response A Column */}
                <div className="response-column">
                  <h3 className="column-header">Response A</h3>
                  
                  <div className="control-group">
                    <label className="control-label">
                      <span className="control-title">Max Tokens</span>
                      <span className="control-value">{maxTokensA}</span>
                    </label>
                    <input
                      type="range"
                      min="50"
                      max="2000"
                      step="50"
                      value={maxTokensA}
                      onChange={(e) => setMaxTokensA(parseInt(e.target.value))}
                      className="control-slider"
                      disabled={disabled}
                    />
                    <p className="control-hint">Maximum length of the response</p>
                  </div>

                  <div className="control-group">
                    <label className="control-label">
                      <span className="control-title">Top P</span>
                      <span className="control-value">{topPA.toFixed(2)}</span>
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.05"
                      value={topPA}
                      onChange={(e) => setTopPA(parseFloat(e.target.value))}
                      className="control-slider"
                      disabled={disabled}
                    />
                    <p className="control-hint">Nucleus sampling threshold</p>
                  </div>

                  <div className="control-group">
                    <label className="control-label">
                      <span className="control-title">Frequency Penalty</span>
                      <span className="control-value">{frequencyPenaltyA.toFixed(2)}</span>
                    </label>
                    <input
                      type="range"
                      min="-2"
                      max="2"
                      step="0.1"
                      value={frequencyPenaltyA}
                      onChange={(e) => setFrequencyPenaltyA(parseFloat(e.target.value))}
                      className="control-slider"
                      disabled={disabled}
                    />
                    <p className="control-hint">Reduce repetition of frequent tokens</p>
                  </div>

                  <div className="control-group">
                    <label className="control-label">
                      <span className="control-title">Presence Penalty</span>
                      <span className="control-value">{presencePenaltyA.toFixed(2)}</span>
                    </label>
                    <input
                      type="range"
                      min="-2"
                      max="2"
                      step="0.1"
                      value={presencePenaltyA}
                      onChange={(e) => setPresencePenaltyA(parseFloat(e.target.value))}
                      className="control-slider"
                      disabled={disabled}
                    />
                    <p className="control-hint">Encourage new topics</p>
                  </div>
                </div>

                {/* Response B Column */}
                <div className="response-column">
                  <h3 className="column-header">Response B</h3>
                  
                  <div className="control-group">
                    <label className="control-label">
                      <span className="control-title">Max Tokens</span>
                      <span className="control-value">{maxTokensB}</span>
                    </label>
                    <input
                      type="range"
                      min="50"
                      max="2000"
                      step="50"
                      value={maxTokensB}
                      onChange={(e) => setMaxTokensB(parseInt(e.target.value))}
                      className="control-slider"
                      disabled={disabled}
                    />
                    <p className="control-hint">Maximum length of the response</p>
                  </div>

                  <div className="control-group">
                    <label className="control-label">
                      <span className="control-title">Top P</span>
                      <span className="control-value">{topPB.toFixed(2)}</span>
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.05"
                      value={topPB}
                      onChange={(e) => setTopPB(parseFloat(e.target.value))}
                      className="control-slider"
                      disabled={disabled}
                    />
                    <p className="control-hint">Nucleus sampling threshold</p>
                  </div>

                  <div className="control-group">
                    <label className="control-label">
                      <span className="control-title">Frequency Penalty</span>
                      <span className="control-value">{frequencyPenaltyB.toFixed(2)}</span>
                    </label>
                    <input
                      type="range"
                      min="-2"
                      max="2"
                      step="0.1"
                      value={frequencyPenaltyB}
                      onChange={(e) => setFrequencyPenaltyB(parseFloat(e.target.value))}
                      className="control-slider"
                      disabled={disabled}
                    />
                    <p className="control-hint">Reduce repetition of frequent tokens</p>
                  </div>

                  <div className="control-group">
                    <label className="control-label">
                      <span className="control-title">Presence Penalty</span>
                      <span className="control-value">{presencePenaltyB.toFixed(2)}</span>
                    </label>
                    <input
                      type="range"
                      min="-2"
                      max="2"
                      step="0.1"
                      value={presencePenaltyB}
                      onChange={(e) => setPresencePenaltyB(parseFloat(e.target.value))}
                      className="control-slider"
                      disabled={disabled}
                    />
                    <p className="control-hint">Encourage new topics</p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="prompt-actions">
          <motion.button
            className="generate-button liquid-glass"
            onClick={onGenerate}
            disabled={disabled || !prompt.trim() || loading}
            whileHover={!disabled && !loading ? { scale: 1.02 } : {}}
            whileTap={!disabled && !loading ? { scale: 0.98 } : {}}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                <span>Generating...</span>
              </>
            ) : (
              <>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path
                    d="M10 2L12.5 7.5L18 10L12.5 12.5L10 18L7.5 12.5L2 10L7.5 7.5L10 2Z"
                    stroke="currentColor"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    fill="none"
                  />
                </svg>
                <span>Generate Responses</span>
              </>
            )}
          </motion.button>

          <p className="prompt-hint">
            Press <kbd>⌘</kbd> + <kbd>Enter</kbd> to generate
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default PromptInput;
