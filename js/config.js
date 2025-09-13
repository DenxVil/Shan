// API Endpoints and Keys
// IMPORTANT: Do not commit real API keys to a public repository.
// Use environment variables or a secure backend to manage keys in production.
const API_KEYS = {
    GEMINI_API_KEY: 'YOUR_GEMINI_API_KEY_HERE',
    PERPLEXITY_API_KEY: 'YOUR_PERPLEXITY_API_KEY_HERE',
    HUGGINGFACE_API_KEY: 'YOUR_HUGGINGFACE_API_KEY_HERE'
};

const API_ENDPOINTS = {
    GEMINI: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
    PERPLEXITY_ONLINE: 'https://api.perplexity.ai/chat/completions', // For pplx-7b-online or pplx-8x7b-online
    HUGGINGFACE: 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium'
};

// Model routing configuration
const MODEL_ROUTING_RULES = [
    { keywords: ['latest', 'news', 'now', 'current events'], model: 'perplexity' },
    { keywords: ['code', 'debug', 'javascript', 'python'], model: 'gemini' }
];

const DEFAULT_MODEL = 'gemini';