import os
import requests
import logging

HUGGING_MODELS = [
    {"name": "GPT-2", "id": "gpt2"},
    {"name": "DistilGPT2", "id": "distilgpt2"},
    {"name": "BLOOM", "id": "bigscience/bloom"},
]

HUGGING_FACE_API_KEY = os.getenv("HF_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Setup basic logging
logging.basicConfig(level=logging.INFO)

async def get_ai_response(prompt, model_id):
    # Try HuggingFace
    if not HUGGING_FACE_API_KEY:
        logging.warning("Missing HuggingFace API key.")
    else:
        response = hugging_face_request(prompt, model_id)
        if response:
            return response
        else:
            logging.info(f"HuggingFace model '{model_id}' did not return a response.")

    # Try Perplexity
    if not PERPLEXITY_API_KEY:
        logging.warning("Missing Perplexity API key.")
    else:
        response = perplexity_request(prompt)
        if response:
            return response
        else:
            logging.info("Perplexity did not return a response.")

    # Fallback error message
    logging.error("All AI providers failed to respond.")
    return "Sorry, AI service is temporarily unavailable. Please check API keys and service status, then try again later."

def hugging_face_request(prompt, model_id):
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    data = {"inputs": prompt}
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=8)
        if resp.status_code == 200:
            result = resp.json()
            # Handle different possible response formats
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]
            elif "generated_text" in result:
                return result["generated_text"]
            elif isinstance(result, str):
                return result
            else:
                logging.info(f"Unexpected HuggingFace response format: {result}")
        else:
            logging.warning(f"HuggingFace API error {resp.status_code}: {resp.text}")
        return None
    except Exception as e:
        logging.error(f"HuggingFace request exception: {e}")
        return None

def perplexity_request(prompt):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {PERPLEXITY_API_KEY}"}
    data = {"model": "pplx-7b-online", "messages": [{"role": "user", "content": prompt}]}
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=8)
        if resp.status_code == 200:
            result = resp.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", None)
        else:
            logging.warning(f"Perplexity API error {resp.status_code}: {resp.text}")
        return None
    except Exception as e:
        logging.error(f"Perplexity request exception: {e}")
        return None
