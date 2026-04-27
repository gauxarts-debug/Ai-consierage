import streamlit as st
import re

# --- MOCK DATABASE ---
PRODUCTS = [
    {"name": "Acer Nitro 5", "price": 75000, "category": "laptop", "use": "gaming"},
    {"name": "HP Pavilion", "price": 65000, "category": "laptop", "use": "general"},
    {"name": "Dell G15", "price": 82000, "category": "laptop", "use": "gaming"},
    {"name": "iPhone 13", "price": 70000, "category": "phone", "use": "general"},
    {"name": "Realme Narzo", "price": 15000, "category": "phone", "use": "budget"},
]

# --- SIMPLE INTENT PARSER ---
def parse_intent(text):
    text = text.lower()

    category = None
    if "laptop" in text:
        category = "laptop"
    elif "phone" in text:
        category = "phone"

    use_case = None
    if "gaming" in text:
        use_case = "gaming"
    elif "budget" in text:
        use_case = "budget"

    budget = None
    numbers = re.findall(r'\d+', text)
    if numbers:
        budget = int(numbers[0])

    return {
        "category": category,
        "use_case": use_case,
        "budget": budget
    }

# --- MATCH ENGINE ---
def match_products(intent):
    results = []
    for p in PRODUCTS:
        if intent["category"] and p["category"] != intent["category"]:
            continue
        if intent["use_case"] and p["use"] != intent["use_case"]:
            continue
        if intent["budget"] and p["price"] > intent["budget"]:
            continue
        results.append(p)
    return results

# --- UI ---
st.title("AI Concierge (Mini)")

user_input = st.text_input("What do you want?")

if user_input:
    intent = parse_intent(user_input)

    st.subheader("Parsed Intent")
    st.json(intent)

    results = match_products(intent)

    st.subheader("Results")
    if results:
        for r in results:
            st.write(f"{r['name']} - ₹{r['price']}")
    else:
        st.write("No matching products found.")
