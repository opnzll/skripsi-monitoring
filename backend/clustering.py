"""
Machine Learning utilities for Smart Energy Monitoring.

This module provides:

- K-Means Clustering
- PCA Projection
- Elbow Method
- Silhouette Score
- Cluster Statistics
"""

from __future__ import annotations

import logging

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    silhouette_samples,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# CONSTANTS
# ==========================================================

FEATURES = [
    "voltage",
    "current",
    "power",
    "frequency",
    "power_factor",
]

DEFAULT_RANDOM_STATE = 42

DEFAULT_N_INIT = 10

DEFAULT_CLUSTER = 3

PCA_COMPONENTS = 2

# ==========================================================
# VALIDATION
# ==========================================================

def _validate_dataframe(df: pd.DataFrame) -> None:
    """
    Validate clustering dataset.
    """

    if df.empty:
        raise ValueError("Dataset is empty.")

    missing = [
        column
        for column in FEATURES
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

# ==========================================================
# PREPROCESSING
# ==========================================================

def _prepare_dataset(
    df: pd.DataFrame,
):
    """
    Extract feature matrix and apply StandardScaler.
    """

    _validate_dataframe(df)

    X = df.loc[:, FEATURES].copy()

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    return X, X_scaled, scaler

# ==========================================================
# MODEL
# ==========================================================

def _create_model(
    n_clusters: int,
    random_state: int,
) -> KMeans:
    """
    Create K-Means model.
    """

    return KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=DEFAULT_N_INIT,
    )

# ==========================================================
# RUN K-MEANS
# ==========================================================

