"""Reproducible Decision Tree and K-Means demonstrations on synthetic data."""
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, silhouette_score
from data import SKILLS, ROLES
from engine import match_score

RANDOM_STATE = 42
LABELS = {0: "Developing", 1: "Nearly Ready", 2: "Ready"}

def _role_features(profile, role_name, skills):
    req = ROLES[role_name]
    student = [float(profile.get(s, 0)) / 100.0 for s in skills]
    target = [float(req.get(s, {}).get("target", 0)) / 100.0 for s in skills]
    return student + target

def make_synthetic_profiles(n=1600, seed=RANDOM_STATE):
    """Create balanced synthetic role/profile pairs for a controlled classifier demo."""
    rng = np.random.default_rng(seed)
    skills = list(SKILLS)
    role_names = list(ROLES)
    X, y, raw_profiles = [], [], []
    # Deliberately balance the three score bands so the model is not dominated
    # by one synthetic class. This is a teaching dataset, not labour-market data.
    bands = [(0, .30, .58), (1, .60, .78), (2, .82, 1.28)]
    for i in range(n):
        role = role_names[int(rng.integers(0, len(role_names)))]
        req = ROLES[role]
        label, low, high = bands[i % len(bands)]
        factor = float(rng.uniform(low, high))
        profile = {}
        for skill in skills:
            target = req.get(skill, {}).get("target", 0)
            if target:
                value = target * factor + rng.normal(0, 4)
            else:
                value = rng.uniform(0, 12)
            profile[skill] = float(np.clip(value, 0, 100))
        # Derive the class from the actual weighted score to keep labels consistent.
        score = match_score(profile, role)
        actual_label = 2 if score >= 80 else 1 if score >= 60 else 0
        X.append(_role_features(profile, role, skills))
        y.append(actual_label)
        raw_profiles.append((profile, role))
    return np.asarray(X), np.asarray(y), skills, raw_profiles

def train_readiness_model():
    X, y, skills, _ = make_synthetic_profiles()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.25, random_state=RANDOM_STATE, stratify=y)
    model = DecisionTreeClassifier(max_depth=7, min_samples_leaf=6,
                                    class_weight="balanced", random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return model, {"accuracy": accuracy_score(y_test, pred),
                   "report": classification_report(y_test, pred, zero_division=0),
                   "skills": skills, "test_size": len(y_test)}

def predict_readiness(model, profile, role_name, skills=None):
    skills = skills or list(SKILLS)
    features = np.asarray([_role_features(profile, role_name, skills)])
    return LABELS[int(model.predict(features)[0])]

def cluster_profiles(n_clusters=5):
    X, _, skills, _ = make_synthetic_profiles(n=500)
    # Cluster only student skill levels, not role-target metadata.
    X_students = X[:, :len(skills)]
    model = KMeans(n_clusters=n_clusters, n_init=10, random_state=RANDOM_STATE)
    labels = model.fit_predict(X_students)
    silhouette = silhouette_score(X_students, labels) if len(set(labels)) > 1 else float("nan")
    return model, {"silhouette": silhouette, "labels": labels, "skills": skills}
