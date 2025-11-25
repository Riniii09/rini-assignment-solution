import os
# Suppress gRPC verbose logging
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

import streamlit as st
import json
import re
from typing import Dict, Any
from google import genai

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Prompt Context Analyzer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Prompt Context Analyzer")

# ---------------------------------------------------------
# SIDEBAR — API KEY
# ---------------------------------------------------------
st.sidebar.header("🔑 Configuration")

api_key = st.sidebar.text_input(
    "Enter Gemini API Key:",
    type="password",
    placeholder="AIza..."
)

client = None
if api_key:
    # Clean the API key (remove whitespace, newlines)
    api_key = api_key.strip()
    client = genai.Client(api_key=api_key)


# ---------------------------------------------------------
# FUNCTION: SAFE JSON PARSE
# ---------------------------------------------------------
def safe_json_loads(text: str) -> Any:
    """
    Cleans and parses JSON safely.
    Removes markdown, ```json blocks, stray characters, etc.
    """
    clean = text.strip()

    # Remove fences like ```json ... ```
    clean = re.sub(r"```json|```", "", clean).strip()

    # Remove weird backticks
    clean = clean.replace("`", "")

    # Attempt to parse
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON", "raw": clean}


# ---------------------------------------------------------
# FUNCTION: ASK GEMINI FOR CONTEXT ANALYSIS
# ---------------------------------------------------------
def analyze_prompt(user_prompt: str, ai_reply: str) -> Dict:
    analysis_instruction = """
You are a **CRITICAL AUDITOR**. Your sole purpose is to find flaws in the AI REPLY relative to the USER PROMPT.

**MANDATORY RULE:** You MUST be critical. If you cannot find a specific flaw, you MUST add a generic, high-level suggestion for ELABORATION to the 'unclear_points' list. For example, 'The AI reply lacks specific examples and real-world applicability.' DO NOT leave all lists empty.

Return ONLY a JSON object (no markdown, no backticks, no explanation) with the exact structure:

{{
  "missing_details": ["if nothing add some generic elaboration suggestion here, ..."],
  "unclear_points": ["if nothing add some generic elaboration suggestion here, ..."],
  "contradictions": ["if nothing add some generic elaboration suggestion here, ..."],
  "unanswered_parts": ["if nothing add some generic elaboration suggestion here, ..."]
}}

**FIELD DEFINITIONS:**
- **missing_details:** Specific facts/constraints requested (e.g., date, format, location) that are absent.
- **unclear_points:** Ambiguous statements, jargon, or areas where the AI's explanation is too shallow/general.
- **contradictions:** Conflicts between statements.
- **unanswered_parts:** Explicit questions/requests ignored by the AI.
**IMPORTANT:** Even if you find no issues, you MUST add at least one generic suggestion for elaboration to the 'unclear_points' list.
Rules:
- Output ONLY valid JSON.
- No explanations, no markdown, no ```json blocks.
"""

    full_text = f"{analysis_instruction}\n\nUSER PROMPT:\n{user_prompt}\n\nAI REPLY:\n{ai_reply}"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_text
    )
    
    raw = response.text

    return safe_json_loads(raw)


# ---------------------------------------------------------
# UI — INPUTS FROM USER
# ---------------------------------------------------------
st.subheader("📝 Input Area")

user_prompt = st.text_area("Enter User Prompt:", height=150)
ai_reply = st.text_area("Enter AI Reply:", height=150)

if st.button("Analyze", type="primary"):
    if not api_key:
        st.error(" Please enter Gemini API Key in sidebar.")
    elif not client:
        st.error(" Gemini client could not be initialized.")
    elif not user_prompt or not ai_reply:
        st.error(" Both fields are required.")
    else:
        with st.spinner("Analyzing using Gemini..."):
            try:
                result = analyze_prompt(user_prompt, ai_reply)

                st.subheader("📘 Context Analysis Result")
                st.json(result)

                # ---------------------------------------------------------
                # FOLLOW-UP QUESTIONS (Gemini generated)
                # ---------------------------------------------------------
                st.subheader("✨ Follow-up Suggestions")

                followup_prompt = """
Generate 3 follow-up questions for the user based on this prompt/reply.
Return ONLY a numbered list in plain text.
"""

                try:
                    followup = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=followup_prompt + f"\n\nUSER PROMPT:\n{user_prompt}\n\nAI REPLY:\n{ai_reply}"
                    )
                    st.write(followup.text)
                except Exception as e:
                    st.warning(f"Could not generate follow-ups: {e}")

            except Exception as e:
                st.error(f" Analysis failed: {e}")
                st.info("💡 Make sure your API key is valid and you have access to Gemini models.")

# ---------------------------------------------------------
# SIDEBAR: Test API Key
# ---------------------------------------------------------
if api_key:
    st.sidebar.divider()
    if st.sidebar.button("🧪 Test API Key"):
        try:
            test_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents="Say 'Hello! API is working.'"
            )
            st.sidebar.success("✅ API Key is valid!")
            st.sidebar.write(test_response.text)
        except Exception as e:
            st.sidebar.error(f" API test failed: {e}")