"""
Chat Router — Tutor matematic inteligent.

Flow:
  1. Dacă exercise_id → explică rezolvarea acelui exercițiu
  2. Dacă mesajul conține o problemă math → detectează și rezolvă pas cu pas
  3. Dacă e o întrebare conceptuală ("ce e derivata?") → explicație din dicționar
  4. Dacă "nu înțeleg pasul X" → re-explică pasul respectiv
  5. Fallback → sugestii utile

Ordinea modelelor: SmartBAC de pe Kaggle (via ngrok) → Qwen LoRA (dacă e
încărcat) → solver rule-based + dicționar de concepte (fallback offline).
"""

import re
import os
import sys
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from database import get_db
from services.math_tutor import solve, explain_wrong_answer, detect_exercise_type
from services.math_explainer import find_concept, get_all_topics

AI_NGROK_URL = os.getenv("AI_NGROK_URL", "")


def _normalize_math_input(text: str) -> str:
    """
    Normalizează input-ul utilizatorului în formatul pe care modelul l-a văzut la antrenare.
    Convertește LaTeX, simboluri Unicode, notații informale → format curat.
    """
    t = text.strip()

    # ─── LaTeX → Unicode/text (formatul din dataset) ───
    latex_map = [
        (r"\\frac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)"),
        (r"\\sqrt\{([^}]*)\}", r"√(\1)"),
        (r"\\sqrt\b", "√"),
        (r"\\int_\{([^}]*)\}\^\{([^}]*)\}", r"∫_\1^\2"),
        (r"\\int\b", "∫"),
        (r"\\sum\b", "∑"),
        (r"\\lim\b", "lim"),
        (r"\\infty\b", "∞"),
        (r"\\pi\b", "π"),
        (r"\\alpha\b", "α"), (r"\\beta\b", "β"), (r"\\gamma\b", "γ"),
        (r"\\theta\b", "θ"), (r"\\lambda\b", "λ"), (r"\\mu\b", "μ"),
        (r"\\sin\b", "sin"), (r"\\cos\b", "cos"), (r"\\tg\b", "tg"),
        (r"\\tan\b", "tg"), (r"\\ln\b", "ln"), (r"\\log\b", "log"),
        (r"\\cdot\b", "·"), (r"\\times\b", "×"), (r"\\div\b", "÷"),
        (r"\\pm\b", "±"), (r"\\mp\b", "∓"),
        (r"\\leq\b", "≤"), (r"\\geq\b", "≥"), (r"\\neq\b", "≠"),
        (r"\\in\b", "∈"), (r"\\subset\b", "⊂"),
        (r"\\cup\b", "∪"), (r"\\cap\b", "∩"),
        (r"\\forall\b", "∀"), (r"\\exists\b", "∃"),
        (r"\\rightarrow\b", "→"), (r"\\Rightarrow\b", "⇒"),
        (r"\\mathbb\{R\}", "ℝ"), (r"\\mathbb\{Z\}", "ℤ"), (r"\\mathbb\{N\}", "ℕ"),
        (r"\\left\s*[\(\[\{]", "("), (r"\\right\s*[\)\]\}]", ")"),
        (r"\\\(|\\\)", ""), (r"\\\[|\\\]", ""),
        (r"\\,|\\;|\\!", " "),
        (r"\\quad", "  "),
        (r"\\text\{([^}]*)\}", r"\1"),
    ]
    for pattern, repl in latex_map:
        t = re.sub(pattern, repl, t)
    # Clean remaining LaTeX backslashes
    t = re.sub(r"\\([a-zA-Z]+)", r"\1", t)

    # ─── Notații informale → format dataset ───
    # "sqrt(x)" / "radical din x" → "√(x)"
    t = re.sub(r"\bradical\s+din\s+", "√", t, flags=re.IGNORECASE)
    t = re.sub(r"\bradical\s*\(", "√(", t, flags=re.IGNORECASE)
    t = re.sub(r"\bradical\b", "√", t, flags=re.IGNORECASE)
    t = re.sub(r"\bsqrt\(", "√(", t, flags=re.IGNORECASE)
    t = re.sub(r"\bsqrt\b", "√", t, flags=re.IGNORECASE)
    # "pi" → "π" (doar când e singur, nu în "pipa")
    t = re.sub(r"\bpi\b", "π", t, flags=re.IGNORECASE)
    # "inf" / "infinit" → "∞"
    t = re.sub(r"\binfinit\b|\binf\b", "∞", t, flags=re.IGNORECASE)
    # "x^2" rămâne "x²" (format dataset)
    sup_map = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
               "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
    def _to_sup(m):
        exp = m.group(1) if m.group(1) else m.group(2)
        if len(exp) == 1 and exp in sup_map:
            return sup_map[exp]
        return "^" + exp
    t = re.sub(r"\^\{([^}]+)\}|\^(\d)", _to_sup, t)
    # "x_1" → "x₁"
    sub_map = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄",
               "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉"}
    def _to_sub(m):
        idx = m.group(1) if m.group(1) else m.group(2)
        if len(idx) == 1 and idx in sub_map:
            return sub_map[idx]
        return "_" + idx
    t = re.sub(r"_\{([^}]+)\}|_(\d)", _to_sub, t)
    # "**" → "^" (Python notation)
    t = t.replace("**", "^")
    # "*" → "·" (multiplication)
    t = re.sub(r"(?<=\w)\*(?=\w)", "·", t)

    # ─── Adaugă prefix dacă lipsește (formatul dataset) ───
    t_lower = t.lower()
    has_prefix = any(t_lower.startswith(p) for p in [
        "rezolv", "calcul", "determin", "demonstr", "arăta", "arata",
        "fie ", "se consider", "bac ", "aflat", "scrie", "găsi", "gasi",
        "după", "dupa", "suma ", "produsul", "media",
    ])

    if not has_prefix:
        # Întrebări conceptuale — NU adăugăm prefix matematic
        if re.search(r"ce (e|este|sunt|inseamna)|explica|cum (se|func)|definiti|regul|formul|invata|ajutor|help", t_lower):
            pass
        elif re.search(r"deriv|f['\u2032]", t_lower):
            t = f"Calculează derivata: {t}"
        elif re.search(r"∫|integra|primitiv", t_lower):
            t = f"Calculează integrala: {t}"
        elif re.search(r"\blim\b|limita", t_lower):
            t = f"Calculează limita: {t}"
        elif re.search(r"\bdet\b|determinant", t_lower):
            t = f"Calculează determinantul: {t}"
        elif re.search(r"C\(\d|combin|aranjam|\bA\(\d", t):
            t = f"Calculează: {t}"
        elif re.search(r"=\s*0|ecuati", t_lower):
            t = f"Rezolvă ecuația: {t}"
        elif "=" in t and re.search(r"[xyzXYZ]", t):
            t = f"Rezolvă ecuația: {t}"
        else:
            t = f"Rezolvă: {t}"

    # Curățare finală
    t = re.sub(r"\s{2,}", " ", t).strip()
    return t


