import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples

# ==========================================================
# PREPROCESSING
# ==========================================================

FEATURES = [
    "voltage",
    "current",
    "power",
    "frequency",
    "power_factor"
]

# ==========================================================
# RUN KMEANS
# ==========================================================

def run_kmeans(df, n_clusters=3, random_state=42):

    X = df[FEATURES].copy()

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    result = df.copy()

    result["cluster"] = labels

    return {
        "result": result,
        "model": model,
        "scaled": X_scaled,
        "scaler": scaler,
        "labels": labels
    }

# ==========================================================
# CLUSTER STATISTICS
# ==========================================================

def cluster_statistics(result):

    return (
        result
        .groupby("cluster")[FEATURES]
        .mean()
        .round(2)
    )

# ==========================================================
# CENTROID
# ==========================================================

def cluster_centroid(model, scaler):

    centroid = pd.DataFrame(
        scaler.inverse_transform(
            model.cluster_centers_
        ),
        columns=FEATURES
    ).round(2)

    centroid.index = [
        f"Cluster {i}"
        for i in range(len(centroid))
    ]

    return centroid

# ==========================================================
# PCA
# ==========================================================

def cluster_pca(X_scaled, labels):

    pca = PCA(n_components=2)

    result = pca.fit_transform(X_scaled)

    return pd.DataFrame({
        "PC1": result[:,0],
        "PC2": result[:,1],
        "Cluster": labels.astype(str)
    })

# ==========================================================
# DISTRIBUTION
# ==========================================================

def cluster_distribution(result):

    distribution = (
        result["cluster"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    distribution.columns = [
        "Cluster",
        "Samples"
    ]

    return distribution

# ==========================================================
# MODEL INFORMATION
# ==========================================================

def model_information(
    model,
    result,
    n_clusters,
    random_state
):

    return pd.DataFrame({
        "Parameter":[
            "Algorithm",
            "Clusters",
            "Random State",
            "Samples",
            "Features",
            "Inertia"
        ],
        "Value":[
            "K-Means",
            n_clusters,
            random_state,
            len(result),
            len(FEATURES),
            round(model.inertia_,2)
        ]
    })

# ==========================================================
# ELBOW METHOD
# ==========================================================

def compute_elbow(df, max_k=10, random_state=42):

    X = df[FEATURES].copy()

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    k_values = list(range(2, max_k + 1))

    inertia = []

    for k in k_values:

        model = KMeans(
            n_clusters=k,
            random_state=random_state,
            n_init=10
        )

        model.fit(X_scaled)

        inertia.append(model.inertia_)

    elbow_df = pd.DataFrame({
        "K": k_values,
        "WCSS": inertia
    })

    diff1 = pd.Series(inertia).diff().abs()
    diff2 = diff1.diff().abs()

    if len(diff2.dropna()) > 0:
        recommended_k = diff2.idxmax() + 2
    else:
        recommended_k = 3

    return {
        "elbow_df": elbow_df,
        "recommended_k": recommended_k
    }

# ==========================================================
# SILHOUETTE SCORE
# ==========================================================

def compute_silhouette(df, n_clusters=3, random_state=42):

    X = df[FEATURES].copy()

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    avg_score = silhouette_score(X_scaled, labels)

    sample_score = silhouette_samples(X_scaled, labels)

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

    return {
        "result": result,
        "avg_score": avg_score,
        "cluster_score": cluster_score
    }

# ==========================================================
# SILHOUETTE INTERPRETATION
# ==========================================================

def silhouette_quality(avg_score):

    if avg_score >= 0.70:
        return (
            "Excellent ⭐⭐⭐⭐⭐",
            "The clusters are well separated and highly compact. "
            "This indicates excellent clustering quality."
        )

    if avg_score >= 0.50:
        return (
            "Good ⭐⭐⭐⭐",
            "The clusters are reasonably separated and compact. "
            "This clustering result is considered good."
        )

    if avg_score >= 0.25:
        return (
            "Fair ⭐⭐⭐",
            "The clusters overlap slightly. "
            "The clustering is acceptable but could be improved."
        )

    return (
        "Poor ⭐",
        "The clusters overlap heavily. "
        "The selected number of clusters is not recommended."
    )