"""Core explainable analysis engine for PathForge AI."""
import re
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data import SKILLS, ROLES, RESOURCE_GUIDE

def _normalise(text: str) -> str:
    text = (text or "").lower()
    text = text.replace("c++", " cplusplus ").replace("c#", " csharp ")
    text = re.sub(r"[^a-z0-9+#.]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_skills(text: str, default_level: float = 55.0) -> dict:
    """Extract known skills using synonym-aware boundary matching."""
    source = _normalise(text)
    found = {}
    for canonical, synonyms in SKILLS.items():
        terms = [canonical] + synonyms
        for term in terms:
            term_n = _normalise(term)
            if not term_n:
                continue
            # Special handling for short aliases and punctuation-heavy languages.
            pattern = r"(?<![a-z0-9])" + re.escape(term_n.strip()) + r"(?![a-z0-9])"
            if re.search(pattern, source):
                found[canonical] = float(default_level)
                break
    return found

def _profile_vector(profile: dict, skills: list) -> np.ndarray:
    return np.array([float(np.clip(profile.get(s, 0), 0, 100)) for s in skills], dtype=float)

def match_score(profile: dict, role_name: str) -> float:
    """Weighted capped match score from 0 to 100."""
    if role_name not in ROLES:
        raise ValueError(f"Unknown role: {role_name}")
    req = ROLES[role_name]
    denom = sum(v["weight"] * v["target"] for v in req.values())
    if denom <= 0:
        return 0.0
    earned = sum(v["weight"] * min(float(np.clip(profile.get(s, 0), 0, 100)), v["target"])
                 for s, v in req.items())
    return round(100.0 * earned / denom, 2)

def cosine_role_similarity(profile: dict, role_name: str) -> float:
    req = ROLES[role_name]
    skills = sorted(set(profile) | set(req))
    student = _profile_vector(profile, skills)
    target = np.array([req.get(s, {}).get("target", 0) for s in skills], dtype=float)
    if not np.any(student) or not np.any(target):
        return 0.0
    return round(float(cosine_similarity([student], [target])[0, 0] * 100), 2)

def analyse(profile: dict, target_role: str) -> dict:
    """Return score, gaps, role ranking, readiness heuristic and a four-week plan."""
    if target_role not in ROLES:
        raise ValueError(f"Unknown role: {target_role}")
    clean = {s: float(np.clip(v, 0, 100)) for s, v in profile.items() if s in SKILLS}
    req = ROLES[target_role]
    gaps = []
    for skill, spec in req.items():
        current = clean.get(skill, 0.0)
        shortfall = max(0.0, spec["target"] - current)
        if shortfall > 0:
            gaps.append({
                "skill": skill, "current": round(current, 1),
                "target": spec["target"], "shortfall": round(shortfall, 1),
                "importance": spec["weight"],
                "priority": round(spec["weight"] * shortfall, 2)
            })
    gaps.sort(key=lambda x: x["priority"], reverse=True)
    score = match_score(clean, target_role)
    readiness = "Ready" if score >= 80 else "Nearly Ready" if score >= 60 else "Developing"

    ranking = []
    for role in ROLES:
        ranking.append({"role": role, "match_score": match_score(clean, role),
                        "cosine_similarity": cosine_role_similarity(clean, role)})
    ranking.sort(key=lambda x: x["match_score"], reverse=True)

    plan = []
    selected = gaps[:8]
    if not selected:
        plan.append({"week": 1, "focus": "Consolidation", "activities": [
            "Build a portfolio project using the target role's core skills",
            "Review fundamentals and document evidence of proficiency"
        ]})
    else:
        for week in range(1, 5):
            batch = selected[(week-1)*2:week*2]
            if not batch:
                batch = selected[-2:]
            activities = []
            for item in batch:
                course, project = RESOURCE_GUIDE.get(
                    item["skill"], (f"Study {item['skill']} fundamentals",
                                    f"Build a small project demonstrating {item['skill']}"))
                activities.extend([course, project])
            plan.append({"week": week, "focus": ", ".join(x["skill"] for x in batch),
                         "activities": activities})
    return {"target_role": target_role, "match_score": score, "readiness": readiness,
            "cosine_similarity": cosine_role_similarity(clean, target_role),
            "gaps": gaps, "role_ranking": ranking, "learning_plan": plan,
            "profile": clean}

def rank_resources(gap_skills: list, resources: list) -> list:
    """Small content-based TF-IDF ranking helper."""
    if not resources:
        return []
    corpus = [str(r.get("description", "")) for r in resources]
    query = " ".join(gap_skills)
    if not query.strip():
        return resources
    vec = TfidfVectorizer(stop_words="english")
    matrix = vec.fit_transform(corpus + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    return [resources[i] for i in np.argsort(scores)[::-1]]
