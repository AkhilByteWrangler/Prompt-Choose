import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Starfield from './components/Starfield';
import Header from './components/Header';
import PromptInput from './components/PromptInput';
import ResponseCards from './components/ResponseCards';
import Statistics from './components/Statistics';
import api from './services/api';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentPromptId, setCurrentPromptId] = useState(null);
  const [responses, setResponses] = useState({ a: '', b: '' });
  const [selectedResponse, setSelectedResponse] = useState(null);
  const [stats, setStats] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  
  // Response A parameters
  const [temperatureA, setTemperatureA] = useState(0.7);
  const [maxTokensA, setMaxTokensA] = useState(500);
  const [topPA, setTopPA] = useState(1.0);
  const [frequencyPenaltyA, setFrequencyPenaltyA] = useState(0.0);
  const [presencePenaltyA, setPresencePenaltyA] = useState(0.0);
  
  // Response B parameters
  const [temperatureB, setTemperatureB] = useState(0.9);
  const [maxTokensB, setMaxTokensB] = useState(500);
  const [topPB, setTopPB] = useState(1.0);
  const [frequencyPenaltyB, setFrequencyPenaltyB] = useState(0.0);
  const [presencePenaltyB, setPresencePenaltyB] = useState(0.0);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await api.getStats();
      setStats(data);
    } catch (error) {
      // Silent fail for stats loading
    }
  };

  const handleGenerateResponses = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setSelectedResponse(null);
    setShowSuccess(false);

    try {
      const data = await api.generateResponses(prompt, {
        temperatureA,
        maxTokensA,
        topPA,
        frequencyPenaltyA,
        presencePenaltyA,
        temperatureB,
        maxTokensB,
        topPB,
        frequencyPenaltyB,
        presencePenaltyB
      });
      setCurrentPromptId(data.id);
      setResponses({
        a: data.response_a,
        b: data.response_b
      });
    } catch (error) {
      // Log error without exposing details
      console.error('Error generating responses');
      alert('Error generating responses. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectResponse = async (choice) => {
    if (!currentPromptId || selectedResponse) return;

    setSelectedResponse(choice);

    try {
      await api.recordPreference(currentPromptId, choice);
      await loadStats();
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      // Silent fail for preference recording
    }
  };

  const handleExportData = async () => {
    try {
      const data = await api.exportTrainingData();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `training-data-${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting data');
      alert('Error exporting data. Please try again.');
    }
  };

  const handleNewPrompt = () => {
    setPrompt('');
    setResponses({ a: '', b: '' });
    setCurrentPromptId(null);
    setSelectedResponse(null);
    setShowSuccess(false);
  };

  return (
    <div className="app">
      <Starfield />
      
      <div className="app-container">
        <Header onExport={handleExportData} />

        <motion.main 
          className="main-content"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          {stats && <Statistics stats={stats} />}

          <PromptInput
            prompt={prompt}
            setPrompt={setPrompt}
            onGenerate={handleGenerateResponses}
            loading={loading}
            disabled={loading || (currentPromptId && !selectedResponse)}
            temperatureA={temperatureA}
            setTemperatureA={setTemperatureA}
            maxTokensA={maxTokensA}
            setMaxTokensA={setMaxTokensA}
            topPA={topPA}
            setTopPA={setTopPA}
            frequencyPenaltyA={frequencyPenaltyA}
            setFrequencyPenaltyA={setFrequencyPenaltyA}
            presencePenaltyA={presencePenaltyA}
            setPresencePenaltyA={setPresencePenaltyA}
            temperatureB={temperatureB}
            setTemperatureB={setTemperatureB}
            maxTokensB={maxTokensB}
            setMaxTokensB={setMaxTokensB}
            topPB={topPB}
            setTopPB={setTopPB}
            frequencyPenaltyB={frequencyPenaltyB}
            setFrequencyPenaltyB={setFrequencyPenaltyB}
            presencePenaltyB={presencePenaltyB}
            setPresencePenaltyB={setPresencePenaltyB}
          />

          <AnimatePresence mode="wait">
            {(responses.a || responses.b) && (
              <ResponseCards
                responses={responses}
                selectedResponse={selectedResponse}
                onSelect={handleSelectResponse}
                loading={loading}
              />
            )}
          </AnimatePresence>

          <AnimatePresence>
            {showSuccess && (
              <motion.div
                className="success-message glass"
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 50 }}
              >
                <div className="success-icon">✓</div>
                <p>Preference recorded successfully</p>
              </motion.div>
            )}
          </AnimatePresence>

          {selectedResponse && (
            <motion.div
              className="new-prompt-container"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <button 
                className="liquid-glass new-prompt-button"
                onClick={handleNewPrompt}
              >
                <span>Try Another Prompt</span>
              </button>
            </motion.div>
          )}
        </motion.main>

        <footer className="footer">
          <p>Built with precision and care</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
