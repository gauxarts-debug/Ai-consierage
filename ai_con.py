import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS
import json

# --- CONFIG ---
client = OpenAI(api_key="YOUR_API_KEY_HERE")

# --- AI: INTENT PARSER ---
def parse_intent(user_input):
    prompt = f"""
    Extract structured intent from this query:
    "{user_input}"

    Return only JSON with:
    category, budget, use_case
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {"category": None, "budget": None, "use_case": None}


# --- REAL SEARCH ---
def search_products(query):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append({
                "title": r["title"],
                "link": r["href"],
                "snippet": r["body"]
            })

    return results


# --- AI: EXPLANATION ---
def explain_result(result, intent):
    prompt = f"""
    User is looking for: {intent}

    Explain briefly why this result is relevant:
    Title: {result['title']}
    Description: {result['snippet']}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# --- UI ---
st.set_page_config(page_title="AI Concierge", layout="centered")

st.title("AI Concierge")
st.write("Describe what you're looking for. The system will interpret your request and show relevant results from the web.")

user_input = st.text_input(
    "Enter your request",
    placeholder="Example: gaming laptop under 80000"
)

if user_input:
    with st.spinner("Understanding your request..."):
        intent = parse_intent(user_input)

    st.subheader("Interpreted Request")
    st.json(intent)

    # Build search query
    query_parts = [
        intent.get("use_case") or "",
        intent.get("category") or "",
        f"under {intent.get('budget')}" if intent.get("budget") else ""
    ]
    search_query = " ".join(query_parts)

    with st.spinner("Searching the web..."):
        results = search_products(search_query)

    st.subheader("Results")

    if results:
        for r in results:
            st.markdown(f"**{r['title']}**")
            st.write(r["snippet"])
            st.write(r["link"])

            with st.spinner("Generating explanation..."):
                explanation = explain_result(r, intent)

            st.write(explanation)
            st.write("---")
    else:
        st.warning("No results found. Try rephrasing your request.")
