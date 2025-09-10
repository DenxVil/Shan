import os
import requests

HUGGING_MODELS = [
    {"name": "GPT-2", "id": "gpt2"},
    {"name": "DistilGPT2", "id": "distilgpt2"},
    {"name": "BLOOM", "id": "bigscience/bloom"},
]

HUGGING_FACE_API_KEY = os.getenv("HF_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

async def get_ai_response(prompt, model_id):
    response = hugging_face_request(prompt, model_id)
    if response:
        return response
    response = perplexity_request(prompt)
    if response:
        return response
    return "Sorry, no AI is available right now!"

def hugging_face_request(prompt, model_id):
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    data = {"inputs": prompt}
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=8)
        if resp.status_code == 200:
            result = resp.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]
            elif "generated_text" in result:
                return result["generated_text"]
            elif isinstance(result, str):
                return result
        return None
    except Exception:
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
        return None
    except Exception:
        return None
