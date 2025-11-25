# rini-assignment-solution

Project Scope

1. Context Analysis
   ○ Take a user’s original prompt and the AI’s reply (you may mock this or
   integrate an actual LLM).
   ○ Compare these texts to identify gaps, missing details, or unclear points.

What I understand:

- we can use the gaps, missing details, unclear points, inconsistencies in the prompts and show it in the analysis later on for perfect interpretation

2. Prompt Suggestions
   ○ Generate 2–3 concise follow-up prompts that could help clarify or expand the
   conversation.
   ○ These might focus on elaboration (e.g., “Explain in detail”) or corrections
   (e.g., “Double-check this part”).
   What I understand:

- we can show all the possible concise prompts and give it a how-related-it-is score in the analysis dashboard for even more options

3. Basic UI
   ○ Present your suggestions in a simple, user-friendly format—this can be a web
   interface, a console application, or a browser extension overlay.

What I understand:

- We should use streamlit

4. Documentation
   ○ Provide a short explanation of how your context analysis works, which
   models/libraries you used, and any assumptions made.

What I understand:

- A good doc like this in proper readme format (md format)

Technical Guidelines
● Data & Models
○ Feel free to use pretrained NLP/LLM libraries (e.g., spaCy, Hugging Face
Transformers, OpenAI API).
○ Focus on how you process and evaluate the text rather than training from
scratch.
● Reasoning Approach
○ You can use rule-based logic, semantic embeddings, or a fine-tuned
model—whatever fits the 2 hr timeline.
○ The key is to demonstrate how you identify and fill gaps in the AI’s response.
● Code Structure
○ Organize your code and keep it readable. Provide comments or docstrings
explaining key steps

Evaluation Criteria

1. Technical Understanding (40%)
   ○ Quality of context analysis, approach to suggestion generation, and effective
   use of ML/NLP techniques.
2. Functionality & Completeness (30%)
   ○ Does the prototype run smoothly? Do the suggestions make sense and align
   with user queries?
3. Creativity & Problem-Solving (20%)
   ○ Novel methods for detecting gaps or delivering prompts, any unique UX/UI
   choices, or interesting expansions.
4. Documentation & Presentation (10%)
   ○ Clarity of the ReadMe and (if provided) the demo video. Is it easy to run and
   understand your work?