def _ask_kaggle(question: str) -> dict | None:
    """Apelează modelul SmartBAC antrenat pe Kaggle via ngrok."""
    if not AI_NGROK_URL:
        return None
    try:
        import httpx
        base = AI_NGROK_URL.rstrip("/")
        url = base if base.endswith("/ask") else base + "/ask"
        normalized = _normalize_math_input(question)
        print(f"[chat] Kaggle input: {question!r} → {normalized!r}")
        resp = httpx.post(
            url,
            json={"intrebare": normalized},
            timeout=30.0,
        )
        if resp.status_code != 200:
            print(f"[chat] Kaggle HTTP {resp.status_code}: {resp.text[:200]}")
            return None

        data = resp.json()
        raspuns = data.get("raspuns", "").strip()
        if not raspuns:
            return None

        # ─── Parsare răspuns → pași + answer ───
        steps = []
        answer = ""
        metoda = ""
        lines = raspuns.split("\n")

        # Regex pentru a curăța orice prefix de pas
        step_re = re.compile(
            r"^(Pasul|Pas|Step|Stepi|Step final|Etapa)\s*\d*\s*:?\s*",
            re.IGNORECASE,
        )
        answer_re = re.compile(
            r"^(Răspuns|Raspuns|Rezultat|Solutia|Soluția|Answer|Rezultatul)\s*:?\s*",
            re.IGNORECASE,
        )
        skip_re = re.compile(
            r"^(Rezolvare pas cu pas|Thinking|<think>|</think>|---)",
            re.IGNORECASE,
        )

        for line in lines:
            stripped = line.strip()
            if not stripped or skip_re.match(stripped):
                continue
            # Răspuns final
            if answer_re.match(stripped):
                answer = answer_re.sub("", stripped).strip()
                continue
            # Metodă/abordare
            if re.match(r"^(Metoda|Abordare|Folosim|Aplicăm|Aplicam)", stripped, re.IGNORECASE):
                metoda = stripped
                continue
            # Pas — curățăm prefixul
            clean = step_re.sub("", stripped).strip()
            if clean:
                steps.append(clean)

        # Dacă nu am găsit answer explicit, ultimul pas e răspunsul
        if not answer and steps:
            answer = steps.pop() if len(steps) > 1 else steps[-1]

        # Dacă nu sunt pași deloc, împărțim textul în propoziții
        if not steps and raspuns:
            sentences = [s.strip() for s in re.split(r"[.!]\s+", raspuns) if s.strip() and len(s.strip()) > 5]
            steps = sentences[:5] if sentences else [raspuns[:200]]
            if not answer:
                answer = sentences[-1] if sentences else raspuns[:100]

        # ─── Filtru calitate — elimină halucinări ───
        def _is_garbage(s: str) -> bool:
            if not s or len(s) < 3:
                return True
            # Emoji spam
            if any(c in s for c in "😊😂🤔😎👍🎉💪🔥"):
                return True
            # Gibberish: prea multe cuvinte fără sens
            if re.search(r"spunsesemnele|Finalizat!|am spus tot|nu.*am.*spus", s, re.IGNORECASE):
                return True
            # Repetiții inutile: "a₁ = a₁"
            parts = s.split("=")
            if len(parts) == 2 and parts[0].strip() == parts[1].strip():
                return True
            # Prea scurt și fără math
            if len(s) < 5 and not any(c in s for c in "=+-*/^√∫²³<>≤≥"):
                return True
            # English gibberish amestecat
            if re.search(r"\b(th term|finalized|done|sorry)\b", s, re.IGNORECASE):
                return True
            # Doar "..."
            if s.strip() in ("...", "…", "---"):
                return True
            return False

        steps = [s for s in steps if not _is_garbage(s)]

        # Dacă răspunsul e garbage, ia ultimul pas valid
        if _is_garbage(answer) and steps:
            answer = steps[-1]
        elif _is_garbage(answer):
            return None  # răspuns prea prost, fallback la rule-based

        # Dacă nu au rămas pași valizi, returnăm None
        if not steps:
            return None

        tip = detect_exercise_type(question).capitalize()
        if tip == "Necunoscut":
            tip = "Exercițiu"

        structured = {
            "tip": tip,
            "ce_avem": question,
            "ce_aplicam": metoda or "Rezolvare cu DeepSeek-R1 (model antrenat)",
            "pasi": [
                {
                    "pas": i + 1,
                    "actiune": s,
                    "rezultat": s if any(c in s for c in "=<>≤≥±√∫²³") else "",
                }
                for i, s in enumerate(steps[:6])  # max 6 pași
            ],
            "raspuns": answer,
            "verificare": "",
            "greseli_frecvente": [],
        }

        return {
            "mode": "solve",
            "structured": structured,
            "concept": None,
            "suggestions": ["Explică mai detaliat", "Exercițiu similar", "Alt exercițiu"],
        }
    except Exception as e:
        print(f"[chat] Kaggle error: {e}")
        return None

