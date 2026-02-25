import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = {
  async generateResponses(prompt, options = {}) {
    const response = await axios.post(`${API_BASE_URL}/prompts/generate/`, {
      prompt,
      model_name: options.modelName || 'gpt-3.5-turbo',
      // Response A parameters
      temperature_a: options.temperatureA !== undefined ? options.temperatureA : 0.7,
      max_tokens_a: options.maxTokensA !== undefined ? options.maxTokensA : 500,
      top_p_a: options.topPA !== undefined ? options.topPA : 1.0,
      frequency_penalty_a: options.frequencyPenaltyA !== undefined ? options.frequencyPenaltyA : 0.0,
      presence_penalty_a: options.presencePenaltyA !== undefined ? options.presencePenaltyA : 0.0,
      // Response B parameters
      temperature_b: options.temperatureB !== undefined ? options.temperatureB : 0.9,
      max_tokens_b: options.maxTokensB !== undefined ? options.maxTokensB : 500,
      top_p_b: options.topPB !== undefined ? options.topPB : 1.0,
      frequency_penalty_b: options.frequencyPenaltyB !== undefined ? options.frequencyPenaltyB : 0.0,
      presence_penalty_b: options.presencePenaltyB !== undefined ? options.presencePenaltyB : 0.0
    });
    return response.data;
  },

  async recordPreference(promptId, preference) {
    const response = await axios.post(
      `${API_BASE_URL}/prompts/${promptId}/record-preference/`,
      { preference }
    );
    return response.data;
  },

  async getStats() {
    const response = await axios.get(`${API_BASE_URL}/prompts/stats/`);
    return response.data;
  },

  async exportTrainingData() {
    const response = await axios.get(`${API_BASE_URL}/prompts/export-training-data/`);
    return response.data;
  },

  async getAllPrompts() {
    const response = await axios.get(`${API_BASE_URL}/prompts/`);
    return response.data;
  }
};

export default api;
