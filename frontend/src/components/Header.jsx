import React from 'react';
import { motion } from 'framer-motion';
import './Header.css';

const Header = ({ onExport }) => {
  return (
    <motion.header 
      className="header glass"
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, type: 'spring', stiffness: 100 }}
    >
      <div className="header-content">
        <motion.div 
          className="logo-container"
          whileHover={{ scale: 1.05 }}
          transition={{ duration: 0.3 }}
        >
          <div className="logo-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <path
                d="M16 2L4 8.5L4 23.5L16 30L28 23.5V8.5L16 2Z"
                stroke="white"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                opacity="0.9"
              />
              <circle cx="16" cy="16" r="4" fill="white" opacity="0.8" />
            </svg>
          </div>
          <h1 className="logo-text gradient-text">Prompt Selector</h1>
        </motion.div>

        <button 
          className="export-button liquid-glass"
          onClick={onExport}
        >
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path
              d="M16 11V14.5C16 15.3284 15.3284 16 14.5 16H3.5C2.67157 16 2 15.3284 2 14.5V11M9 2V12M9 2L5 6M9 2L13 6"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span>Export Data</span>
        </button>
      </div>
    </motion.header>
  );
};

export default Header;