# Add project root for AI imports (keep transformer/qwen as optional)
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Try to load the fine-tuned Qwen model
QWEN_AVAILABLE = False
try:
    from ai.finetune.inference import solve_exercise as qwen_solve, load_model as qwen_load
    # Try loading model at startup (will be cached)
    qwen_load()
    QWEN_AVAILABLE = True
    print("[chat] Qwen2.5-Math LoRA model loaded successfully!")
except Exception as e:
    print(f"[chat] Qwen model not available ({e}). Using rule-based fallback.")

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    user_id: int = 1
    exercise_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    structured: Optional[dict] = None  # Rezolvare pas cu pas
    concept: Optional[dict] = None     # Explicație concept
    latex: Optional[str] = None
    model_used: str = "math_tutor"
    suggestions: list = []


# ─── Intent detection ───

def _detect_intent(message: str) -> str:
    """Detect user intent from message."""
    t = message.lower().strip()

    # Re-explain / "why" questions about steps, formulas, methods
    if re.search(r"(?:nu\s+(?:inteleg|pricep)|explica.*pas(?:ul)?|mai\s+detaliat|repeta|de\s+ce\s+(?:ai|s-a|se|am|folosit|aplicat|ales|facut)|cum\s+ai\s+(?:ajuns|obtinut|calculat)|de\s+unde\s+(?:vine|rezulta|ai)|care\s+e\s+logica|nu\s+(?:vad|inteleg)\s+(?:cum|de\s+ce))", t):
        return "re_explain"

    # Explain wrong answer
    if re.search(r"(?:unde\s+am\s+gresit|ce\s+am\s+gresit|greseala|ce\s+e\s+gresit)", t):
        return "explain_mistake"

    # Solve an exercise
    if re.search(r"(?:rezolv[aă]|calculeaz[aă]|det(?:ermin[aă])?|deriv|integr|lim|combin|aranjam|sin|cos|tg|tan|\d+x)", t):
        return "solve"

    # Math expression present
    if re.search(r"[xX]\s*[²\^=+\-*/]|[+-]?\d+\s*[xX]|\d+\s*[+\-*/]\s*\d+", t):
        return "solve"

    # Conceptual question
    if re.search(r"(?:ce\s+(?:e|este|sunt|inseamna)|explica|cum\s+(?:se|functioneaz)|definiti|regul|formul|invata)", t):
        return "concept"

    # Similar exercise request
    if re.search(r"(?:exercitiu\s+similar|alt\s+exercitiu|mai\s+dă|genereaz)", t):
        return "similar"

    # General greeting/question
    if re.search(r"(?:salut|buna|hello|ajutor|help|ce\s+pot|cum\s+func)", t):
        return "greeting"

    # Try to detect if it's a math problem anyway
    if detect_exercise_type(t) != "necunoscut":
        return "solve"

    return "concept"


