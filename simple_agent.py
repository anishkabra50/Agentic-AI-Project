"""
simple_agent.py — Lightweight 3-Agent Pipeline for Developer Tool Finder

Agents:
  1. Researcher Agent  — Uses Gemini + Tavily to search the web for tools.
  2. Synthesizer Agent — Cleans raw data into a top-3 comparison.
  3. Judge Agent       — LLM-as-Judge: scores the final output on a rubric.

No heavy frameworks. Pure Python + google-genai + tavily-python.
"""

import os
import json
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient

load_dotenv()

# ── Clients ──────────────────────────────────────────────────────────────────

def get_api_key(name):
    """Universal helper to get keys from Streamlit Cloud Secrets or local .env"""
    try:
        import streamlit as st
        if name in st.secrets:
            return st.secrets[name]
    except (ImportError, RuntimeError):
        pass
    return os.getenv(name)

gemini_key = get_api_key("GEMINI_API_KEY")
tavily_key = get_api_key("TAVILY_API_KEY")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file or Streamlit Secrets.")

client = genai.Client(api_key=gemini_key)
tavily_client = TavilyClient(api_key=tavily_key)

MODEL_NAME = "gemini-1.5-flash" 


# ─────────────────────────────────────────────────────────────────────────────
#  AGENT 1 — Researcher
#  Responsibility: Take the user query, search Tavily, return raw facts.
# ─────────────────────────────────────────────────────────────────────────────

def run_researcher(user_query: str) -> str:
    """
    Searches the web via Tavily and asks Gemini to pull out the key facts
    about developer tools that match the user's request.
    """

    # Step 1 — Tavily web search
    search_response = tavily_client.search(
        query=user_query,
        max_results=5,
        search_depth="basic",
    )

    # Combine snippets into one block of text for Gemini to read
    snippets = []
    for result in search_response.get("results", []):
        title = result.get("title", "")
        content = result.get("content", "")
        url = result.get("url", "")
        snippets.append(f"**{title}**\n{content}\nSource: {url}\n")

    raw_web_data = "\n---\n".join(snippets)

    # Step 2 — Gemini extracts structured facts from the raw web data
    prompt = f"""You are a Researcher Agent.

The user is looking for developer tools: "{user_query}"

Below are web search results. Extract ALL developer tools mentioned,
along with any facts you find (what the tool does, pricing, platform,
official website URL).  Return the information as a bullet-point list.
Do NOT make up tools that are not in the search results.

--- WEB SEARCH RESULTS ---
{raw_web_data}
--- END ---

Return only the extracted facts as bullet points."""

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=prompt
    )
    return response.text


# ─────────────────────────────────────────────────────────────────────────────
#  AGENT 2 — Synthesizer
#  Responsibility: Take raw facts → produce a clean Top-3 recommendation.
# ─────────────────────────────────────────────────────────────────────────────

def run_synthesizer(user_query: str, raw_facts: str) -> str:
    """
    Takes the raw bullet-point facts from the Researcher and produces
    a clean, formatted comparison of the Top 3 tools.
    """

    prompt = f"""You are a Synthesizer Agent.

The user asked: "{user_query}"

A Researcher Agent found these raw facts from the web:
{raw_facts}

Your job:
1. Pick the **Top 3** most relevant tools for the user's needs.
2. For each tool, provide:
   - **Name**
   - **What it does** (1-2 sentences)
   - **Pricing** (Free / Paid / Freemium)
   - **Platforms** (Windows, Mac, Linux, Web, etc.)
   - **Pros** (2-3 bullet points)
   - **Cons** (1-2 bullet points)
   - **Official Link** (if available)
3. End with a brief **Verdict** sentence recommending the best overall pick.

Format the output in clean, readable Markdown.
Do NOT add any tools that were not in the raw facts."""

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=prompt
    )
    return response.text


# ─────────────────────────────────────────────────────────────────────────────
#  AGENT 3 — Judge  (LLM-as-Judge)
#  Responsibility: Evaluate the Synthesizer's output using a rubric.
# ─────────────────────────────────────────────────────────────────────────────

def run_judge(user_query: str, final_recommendations: str) -> dict:
    """
    Evaluates the quality of the final recommendations using a strict rubric.
    Returns a Python dict with scores and reasoning.
    """

    prompt = f"""You are a Judge Agent performing an LLM-as-Judge evaluation.

The user's original query was: "{user_query}"

The system produced this recommendation:
--- RECOMMENDATION START ---
{final_recommendations}
--- RECOMMENDATION END ---

Evaluate the recommendation using this rubric.  Score each criterion from 1 to 5:

1. **Relevance** — Are the recommended tools actually relevant to what the user asked for?
2. **Accuracy**  — Are the facts (pricing, platforms, descriptions) correct based on general knowledge?
3. **Completeness** — Does the recommendation cover enough options with pros/cons?
4. **Clarity** — Is the output well-structured, readable, and easy to understand?

Return ONLY valid JSON in this exact format (no markdown fencing, no extra text):
{{
  "scores": {{
    "relevance": {{"score": <1-5>, "reason": "<brief reason>"}},
    "accuracy": {{"score": <1-5>, "reason": "<brief reason>"}},
    "completeness": {{"score": <1-5>, "reason": "<brief reason>"}},
    "clarity": {{"score": <1-5>, "reason": "<brief reason>"}}
  }},
  "overall_score": <average of the four scores, rounded to 1 decimal>,
  "summary": "<1-2 sentence overall assessment>"
}}"""

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=prompt
    )
    raw_text = response.text.strip()

    # Clean up potential markdown fencing from Gemini
    if raw_text.startswith("```"):
        raw_text = raw_text.split("\n", 1)[1]  # remove first line
    if raw_text.endswith("```"):
        raw_text = raw_text.rsplit("```", 1)[0]
    raw_text = raw_text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback: return a basic structure so the UI doesn't break
        return {
            "scores": {
                "relevance":    {"score": "N/A", "reason": "Could not parse judge output."},
                "accuracy":     {"score": "N/A", "reason": "Could not parse judge output."},
                "completeness": {"score": "N/A", "reason": "Could not parse judge output."},
                "clarity":      {"score": "N/A", "reason": "Could not parse judge output."},
            },
            "overall_score": "N/A",
            "summary": raw_text,  # show raw text as fallback
        }


# ─────────────────────────────────────────────────────────────────────────────
#  PIPELINE — Runs all 3 agents sequentially
# ─────────────────────────────────────────────────────────────────────────────

def run_pipeline(user_query: str) -> dict:
    """
    Orchestrates the full 3-agent pipeline:
      Researcher → Synthesizer → Judge
    Returns a dict with all intermediate and final outputs.
    """

    # Agent 1
    raw_facts = run_researcher(user_query)

    # Agent 2
    recommendations = run_synthesizer(user_query, raw_facts)

    # Agent 3
    judge_result = run_judge(user_query, recommendations)

    return {
        "raw_research":     raw_facts,
        "recommendations":  recommendations,
        "judge":            judge_result,
    }
