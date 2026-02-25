import React from 'react';
import { motion } from 'framer-motion';
import './ResponseCards.css';

const ResponseCards = ({ responses, selectedResponse, onSelect, loading }) => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.1
      }
    }
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 50, scale: 0.9 },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: {
        type: 'spring',
        stiffness: 100,
        damping: 15
      }
    }
  };

  const getCardClass = (choice) => {
    let className = 'response-card glass-hover';
    if (selectedResponse === choice) {
      className += ' selected';
    } else if (selectedResponse && selectedResponse !== choice) {
      className += ' not-selected';
    }
    return className;
  };

  return (
    <motion.div
      className="responses-container"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div className="responses-header" variants={cardVariants}>
        <h3 className="responses-title">Compare Responses</h3>
        <p className="responses-subtitle">
          {selectedResponse 
            ? 'Preference recorded. Try another prompt!' 
            : 'Choose which response you prefer, or mark as tie'}
        </p>
      </motion.div>

      <div className="responses-grid">
        <motion.div
          className={getCardClass('A')}
          variants={cardVariants}
          onClick={() => !selectedResponse && !loading && onSelect('A')}
          whileHover={!selectedResponse ? { y: -8 } : {}}
          whileTap={!selectedResponse ? { scale: 0.98 } : {}}
        >
          <div className="response-header">
            <div className="response-badge" style={{ background: 'rgba(94, 92, 230, 0.15)', border: '1px solid rgba(94, 92, 230, 0.3)' }}>
              <span style={{ color: '#5e5ce6' }}>Response A</span>
            </div>
            {selectedResponse === 'A' && (
              <motion.div 
                className="selected-icon"
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ type: 'spring', stiffness: 200 }}
              >
                ✓
              </motion.div>
            )}
          </div>
          <div className="response-content">
            {responses.a || 'Generating...'}
          </div>
        </motion.div>

        <motion.div
          className={getCardClass('B')}
          variants={cardVariants}
          onClick={() => !selectedResponse && !loading && onSelect('B')}
          whileHover={!selectedResponse ? { y: -8 } : {}}
          whileTap={!selectedResponse ? { scale: 0.98 } : {}}
        >
          <div className="response-header">
            <div className="response-badge" style={{ background: 'rgba(255, 69, 58, 0.15)', border: '1px solid rgba(255, 69, 58, 0.3)' }}>
              <span style={{ color: '#ff453a' }}>Response B</span>
            </div>
            {selectedResponse === 'B' && (
              <motion.div 
                className="selected-icon"
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ type: 'spring', stiffness: 200 }}
              >
                ✓
              </motion.div>
            )}
          </div>
          <div className="response-content">
            {responses.b || 'Generating...'}
          </div>
        </motion.div>
      </div>

      {!selectedResponse && !loading && (responses.a || responses.b) && (
        <motion.div 
          className="tie-button-container"
          variants={cardVariants}
        >
          <motion.button
            className="tie-button liquid-glass"
            onClick={() => onSelect('TIE')}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path
                d="M10 4V10M10 10V16M10 10H16M10 10H4"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
            </svg>
            <span>Mark as Tie</span>
          </motion.button>
        </motion.div>
      )}
    </motion.div>
  );
};

export default ResponseCards;