def run_kmeans(
    df: pd.DataFrame,
    n_clusters: int = DEFAULT_CLUSTER,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> dict:
    """
    Perform K-Means clustering.
    """

    try:

        _, X_scaled, scaler = _prepare_dataset(df)

        model = _create_model(
            n_clusters,
            random_state,
        )

        labels = model.fit_predict(
            X_scaled,
        )

        result = df.copy()

        result["cluster"] = labels

        logger.info(
            "K-Means completed (%s clusters).",
            n_clusters,
        )

        return {

            "result": result,

            "model": model,

            "scaled": X_scaled,

            "scaler": scaler,

            "labels": labels,

        }

    except Exception:

        logger.exception(
            "Failed running K-Means."
        )

        raise

# ==========================================================
# CLUSTER STATISTICS
# ==========================================================

def cluster_statistics(
    result: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate mean value of each feature for every cluster.
    """

    try:

        statistics = (
            result
            .groupby("cluster")[FEATURES]
            .mean()
            .round(2)
        )

        return statistics

    except Exception:

        logger.exception(
            "Failed calculating cluster statistics."
        )

        raise


# ==========================================================
# CLUSTER CENTROID
# ==========================================================

def cluster_centroid(
    model: KMeans,
    scaler: StandardScaler,
) -> pd.DataFrame:
    """
    Transform centroid back to original feature scale.
    """

    try:

        centroid = pd.DataFrame(

            scaler.inverse_transform(
                model.cluster_centers_
            ),

            columns=FEATURES,

        ).round(2)

        centroid.index = [

            f"Cluster {i}"

            for i in range(
                len(centroid)
            )

        ]

        return centroid

    except Exception:

        logger.exception(
            "Failed calculating centroid."
        )

        raise


# ==========================================================
# PCA VISUALIZATION
# ==========================================================

def cluster_pca(
    X_scaled,
    labels,
) -> pd.DataFrame:
    """
    Reduce clustered data into 2 principal components.
    """

    try:

        pca = PCA(
            n_components=PCA_COMPONENTS,
        )

        projection = pca.fit_transform(
            X_scaled
        )

        return pd.DataFrame(

            {

                "PC1": projection[:, 0],

                "PC2": projection[:, 1],

                "Cluster": labels.astype(str),

            }

        )

    except Exception:

        logger.exception(
            "Failed performing PCA."
        )

        raise


# ==========================================================
# CLUSTER DISTRIBUTION
# ==========================================================

def cluster_distribution(
    result: pd.DataFrame,
) -> pd.DataFrame:
    """
    Count number of samples in every cluster.
    """

    try:

        distribution = (

            result["cluster"]

            .value_counts()

            .sort_index()

            .rename_axis("Cluster")

            .reset_index(name="Samples")

        )

        return distribution

    except Exception:

        logger.exception(
            "Failed calculating distribution."
        )

        raise


# ==========================================================
# MODEL INFORMATION
# ==========================================================

def model_information(
    model: KMeans,
    result: pd.DataFrame,
    n_clusters: int,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> pd.DataFrame:
    """
    Return model metadata.
    """

    try:

        return pd.DataFrame(

            {

                "Parameter": [

                    "Algorithm",

                    "Clusters",

                    "Random State",

                    "Samples",

                    "Features",

                    "Inertia",

                ],

                "Value": [

                    "K-Means",

                    n_clusters,

                    random_state,

                    len(result),

                    len(FEATURES),

                    round(
                        model.inertia_,
                        2,
                    ),

                ],

            }

        )

    except Exception:

        logger.exception(
            "Failed creating model information."
        )

        raise

# ==========================================================
# ELBOW METHOD
# ==========================================================

def compute_elbow(
    df: pd.DataFrame,
    max_k: int = 10,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> dict:
    """
    Compute Elbow Method for determining
    the optimal number of clusters.

    Returns
    -------
    dict
        {
            "elbow_df": pd.DataFrame,
            "recommended_k": int
        }
    """

    try:

        _, X_scaled, _ = _prepare_dataset(df)

        inertia = []
        k_values = list(range(2, max_k + 1))

        for k in k_values:

            model = _create_model(
                n_clusters=k,
                random_state=random_state,
            )

            model.fit(X_scaled)

            inertia.append(model.inertia_)

        elbow_df = pd.DataFrame(
            {
                "K": k_values,
                "WCSS": inertia,
            }
        )

        # Maximum curvature approximation
        diff1 = pd.Series(inertia).diff().abs()
        diff2 = diff1.diff().abs()

        recommended_k = (
            diff2.idxmax() + 2
            if not diff2.dropna().empty
            else DEFAULT_CLUSTER
        )

        logger.info(
            "Elbow Method completed."
        )

        return {
            "elbow_df": elbow_df,
            "recommended_k": recommended_k,
        }

    except Exception:

        logger.exception(
            "Failed computing Elbow Method."
        )

        raise


# ==========================================================
# SILHOUETTE SCORE
# ==========================================================

def compute_silhouette(
    df: pd.DataFrame,
    n_clusters: int = DEFAULT_CLUSTER,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> dict:
    """
    Compute Silhouette Score for K-Means clustering.
    """

    try:

        _, X_scaled, _ = _prepare_dataset(df)

        model = _create_model(
            n_clusters=n_clusters,
            random_state=random_state,
        )

        labels = model.fit_predict(
            X_scaled
        )

        avg_score = silhouette_score(
            X_scaled,
            labels,
        )

        sample_score = silhouette_samples(
            X_scaled,
            labels,
        )

        result = df.copy()

        result["cluster"] = labels

        result["silhouette"] = sample_score

        cluster_score = (
            result
            .groupby("cluster")["silhouette"]
            .mean()
            .round(4)
            .reset_index()
        )

        logger.info(
            "Silhouette Score computed."
        )

        return {

            "result": result,

            "avg_score": avg_score,

            "cluster_score": cluster_score,

        }

    except Exception:

        logger.exception(
            "Failed computing Silhouette Score."
        )

        raise


# ==========================================================
# SILHOUETTE QUALITY
# ==========================================================

def silhouette_quality(
    avg_score: float,
) -> tuple[str, str]:
    """
    Interpret Silhouette Score.
    """

    if avg_score >= 0.70:

        return (

            "Excellent ⭐⭐⭐⭐⭐",

            (
                "The clusters are well separated "
                "and highly compact."
            ),

        )

    elif avg_score >= 0.50:

        return (

            "Good ⭐⭐⭐⭐",

            (
                "Clusters are reasonably separated "
                "with good compactness."
            ),

        )

    elif avg_score >= 0.25:

        return (

            "Fair ⭐⭐⭐",

            (
                "Clusters overlap slightly. "
                "The result is acceptable."
            ),

        )

    else:

        return (

            "Poor ⭐",

            (
                "Clusters overlap significantly. "
                "Consider using another value of K."
            ),

        )