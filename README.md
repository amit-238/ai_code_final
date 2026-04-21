# ⚡ AI Code Generator

Generate production-ready code in 18+ languages using Google Gemini — with live streaming, refinement, and unit test generation.

## Setup

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_key_here
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Features

- 18+ programming languages
- Two AI models: Gemini 2.5 Flash (fast) and Gemini 2.5 Pro (smart)
- Beginner / intermediate / production complexity levels
- Live streaming output token by token
- Optional plain-English explanation after the code
- Refine generated code with follow-up prompts
- One-click unit test generation
- Generation history in sidebar with clear button
- Language badge with colour coding on output
- Download generated code as a file
- Rotating fun loading messages
- Dark theme with custom styling

## Project structure

```
.
├── app.py              # Streamlit UI
├── generator.py        # Gemini API calls
├── config.py           # Languages, models, examples, colours
├── test_gemini.py      # Unit tests (run with pytest)
├── requirements.txt
├── README.md
├── .env                # Your API key (never commit this)
├── .gitignore
└── .streamlit/
    └── config.toml     # Dark theme config
```

## Running tests

```bash
pip install pytest
pytest test_gemini.py -v
```
