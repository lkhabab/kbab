# app/services/rules_engine.py
import os, re, json
from collections import defaultdict
from typing import Dict

HERE = os.path.dirname(__file__)

# --- تطبيع عربي بسيط ---
AR_DIAC    = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
AR_TATWEEL = re.compile(r'[\u0640]')
AR_PUNC    = re.compile(r'[^\w\s\u0600-\u06FF]')

def norm_ar(t: str) -> str:
    t = t.strip().lower()
    t = AR_DIAC.sub('', t)
    t = AR_TATWEEL.sub('', t)
    t = t.replace('أ','ا').replace('إ','ا').replace('آ','ا')
    t = t.replace('ى','ي').replace('ئ','ي').replace('ؤ','و')
    t = AR_PUNC.sub(' ', t)
    return re.sub(r'\s+',' ', t)

# --- التقاط كيانات أساسية ---
RE_CROP  = re.compile(r'(قمح|حنطة|ذرة|ذره|سورغم|sorghum|طماطم|طماط|بندورة)')
RE_AREA  = re.compile(r'(\d+(?:\.\d+)?)\s*(م2|م|فدان|هكتار)')
RE_AGE   = re.compile(r'(\d+)\s*(يوم|اسبوع|شهر|ايام|اسابيع|اشهر)')
RE_SYMPT = re.compile(r'(بقع|اصفرار|ذبول|تعفن|حروق|ثقوب|صدأ|لفحة)')

def extract_entities(text: str) -> Dict[str, str]:
    out = {}
    m = RE_CROP.search(text);  out['crop']    = m.group(1) if m else None
    m = RE_AREA.search(text);  out['area']    = m.group(1) if m else None
    m = RE_AGE.search(text);   out['age']     = m.group(1) if m else None
    m = RE_SYMPT.search(text); out['symptom'] = m.group(1) if m else None
    return out

class RuleEngine:
    def __init__(self, rules_path=None):
        path = rules_path or os.path.join(os.path.dirname(HERE), "rules", "ar_rules.json")
        self._load(path)

    def _load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        self.threshold = float(cfg.get("threshold", 0.5))
        self.intents = cfg["intents"]
        self.synonyms = cfg.get("synonyms", {})
        # تجهيز قاموس مرادفات مطبّع
        self.lex = defaultdict(set)
        for base, syns in self.synonyms.items():
            for s in [base] + syns:
                self.lex[base].add(norm_ar(s))

        # جهّز الـregex لكل intent عشان الأداء
        for it in self.intents:
            it["_re"] = [re.compile(p) for p in it.get("patterns", [])]
            it["_utt"] = [norm_ar(u) for u in it.get("utterances", [])]

    def score_intent(self, text, it) -> float:
        score = 0.0
        # كلمات مفتاحية
        for u in it["_utt"]:
            if u and u in text:
                score += 0.3
        # أنماط
        for r in it["_re"]:
            if r.search(text):
                score += 0.5
        # تعزيز بسيط لو لقينا أي مرادف محصول
        if any(f in text for forms in self.lex.values() for f in forms):
            score += 0.1
        return min(score, 1.0)

    def infer(self, user_text: str, state: Dict):
        raw  = user_text or ""
        text = norm_ar(raw)
        ents = extract_entities(text)

        # إدارة الSlots
        state.setdefault("slots", {})
        state.setdefault("pending", [])

        # لو فيه سؤال سابق يطلب قيمة Slot
        if state["pending"]:
            slot = state["pending"].pop(0)
            state["slots"][slot] = raw
            if state["pending"]:
                return {"reply": f"تمام. أرسل {state['pending'][0]} كمان.", "state": state}

        # احسب سكور النوايا
        best = None
        best_s = -1
        for it in self.intents:
            s = self.score_intent(text, it)
            if s > best_s:
                best, best_s = it, s

        if best_s < self.threshold:
            return {"reply": "ما فهمت سؤالك. اذكر المحصول + المشكلة بإيجاز.", "state": state, "score": best_s}

        # حدّث الSlots من الكيانات
        for k, v in ents.items():
            if v: state["slots"][k] = v

        required = best.get("entities", [])
        missing = [k for k in required if not state["slots"].get(k)]
        if missing:
            state["pending"] = missing.copy()
            return {"reply": f"تمام. أرسل {missing[0]} لو سمحت.", "state": state, "intent": best["name"], "score": best_s}

        # صياغة الرد
        reply = best.get("response", "")
        if state["slots"].get("crop"):
            reply = f"({state['slots']['crop']}): " + reply

        state["last_intent"] = best["name"]
        return {"reply": reply, "state": state, "intent": best["name"], "score": best_s}
