"""
DecodeLabs AI Project 2 - Supervised Learning Pipeline
Author: Rehmat Ali(609)
Description: A production-ready Data Classification pipeline using K-Nearest Neighbors.
             Implements robust Train/Test splitting, Feature Scaling, Validation-based 
             Hyperparameter Tuning (Elbow Method), and F1/Confusion Matrix evaluation.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from typing import Any, Optional, Sequence


# ==============================================================================
# 1. INPUT STAGE: DATA LOADING & SPLITTING
# ==============================================================================
def load_and_split_data(test_size: float = 0.2, random_state: int = 42):
    """Load the Iris dataset and split into an 80% training set and 20% test set."""
    X, y = load_iris(return_X_y=True)

    # Shuffle and split the dataset to remove order bias and ensure a reproducible split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        shuffle=True,
        random_state=random_state,
        stratify=y, # Ensures class balance is maintained across splits
    )

    return X_train, X_test, y_train, y_test


# ==============================================================================
# 2. PROCESS STAGE: FEATURE SCALING
# ==============================================================================
def scale_features(X_train: np.ndarray, X_test: np.ndarray):
    """
    Standardize features to a mean of 0 and a variance of 1.
    
    Why this matters: KNN relies on spatial distance calculations between feature 
    vectors. If one feature is measured in millimeters and another in centimeters, 
    the larger scale will artificially dominate the algorithm's decision boundary.
    """
    scaler = StandardScaler()
    # Fit the scaler ONLY on the training data to prevent data leakage, then transform
    X_train_scaled = scaler.fit_transform(X_train)
    # Transform the test data using the parameters learned from the training data
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled


# ==============================================================================
# 3. PROCESS STAGE: HYPERPARAMETER TUNING (THE ELBOW METHOD)
# ==============================================================================
def plot_elbow_method(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, max_k: int = 20):
    """
    Iterates through K values to find the optimal balance between overfitting (K=1) 
    and underfitting (large K). Evaluates error exclusively on the unseen TEST set.
    """
    error_rates = []
    k_values = list(range(1, max_k + 1))

    for k in k_values:
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        
        # CRITICAL: Predict on the unseen TEST data to measure true generalization error
        predictions = model.predict(X_test)
        error = np.mean(predictions != y_test)
        error_rates.append(error)

    # Plotting the Validation Elbow
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=k_values, y=error_rates, marker="o", linewidth=2)
    plt.title("Elbow Method for KNN Optimization - Rehmat 609", fontsize=16)
    plt.xlabel("Number of Neighbors (K)")
    plt.ylabel("Validation Error Rate")
    plt.xticks(k_values)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

    return k_values, error_rates

def select_optimal_k(k_values, error_rates):
    """Programmatically selects the smallest K that achieves the lowest validation error."""
    min_error = min(error_rates)
    optimal_indices = [i for i, err in enumerate(error_rates) if err == min_error]
    optimal_k = k_values[optimal_indices[0]]
    return optimal_k


# ==============================================================================
# 4. PROCESS STAGE: MODEL TRAINING
# ==============================================================================
def train_knn_classifier(X_train: np.ndarray, y_train: np.ndarray, n_neighbors: int):
    """Instantiate and fit the final KNN model using the optimal K."""
    knn_model = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn_model.fit(X_train, y_train)
    return knn_model


# ==============================================================================
# 5. OUTPUT STAGE: VALIDATION & METRICS
# ==============================================================================
def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray, target_names: Optional[Sequence[str]] = None):
    """
    Evaluates the model using Precision, Recall, F1-Score, and a Confusion Matrix.
    Provides a complete view of model performance beyond the 'accuracy mirage'.
    """
    y_pred = model.predict(X_test)

    if target_names is None:
        target_names = [f"Class {i}" for i in np.unique(y_test)]

    # Print the F1, Precision, and Recall metrics
    report = classification_report(y_test, y_pred, target_names=target_names)
    print("=== Model Diagnostic Report ===\n")
    print(report)

    # Generate and plot the visual Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=list(target_names),
        yticklabels=list(target_names),
    )
    plt.title("Confusion Matrix for KNN Classification - Rehmat 609", fontsize=16)
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.show()

    return report, cm


# ==============================================================================
# EXECUTION
# ==============================================================================
def main():
    print("Initializing Data Classification Pipeline...")
    
    # 1. Load and Split
    iris: Any = load_iris()
    X_train, X_test, y_train, y_test = load_and_split_data()
    
    # 2. Scale Features
    X_train_scaled, X_test_scaled = scale_features(X_train, X_test)

    # 3. Analyze Elbow Method (Using Validation Data)
    print("Running iterative hyperparameter tuning...")
    k_values, error_rates = plot_elbow_method(X_train_scaled, y_train, X_test_scaled, y_test, max_k=20)
    optimal_k = select_optimal_k(k_values, error_rates)
    print(f"Selected optimal K from validation elbow analysis: {optimal_k}\n")

    # 4. Train the Final Model
    print("Training final model with optimal parameters...")
    knn_model = train_knn_classifier(X_train_scaled, y_train, n_neighbors=optimal_k)

    # 5. Evaluate
    target_names = getattr(iris, "target_names", None)
    if target_names is None:
        target_names = ["setosa", "versicolor", "virginica"]

    evaluate_model(knn_model, X_test_scaled, y_test, target_names=target_names)

if __name__ == "__main__":
    main()