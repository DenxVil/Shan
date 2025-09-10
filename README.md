# Telegram AI Chatbot

A modular Telegram bot using Hugging Face and Perplexity AI models, with fallback and model selection.

## Features

- Choose between Hugging Face AI models using Telegram buttons
- Replies with stylish fonts
- Auto fallback: If Hugging Face fails, tries Perplexity, then other APIs
- Easy to add more AI APIs
- Modular Python files for maintainability
- Deploy-ready for Heroku & Render

## File Structure

```
requirements.txt
Procfile
bot/
  main.py
  handlers/
    start.py
    button.py
    message.py
  utils/
    api.py
    style.py
README.md
```

## Setup

1. Clone the repo.
2. Set your environment variables:
   - `TELEGRAM_TOKEN`
   - `HF_API_KEY`
   - `PERPLEXITY_API_KEY`
3. Install requirements:
   ```
pip install -r requirements.txt
   ```
4. Run the bot locally:
   ```
python bot/main.py
   ```

## Deployment

### Heroku

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. `heroku login`
3. Create app:
   ```
heroku create your-app-name
   ```
4. Set environment variables:
   ```
heroku config:set TELEGRAM_TOKEN=xxx HF_API_KEY=xxx PERPLEXITY_API_KEY=xxx
   ```
5. Push code:
   ```
git add .
git commit -m "Deployable bot"
git push heroku main
   ```
6. Done! Bot runs automatically.

### Render

1. Login to [Render](https://render.com/)
2. Create a new Web Service → Connect your repo.
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python bot/main.py`
5. Add environment variables in Render dashboard.
6. Deploy!

## Contributing

Feel free to fork, open issues, or PRs!
