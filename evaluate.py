"""Run reproducible synthetic-data evaluation; not a real-world hiring benchmark."""
from ml_models import train_readiness_model, cluster_profiles

def main():
    _, metrics = train_readiness_model()
    _, clusters = cluster_profiles()
    print("PATHFORGE AI — SYNTHETIC EVALUATION")
    print(f"Decision Tree accuracy: {metrics['accuracy']:.3f}")
    print(f"Held-out synthetic samples: {metrics['test_size']}")
    print(metrics["report"])
    print(f"K-Means silhouette score: {clusters['silhouette']:.3f}")
    print("\nCaution: these are synthetic-data metrics, not real-world career or hiring accuracy.")

if __name__ == "__main__":
    main()
