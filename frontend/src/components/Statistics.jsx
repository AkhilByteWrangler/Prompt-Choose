import React from 'react';
import { motion } from 'framer-motion';
import './Statistics.css';

const Statistics = ({ stats }) => {
  if (!stats) return null;

  const statItems = [
    { label: 'Total Prompts', value: stats.total_prompts, color: 'rgba(255, 255, 255, 0.9)' },
    { label: 'Training Pairs', value: stats.training_pairs, color: 'rgba(76, 217, 100, 0.9)' },
    { label: 'Preference A', value: stats.preference_a, color: 'rgba(94, 92, 230, 0.9)' },
    { label: 'Preference B', value: stats.preference_b, color: 'rgba(255, 69, 58, 0.9)' },
  ];

  return (
    <motion.div 
      className="statistics"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
    >
      <div className="stats-grid">
        {statItems.map((item, index) => (
          <motion.div
            key={item.label}
            className="stat-card glass"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
            whileHover={{ scale: 1.02, y: -4 }}
          >
            <div className="stat-value" style={{ color: item.color }}>
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.5 + index * 0.1 }}
              >
                {item.value}
              </motion.span>
            </div>
            <div className="stat-label">{item.label}</div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default Statistics;