# ─── Format solution for text display ───

def _format_solution(sol: dict) -> str:
    """Format a structured solution as readable text."""
    lines = []

    if sol.get("tip") and sol["tip"] not in ("Nerecunoscut", "Eroare la rezolvare"):
        lines.append(f"📝 Tip: {sol['tip']}")
        lines.append("")

        if sol.get("ce_avem"):
            lines.append(f"📌 Ce avem: {sol['ce_avem']}")

        if sol.get("ce_aplicam"):
            lines.append(f"📐 Ce aplicăm: {sol['ce_aplicam']}")

        lines.append("")

        for pas in sol.get("pasi", []):
            lines.append(f"  Pasul {pas['pas']}: {pas['actiune']}")
            lines.append(f"  → {pas['rezultat']}")
            lines.append("")

        if sol.get("raspuns"):
            lines.append(f"✅ Răspuns: {sol['raspuns']}")

        if sol.get("verificare"):
            lines.append(f"🔍 Verificare: {sol['verificare']}")

        if sol.get("greseli_frecvente"):
            lines.append("")
            lines.append("⚠️ Greșeli frecvente:")
            for g in sol["greseli_frecvente"]:
                lines.append(f"  • {g}")
    else:
        lines.append(sol.get("raspuns", "Nu am putut rezolva exercițiul."))

    return "\n".join(lines)


def _format_concept(concept: dict) -> str:
    """Format a concept explanation as readable text."""
    lines = []
    lines.append(f"📘 {concept['concept']}")
    lines.append("")
    lines.append(f"💡 Ce este: {concept['ce_este']}")
    lines.append("")

    if concept.get("analogie"):
        lines.append(f"🎯 Analogie: {concept['analogie']}")
        lines.append("")

    if concept.get("formula"):
        lines.append(f"📐 Formula: {concept['formula']}")
        lines.append("")

    if concept.get("reguli"):
        lines.append("📋 Reguli:")
        for r in concept["reguli"]:
            lines.append(f"  • {r}")
        lines.append("")

    if concept.get("exemple"):
        lines.append("📝 Exemple:")
        for i, ex in enumerate(concept["exemple"][:3], 1):
            lines.append(f"  {i}. {ex['problema']}")
            lines.append(f"     → {ex['rezolvare']}")
            if ex.get("explicatie"):
                lines.append(f"     ({ex['explicatie']})")
        lines.append("")

    if concept.get("greseli_frecvente"):
        lines.append("⚠️ Greșeli frecvente:")
        for g in concept["greseli_frecvente"]:
            lines.append(f"  • {g}")

    return "\n".join(lines)


# ─── Suggestions based on context ───

