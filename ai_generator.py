import json
import os
import re
from typing import Dict, Any, List, Optional
from google import genai
from google.genai import types
from sample_data import SAMPLE_COURSES

class AIGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini Client: {e}")

    def generate_study_kit(
        self,
        pdf_text: str,
        filename: str = "document.pdf",
        num_mcqs: int = 10,
        difficulty: str = "All Levels",
        focus_mode: str = "Comprehensive",
        custom_api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a complete NPTEL Exam Prep kit (Key points, Conceptual explanations,
        MCQs with NPTEL exam styling, Flashcards, and Doubts).
        """
        key_to_use = custom_api_key or self.api_key
        client = None
        
        if key_to_use:
            try:
                client = genai.Client(api_key=key_to_use)
            except Exception as e:
                print(f"Failed to initialize client with provided key: {e}")

        # If we have a working client, call Gemini API
        if client:
            try:
                return self._call_gemini_study_kit(
                    client=client,
                    pdf_text=pdf_text,
                    filename=filename,
                    num_mcqs=num_mcqs,
                    difficulty=difficulty,
                    focus_mode=focus_mode
                )
            except Exception as e:
                print(f"Gemini API call failed: {e}. Falling back to smart extracted response.")
                # Fall back to smart template synthesis
                fallback = self._synthesize_fallback(pdf_text, filename, num_mcqs)
                fallback["ai_mode"] = "offline_fallback"
                fallback["fallback_notice"] = f"AI Generation Notice: Gemini API returned: '{str(e)[:100]}...'. Running in smart offline mode. You can check your API key in Settings."
                return fallback
        else:
            # Smart synthesized response for zero-key experience
            fallback = self._synthesize_fallback(pdf_text, filename, num_mcqs)
            fallback["ai_mode"] = "demo_mode"
            fallback["fallback_notice"] = "Running in Demo / Offline Mode. Enter a free Gemini API key in the top bar to get real-time generative analysis on custom documents!"
            return fallback

    def _call_gemini_study_kit(
        self,
        client: genai.Client,
        pdf_text: str,
        filename: str,
        num_mcqs: int,
        difficulty: str,
        focus_mode: str
    ) -> Dict[str, Any]:
        """
        Calls Gemini 2.5 Flash / 1.5 Flash with structured output instructions.
        """
        # Trim text if exceedingly long (e.g. keep first 45,000 chars which is ~10,000 words, plenty for a lecture)
        truncated_text = pdf_text[:50000] if len(pdf_text) > 50000 else pdf_text

        prompt = f"""
You are an expert NPTEL (National Programme on Technology Enhanced Learning - IIT/IISc) Professor and Exam Coordinator.
Analyze the following lecture notes/document and generate a high-yield NPTEL Exam Preparation Kit.

DOCUMENT FILENAME: {filename}
FOCUS MODE: {focus_mode}
REQUESTED MCQ COUNT: {num_mcqs}
DIFFICULTY PREFERENCE: {difficulty}

DOCUMENT CONTENT:
\"\"\"
{truncated_text}
\"\"\"

Produce a valid JSON object matching the exact schema below. Do not wrap in markdown quotes if possible, output raw JSON.

JSON Schema:
{{
  "title": "Clear concise course or lecture title",
  "week_or_topic": "e.g., Week X: Topic Name",
  "overview": "2-3 sentences summarizing the core goals and exam relevance of this material.",
  "key_points": [
    {{
      "category": "Core Concept / Formula / Definition / Exam Pitfall",
      "title": "Concise key point title",
      "content": "Clear, high-yield explanation with LaTeX math like $E = mc^2$ or code where relevant."
    }}
  ],
  "conceptual_explanations": [
    {{
      "topic": "Topic Name",
      "analogy": "An intuitive real-world analogy explaining this concept simply",
      "deep_dive": "Technical and conceptual explanation, why it works, steps, and formulas",
      "key_takeaway": "Specific tip or common trap that NPTEL professors test in exams"
    }}
  ],
  "mcqs": [
    {{
      "id": "q1",
      "question": "Clear exam question statement. Can use LaTeX math like $O(N \\log N)$.",
      "options": [
        "A) Option 1",
        "B) Option 2",
        "C) Option 3",
        "D) Option 4"
      ],
      "correct_answers": [0], // 0-based indices of correct options (e.g. [0] for A, or [0, 2] for A and C in MSQ)
      "type": "single", // "single" for Single Choice or "multiple" for Multiple Select Question (NPTEL format)
      "difficulty": "Easy", // "Easy", "Medium", or "Hard"
      "explanation": "Detailed explanation of why the correct option is right and why others are wrong.",
      "hint": "Short revision hint",
      "topic_tag": "Specific subtopic"
    }}
  ],
  "flashcards": [
    {{
      "front": "Question, formula, or term to define",
      "back": "Concise high-yield answer or definition",
      "tag": "Subtopic tag"
    }}
  ],
  "sample_doubts": [
    "3 relevant, thoughtful doubt questions a student might ask about this specific lecture"
  ]
}}

Requirements:
1. Provide at least 5 key points and 3-4 conceptual explanations.
2. Provide exactly {num_mcqs} high-quality MCQs formatted strictly following NPTEL exam patterns (mix of conceptual, application, and formula/numerical questions).
3. Provide at least 5 flashcards for quick revision.
4. Ensure valid JSON without trailing commas or syntax errors.
"""
        
        # Try gemini-2.5-flash or gemini-1.5-flash
        models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]
        last_error = None
        
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2
                    )
                )
                
                raw_text = response.text.strip()
                # Clean any markdown code blocks if present
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:]
                if raw_text.startswith("```"):
                    raw_text = raw_text[3:]
                if raw_text.endswith("```"):
                    raw_text = raw_text[:-3]
                    
                parsed_json = json.loads(raw_text.strip())
                parsed_json["ai_mode"] = "live_gemini"
                parsed_json["model_used"] = model_name
                return parsed_json
            except Exception as e:
                last_error = e
                continue
                
        raise last_error or Exception("Failed to generate content with Gemini models.")

    def _synthesize_fallback(self, pdf_text: str, filename: str, num_mcqs: int) -> Dict[str, Any]:
        """
        Intelligently builds a high-yield study kit directly from the document text
        when offline or before an API key is provided.
        """
        # Look if the text matches any known topics, or parse headings
        clean_text = pdf_text.strip()
        lines = [
            l.strip() for l in clean_text.split("\n") 
            if len(l.strip()) > 3 and not re.match(r'^---\s*Page\s*\d+\s*---$', l.strip(), re.IGNORECASE)
        ]
        
        title = filename.replace(".pdf", "").replace("_", " ").title()
        if lines:
            candidate = lines[0]
            if len(candidate) < 80:
                title = candidate

        # Extract potential topics and bullet points
        bullet_points = []
        for line in lines:
            if line.startswith(('-', '*', '•', '1.', '2.', '3.')) and len(line) > 15:
                bullet_points.append(re.sub(r'^[-*•\d\.]+\s*', '', line))
            if len(bullet_points) >= 10:
                break
                
        if not bullet_points:
            bullet_points = [
                "Fundamental definitions, terminology, and operational scope.",
                "Theoretical underpinnings and core mathematical theorems.",
                "Architecture, system blocks, and interconnection models.",
                "Performance metrics, time/space complexity, and throughput factors.",
                "Common exam pitfalls and frequent assignment question patterns."
            ]

        key_points = [
            {
                "category": "Core Principle",
                "title": f"Key Concept from {title[:35]}",
                "content": bullet_points[0] if len(bullet_points) > 0 else "Primary architectural definitions and working model."
            },
            {
                "category": "Definition",
                "title": "Fundamental Terminology",
                "content": bullet_points[1] if len(bullet_points) > 1 else "Essential characteristics and operational mechanisms described in the lecture."
            },
            {
                "category": "Analysis",
                "title": "System Properties & Trade-offs",
                "content": bullet_points[2] if len(bullet_points) > 2 else "Trade-offs between performance, scalability, and resource overhead."
            },
            {
                "category": "Formula / Metric",
                "title": "Performance Evaluation",
                "content": bullet_points[3] if len(bullet_points) > 3 else "Key quantitative equations, boundary conditions, and evaluation metrics."
            },
            {
                "category": "Exam Pitfall",
                "title": "NPTEL Common Exam Trap",
                "content": bullet_points[4] if len(bullet_points) > 4 else "Pay close attention to edge cases, zero-indexing, and boundary conditions during numerical problems."
            }
        ]

        conceptual_explanations = [
            {
                "topic": f"1. Architectural Overview of {title[:30]}",
                "analogy": "Imagine a highway system with structured lanes—each layer has a designated role to prevent bottlenecks and ensure efficient flow.",
                "deep_dive": f"The lecture breaks down the foundational architecture into modular layers. Each module encapsulates its internal logic while exposing clean interfaces. In NPTEL assignments, questions often test the handoff mechanism between these layers.",
                "key_takeaway": "Focus on the data flow and sequence of execution between components."
            },
            {
                "topic": "2. Core Mechanisms and Algorithms",
                "analogy": "Like a recipe where the sequence of ingredients dictates the outcome, order of operations is critical.",
                "deep_dive": "The algorithm balances computational efficiency against memory usage. Understanding state transitions, invariants, and termination conditions is essential for assignment problem sets.",
                "key_takeaway": "Always verify edge conditions when tracing execution on paper."
            },
            {
                "topic": "3. Performance Metrics and Optimization",
                "analogy": "Similar to measuring a car by top speed, fuel efficiency, and braking distance.",
                "deep_dive": "NPTEL examinations frequently feature quantitative questions requiring calculation of throughput, latency, efficiency, or asymptotic complexity bounds.",
                "key_takeaway": "Memorize the core metric formulas and units before the final proctored exam."
            }
        ]

        # Generate realistic MCQs
        mcqs = []
        for i in range(1, num_mcqs + 1):
            diff = "Easy" if i <= max(2, num_mcqs // 3) else ("Medium" if i <= max(4, 2 * num_mcqs // 3) else "Hard")
            mcqs.append({
                "id": f"gen_q{i}",
                "question": f"Question {i}: Based on the lecture on '{title[:40]}', which of the following statements is conceptually TRUE?",
                "options": [
                    f"A) The primary mechanism prioritizes deterministic throughput and modular abstraction.",
                    f"B) The system relies entirely on unconstrained static allocation without verification.",
                    f"C) Boundary conditions are disregarded in high-throughput environments.",
                    f"D) None of the operational invariants hold under standard constraints."
                ],
                "correct_answers": [0],
                "type": "single",
                "difficulty": diff,
                "explanation": f"Option A is correct: The foundational principle emphasized throughout the lecture material focuses on structured abstraction and deterministic execution. Options B, C, and D contradict core principles.",
                "hint": "Look for the answer that reflects standard engineering design principles.",
                "topic_tag": "Lecture Concepts"
            })

        flashcards = [
            {
                "front": f"Core definition of {title[:35]}",
                "back": key_points[0]["content"],
                "tag": "Definition"
            },
            {
                "front": "Primary trade-off discussed in this lecture",
                "back": key_points[2]["content"],
                "tag": "Trade-offs"
            },
            {
                "front": "Key formula / performance relationship",
                "back": key_points[3]["content"],
                "tag": "Formulas"
            },
            {
                "front": "What is the most frequent student misconception?",
                "back": key_points[4]["content"],
                "tag": "Exam Traps"
            }
        ]

        sample_doubts = [
            f"Can you explain the main difference between the first two topics in {title[:30]}?",
            "What numerical formula from this lecture is most tested in NPTEL assignments?",
            "Could you give a step-by-step example problem solved from scratch?"
        ]

        return {
            "title": title,
            "week_or_topic": "NPTEL Lecture Module",
            "overview": f"Comprehensive NPTEL study guide and exam simulator compiled from '{filename}'. Includes high-yield points, conceptual breakdown, and practice question bank.",
            "key_points": key_points,
            "conceptual_explanations": conceptual_explanations,
            "mcqs": mcqs,
            "flashcards": flashcards,
            "sample_doubts": sample_doubts
        }

    def answer_doubt(
        self,
        doubt: str,
        context_text: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        custom_api_key: Optional[str] = None
    ) -> str:
        """
        Answers a student's doubt regarding the lecture notes or exam preparation.
        """
        key_to_use = custom_api_key or self.api_key
        client = None
        if key_to_use:
            try:
                client = genai.Client(api_key=key_to_use)
            except Exception:
                pass

        if client:
            try:
                prompt = f"""
You are a warm, encouraging, top-tier IIT professor and NPTEL TA.
A student preparing for their upcoming NPTEL proctored examination has asked a doubt.
Answer thoroughly, clearly, and concisely using the lecture context provided. Use markdown, intuitive analogies, and LaTeX math formulas (e.g. $O(N)$ or equation blocks) where helpful.

STUDENT'S DOUBT:
{doubt}

LECTURE MATERIAL CONTEXT:
\"\"\"
{context_text[:25000]}
\"\"\"

Provide an encouraging, clear, and step-by-step explanation. Conclude with a quick 'NPTEL Exam Tip' related to this doubt.
"""
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                return response.text
            except Exception as e:
                print(f"Chat error with Gemini: {e}")

        # Intelligent offline response
        return f"""
### 💡 Concept Explanation & Guidance

Regarding your question: **"{doubt}"**

1. **Core Principle:** In NPTEL examinations, questions on this topic generally probe whether you understand the fundamental mechanism rather than just memorized definitions.
2. **Key Clarification:** Ensure you distinguish between input assumptions (e.g., non-negative weights, synchronous vs asynchronous models) and system guarantees.
3. **Common Pitfall:** Many students confuse the worst-case boundary conditions with average-case expectations.

> 🎓 **NPTEL Exam Pro-Tip:** When answering week assignment questions and final proctored exam questions on this topic, check whether the question is Single Choice (1 mark) or Multiple Select (2 marks with no negative marking or partial marking). Always write down the core equation first!

*(Tip: To get live interactive answers from Gemini 2.5 Flash tailored to every detail of your lecture notes, add your free Gemini API key in the top bar!)*
"""
