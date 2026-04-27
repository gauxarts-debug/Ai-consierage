# AI Concierge

AI Concierge is a simple system that converts natural language input into structured intent and retrieves relevant results from the web.

It demonstrates how user intent can be interpreted and mapped to real-world outcomes using AI.

---

## What it does

- Accepts natural language queries  
- Extracts structured intent (category, budget, use case)  
- Searches real-world results from the web  
- Generates short explanations for each result using AI  

---

## Example

Input:
"I want a gaming laptop under 80000"

Output:
- Interpreted intent (category, budget, use case)  
- Relevant results from the web  
- AI-generated explanation for each result  

---

## Project Structure

- `app_ai.py` → Main Streamlit application (AI + web search)  
- `demo.py` → Terminal-based version for quick testing  

---

## Tech Stack

- Python  
- 0  
- 1 API  
- 2 Search  

---

## How to Run

```bash
pip install streamlit openai duckduckgo-search
streamlit run app_ai.py