def _get_suggestions(intent: str) -> list:
    """Generate contextual quick-reply suggestions."""
    base = []

    if intent == "solve":
        base = [
            "Explică mai detaliat",
            "Exercițiu similar",
            "Ce greșeli se fac la asta?",
        ]
    elif intent == "concept":
        base = [
            "Dă-mi un exemplu",
            "Ce formule trebuie să știu?",
            "Exercițiu practic",
        ]
    elif intent == "explain_mistake":
        base = [
            "Rezolvă pas cu pas",
            "Alt exercițiu similar",
        ]
    else:
        base = [
            "Rezolvă: 2x + 3 = 7",
            "Ce e derivata?",
            "Reguli integrale",
            "Formule trigonometrie",
            "Det [[3,1],[2,4]]",
            "C(10,3) = ?",
        ]

    return base


# ─── Save chat history ───

def _save_to_history(db, user_id: int, message: str, response: str, intent: str):
    """Save conversation turn to MongoDB."""
    db.chat_history.insert_one({
        "user_id": user_id,
        "message": message,
        "response": response[:1000],
        "intent": intent,
        "timestamp": datetime.utcnow(),
    })


def _get_recent_context(db, user_id: int, limit: int = 3) -> list:
    """Get last N conversation turns."""
    turns = list(db.chat_history.find(
        {"user_id": user_id},
        sort=[("timestamp", -1)],
        limit=limit,
    ))
    turns.reverse()
    return turns


