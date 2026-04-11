# Understanding `simple_agent.py` (The Brain of the Tool)

If `app.py` is the face of this project, `simple_agent.py` is the **brain**. This file contains the actual "Artificial Intelligence" work. 

In simple layman's terms, this file creates a virtual team of 3 specialized AI workers (called "Agents"). They work together like an assembly line to answer the user's question.

## The Assembly Line

### Worker 1: The Researcher Agent
* **What it does:** It acts like a fast-reading intern. 
* **How it works:** When the user asks for a tool (like "I need a free database viewer"), the Researcher takes that question, goes to Google (via a tool called **Tavily**), and quickly reads the top search results. It then pulls out the raw facts, names, and summaries of what it found.

### Worker 2: The Synthesizer Agent
* **What it does:** It acts like a senior editor.
* **How it works:** It takes that messy pile of raw facts from the Researcher, cuts out the nonsense, and picks the absolute **Top 3** best tools. It then writes a clean, easy-to-read summary for each tool, including bullet points for Pros and Cons, Pricing, and a final verdict.

### Worker 3: The Judge Agent
* **What it does:** It acts like an AI teacher grading a test.
* **How it works:** Before the final answer is sent back to the user, the Judge looks at the Synthesizer's Top 3 list. It asks: "Did the AI actually answer the user's question? Is it accurate? Is it easy to read?" The Judge then gives a score from 1 to 5 for different categories (Relevancy, Clarity, Completeness) and writes a brief reason for why it gave that score.

## How They Connect (The Pipeline)
At the very bottom of the file, there is a function called `run_pipeline`. This is the team manager. It simply takes the user's question and passes it from the Researcher $\rightarrow$ to the Synthesizer $\rightarrow$ to the Judge. Finally, it bundles up all their work and hands it back to the web page to be displayed.
