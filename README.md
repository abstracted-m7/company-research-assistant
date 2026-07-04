# AI-Powered Company Research Assistant

An intelligent web application that automates business research. By simply providing a company name or website URL, this application automatically discovers the official website, crawls its contents, uses LLMs (Large Language Models) to synthesize the data, and generates a downloadable PDF report including competitor analysis.

Built with **Python**, **Flask**, and **Tailwind CSS**.

---

## 🌟 Features

- **Intelligent URL Resolution:** Uses Serper.dev to find the official website if only a company name is provided.
- **Automated Web Crawling:** Extracts clean, meaningful text from target websites while ignoring boilerplate and scripts.
- **AI Synthesis (OpenRouter):** Dynamically processes scraped data using cutting-edge models (GPT-4o, Claude 3.5, etc.) to extract:
  - Company Contact Info & Address
  - Products and Services Summaries
  - Target Audience Pain Points
  - Top Competitors
- **PDF Report Generation:** Instantly builds a formatted, multi-page PDF report.
- **Discord Integration:** Automatically sends the generated PDF and applicant details to a configured Discord channel via Webhook/Bot API.
- **Modern UI:** ChatGPT-style animated chat interface with dark mode and dynamic loading states.

## 📁 Project Structure

```
relu_consultancy/
│
├── app.py                      # Main Flask application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API Keys - excluded from Git)
│
├── docs/                       # Project Documentation
│   ├── Project_Architecture.md # Technical deep-dive
│   └── Deployment_Guide.md     # Instructions for GitHub & Render deployment
│
├── services/                   # Backend API Services
│   ├── crawler.py              # BeautifulSoup web scraper
│   ├── discord.py              # Discord API integration
│   ├── openrouter.py           # LLM processing logic
│   ├── pdf_generator.py        # fpdf2 PDF creation
│   └── serper.py               # Google search proxy logic
│
├── static/                     # Frontend Assets
│   ├── css/styles.css          # Custom animations and CSS
│   └── js/app.js               # Frontend chat logic and API fetching
│
└── templates/
    └── index.html              # Main UI layout (Tailwind CSS)
```

## 🚀 Local Setup Instructions

### 1. Prerequisites
- Python 3.10 or higher installed.

### 2. Installation
Clone the repository (or download the files) and navigate to the project directory:
```bash
cd relu_consultancy
```

Create a virtual environment:
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a file named `.env` in the root directory and add your API keys:
```env
SERPER_API_KEY="your_serper_api_key"
OPENROUTER_API_KEY="your_openrouter_api_key"
```
*(Get your free keys at [serper.dev](https://serper.dev/) and [openrouter.ai](https://openrouter.ai/)).*

### 4. Running the Application
Start the Flask development server:
```bash
python app.py
```
Open your web browser and navigate to: **http://127.0.0.1:5000**

## 🌐 Deployment
This application is fully production-ready and configured to be deployed on platforms like **Render.com** using the included `gunicorn` dependency.

For step-by-step deployment instructions, please see the `docs/Deployment_Guide.md` file.

## 🎨 UI/UX Enhancements
- **Dynamic Model Selection:** Switch between different LLMs on the fly.
- **Animations:** Custom CSS keyframes for floating background bubbles, pulsing logos, and smooth message transitions.
- **Responsive Design:** Fully mobile and desktop optimized via Tailwind CSS.