# ─── Main chat endpoint ───

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db=Depends(get_db)):
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Mesajul nu poate fi gol.")

    # 1. If exercise_id provided → explain that specific exercise via AI
    if req.exercise_id:
        exercise = db.exercises.find_one({"_id": req.exercise_id})
        if exercise:
            question = exercise.get("question", "")
            ai = _ask_kaggle(f"Rezolvă și explică detaliat acest exercițiu: {question}")
            if ai and ai.get("structured"):
                sol = ai["structured"]
                text = _format_solution(sol)
                _save_to_history(db, req.user_id, message, text, "exercise_explain")
                return ChatResponse(
                    response=text,
                    structured=sol,
                    suggestions=ai.get("suggestions") or ["Explică pasul 1 mai detaliat", "Exercițiu similar", "Alt exercițiu"],
                    model_used="smartbac_ai",
                )
            # Fallback local
            sol = solve(question)
            if sol.get("tip") == "Nerecunoscut":
                sol = {
                    "tip": exercise.get("topic", "Exercițiu"),
                    "ce_avem": question,
                    "ce_aplicam": "Rezolvare din baza de date",
                    "pasi": [{"pas": i+1, "actiune": s.get("action", s) if isinstance(s, dict) else s, "rezultat": s.get("result", "") if isinstance(s, dict) else ""} for i, s in enumerate(exercise.get("solution_steps", []))],
                    "raspuns": exercise.get("answer", ""),
                    "verificare": exercise.get("explanation", ""),
                    "greseli_frecvente": [],
                }
            text = _format_solution(sol)
            _save_to_history(db, req.user_id, message, text, "exercise_explain")
            return ChatResponse(
                response=text,
                structured=sol,
                suggestions=["Explică pasul 1 mai detaliat", "Exercițiu similar", "Alt exercițiu"],
                model_used="math_tutor",
            )

    intent = _detect_intent(message)

    # ─── PRIMARY PATH: Kaggle SmartBAC → rule-based fallback (ZERO API) ───
    if intent not in ("explain_mistake", "greeting"):
        # Modelul propriu SmartBAC (Kaggle via ngrok)
        kaggle = _ask_kaggle(message)
        if kaggle:
            structured = kaggle["structured"]
            text = _format_solution(structured)
            _save_to_history(db, req.user_id, message, text, intent)
            return ChatResponse(
                response=text,
                structured=structured,
                suggestions=kaggle.get("suggestions") or _get_suggestions(intent),
                model_used="smartbac_kaggle",
            )
        # Dacă Kaggle nu e disponibil → rule-based (offline)

    # 2. Re-explain a step / answer "why" questions
    if intent == "re_explain":
        context = _get_recent_context(db, req.user_id)
        if context:
            # Try to re-solve the last user message for more detail
            last_user_msg = None
            for turn in reversed(context):
                if turn.get("intent") in ("solve", "exercise_explain"):
                    last_user_msg = turn.get("message", "")
                    break

            if last_user_msg:
                sol = solve(last_user_msg)
                if sol.get("tip") and sol["tip"] != "Nerecunoscut":
                    explanation_parts = []
                    if sol.get("ce_aplicam"):
                        explanation_parts.append(f"Am aplicat aceasta metoda deoarece:\n\n📐 {sol['ce_aplicam']}\n")
                    if sol.get("ce_avem"):
                        explanation_parts.append(f"Din problema avem: {sol['ce_avem']}\n")
                    for pas in sol.get("pasi", []):
                        explanation_parts.append(f"Pasul {pas['pas']}: {pas['actiune']}")
                        explanation_parts.append("  Deoarece: aplicam regula direct pe expresie")
                        explanation_parts.append(f"  Rezultat: {pas['rezultat']}\n")
                    if sol.get("raspuns"):
                        explanation_parts.append(f"✅ Raspuns final: {sol['raspuns']}")
                    text = "\n".join(explanation_parts)
                else:
                    text = (
                        "Hai sa explic mai detaliat:\n\n"
                        f"In ultimul exercitiu, am folosit formula/metoda standard pentru acel tip de problema.\n\n"
                        "Fiecare pas urmeaza logic din cel anterior - verifica pe rand fiecare calcul.\n\n"
                        "Daca vrei sa stii de ce un pas anume, spune-mi care pas (ex: 'explica pasul 2')."
                    )
            else:
                text = (
                    "Am folosit metoda standard pentru tipul de exercitiu.\n\n"
                    "Daca vrei sa intelegi un pas specific, spune-mi care te incurca "
                    "sau scrie din nou exercitiul si il explic mai detaliat!"
                )
        else:
            text = "Scrie exercitiul concret si il rezolv pas cu pas cu explicatii detaliate!"

        _save_to_history(db, req.user_id, message, text, intent)
        return ChatResponse(
            response=text,
            suggestions=["Explica pasul 1", "Explica pasul 2", "Rezolva alt exercitiu"],
            model_used="math_tutor",
        )

    # 3. Explain mistake
    if intent == "explain_mistake":
        # Check last attempt
        last_attempt = db.attempts.find_one(
            {"user_id": req.user_id},
            sort=[("created_at", -1)],
        )
        if last_attempt:
            exercise = db.exercises.find_one({"_id": last_attempt["exercise_id"]})
            if exercise:
                explanation = explain_wrong_answer(
                    exercise,
                    last_attempt.get("answer", ""),
                    exercise.get("answer", ""),
                )
                text_parts = [explanation["analiza"], "", f"🤔 {explanation['greseala_probabila']}", ""]
                if explanation.get("rezolvare") and explanation["rezolvare"].get("pasi"):
                    text_parts.append("📝 Rezolvarea corectă:")
                    text_parts.append(_format_solution(explanation["rezolvare"]))
                text_parts.append("")
                text_parts.append(f"💡 {explanation['sfat']}")
                text = "\n".join(text_parts)

                _save_to_history(db, req.user_id, message, text, intent)
                return ChatResponse(
                    response=text,
                    structured=explanation.get("rezolvare"),
                    suggestions=["Exercițiu similar", "Mai explică o dată", "Alt exercițiu"],
                    model_used="math_tutor",
                )

        text = "Nu am găsit un exercițiu recent. Scrie exercițiul și răspunsul tău, și îți explic unde ai greșit!"
        _save_to_history(db, req.user_id, message, text, intent)
        return ChatResponse(response=text, suggestions=_get_suggestions("greeting"), model_used="math_tutor")

    # 4. Solve a math problem
    if intent == "solve":
        # Try Qwen fine-tuned model first
        if QWEN_AVAILABLE:
            try:
                qwen_result = qwen_solve(message)
                if qwen_result.get("answer") or qwen_result.get("full_response"):
                    # Convert Qwen output to structured format
                    steps_list = qwen_result.get("steps", [])
                    sol = {
                        "tip": detect_exercise_type(message).capitalize(),
                        "ce_avem": message,
                        "ce_aplicam": "Rezolvare cu model AI antrenat",
                        "pasi": [
                            {"pas": i + 1, "actiune": s, "rezultat": ""}
                            for i, s in enumerate(steps_list)
                        ],
                        "raspuns": qwen_result.get("answer", ""),
                        "verificare": "",
                        "greseli_frecvente": [],
                    }
                    text = _format_solution(sol)
                    _save_to_history(db, req.user_id, message, text, intent)
                    return ChatResponse(
                        response=text,
                        structured=sol,
                        suggestions=_get_suggestions(intent),
                        model_used="qwen_lora",
                    )
            except Exception as e:
                print(f"[chat] Qwen inference error: {e}")

        # Fallback to rule-based solver
        sol = solve(message)

        # Dacă rule-based nu poate → Kaggle
        if sol.get("tip") in ("Nerecunoscut", "Eroare la rezolvare"):
            kaggle2 = _ask_kaggle(message)
            if kaggle2:
                structured = kaggle2["structured"]
                text = _format_solution(structured)
                _save_to_history(db, req.user_id, message, text, intent)
                return ChatResponse(
                    response=text,
                    structured=structured,
                    suggestions=kaggle2.get("suggestions") or _get_suggestions(intent),
                    model_used="smartbac_kaggle",
                )

        text = _format_solution(sol)
        _save_to_history(db, req.user_id, message, text, intent)

        return ChatResponse(
            response=text,
            structured=sol if sol.get("tip") != "Nerecunoscut" else None,
            suggestions=_get_suggestions(intent),
            model_used="math_tutor",
        )

    # 5. Conceptual question
    if intent in ("concept", "similar"):
        concept = find_concept(message)
        if concept:
            text = _format_concept(concept)
            _save_to_history(db, req.user_id, message, text, intent)
            return ChatResponse(
                response=text,
                concept=concept,
                suggestions=_get_suggestions(intent),
                model_used="math_tutor",
            )

    # 6. Greeting
    if intent == "greeting":
        text = (
            "Salut! 👋 Sunt tutorul tău de matematică pentru BAC.\n\n"
            "Pot să te ajut cu:\n"
            "📝 Rezolvarea exercițiilor pas cu pas\n"
            "📘 Explicații concepte (derivate, integrale, limite...)\n"
            "🔍 Analiza greșelilor tale\n"
            "📐 Formule și reguli\n\n"
            "Scrie un exercițiu sau o întrebare!"
        )
        _save_to_history(db, req.user_id, message, text, intent)
        return ChatResponse(
            response=text,
            suggestions=_get_suggestions("greeting"),
            model_used="math_tutor",
        )

    # Last resort: try to solve it as math anyway
    sol = solve(message)
    if sol.get("tip") and sol["tip"] not in ("Nerecunoscut", "Eroare la rezolvare"):
        text = _format_solution(sol)
        _save_to_history(db, req.user_id, message, text, "solve_fallback")
        return ChatResponse(
            response=text,
            structured=sol,
            suggestions=_get_suggestions("solve"),
            model_used="math_tutor",
        )

    # Ultima încercare — trimite la Kaggle direct
    kaggle_last = _ask_kaggle(message)
    if kaggle_last:
        structured = kaggle_last["structured"]
        text_last = _format_solution(structured)
        _save_to_history(db, req.user_id, message, text_last, "kaggle_fallback")
        return ChatResponse(
            response=text_last,
            structured=structured,
            suggestions=kaggle_last.get("suggestions") or _get_suggestions("solve"),
            model_used="smartbac_kaggle",
        )

    text = (
        "Nu am reușit să rezolv acest exercițiu offline.\n\n"
        "Încearcă să reformulezi, de exemplu:\n"
        "  'Rezolvă ecuația: 3x + 5 = 11'\n"
        "  'Calculează derivata: f(x) = x² + 3x'\n"
        "  'Calculează integrala din 2x'\n"
        "  'Ce este derivata?'\n\n"
        "Sau alege din sugestiile de mai jos!"
    )
    _save_to_history(db, req.user_id, message, text, "fallback")
    return ChatResponse(
        response=text,
        suggestions=_get_suggestions("greeting"),
        model_used="math_tutor",
    )


# ─── Knowledge base endpoints (backward compat for admin) ───

@router.get("/chat/knowledge")
def get_knowledge(db=Depends(get_db)):
    topics = get_all_topics()
    knowledge = list(db.chat_knowledge.find({}, {"_id": 0}))
    return {"topics": topics, "knowledge": knowledge}


@router.post("/chat/add-knowledge")
def add_knowledge(data: dict, db=Depends(get_db)):
    db.chat_knowledge.insert_one({
        "topic": data.get("topic", ""),
        "keywords": data.get("keywords", []),
        "response": data.get("response", ""),
        "created_at": datetime.utcnow(),
    })
    return {"success": True}
