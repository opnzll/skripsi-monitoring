"""
Clustering Analysis Page

This page performs K-Means clustering analysis,
Elbow Method evaluation, and Silhouette Score
visualization for Smart Energy Monitoring.
"""

from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from backend.clustering import (
    FEATURES,
    cluster_centroid,
    cluster_distribution,
    cluster_pca,
    cluster_statistics,
    compute_elbow,
    compute_silhouette,
    run_kmeans,
    silhouette_quality,
)

from backend.services import get_clustering_data

from components.cards import metric_card
from components.footer import render_footer
from components.header import render_header
from components.panel import panel
from components.sidebar import render_sidebar

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Clustering Analysis",
    page_icon="🧠",
    layout="wide",
)

# ==========================================================
# CONSTANTS
# ==========================================================

MAX_RECORDS = 2500

DEFAULT_K = 3

MAX_K = 10

CACHE_DATA_TTL = 60

CACHE_MODEL_TTL = 300

PCA_HEIGHT = 560

BAR_HEIGHT = 340

ELBOW_HEIGHT = 440

SILHOUETTE_HEIGHT = 380

# ==========================================================
# AUTHENTICATION
# ==========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/🔐_Login.py")

# ==========================================================
# LOAD CSS
# ==========================================================

css_path = Path("assets/style.css")

if css_path.exists():

    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

# ==========================================================
# RENDER LAYOUT
# ==========================================================

render_sidebar()

render_header()

# ==========================================================
# CACHE
# ==========================================================

@st.cache_data(ttl=CACHE_DATA_TTL, show_spinner=False)
def load_dataset():
    return get_clustering_data(MAX_RECORDS)


@st.cache_data(ttl=CACHE_MODEL_TTL, show_spinner=False)
def load_kmeans(dataset, k: int):
    return run_kmeans(dataset, n_clusters=k)


@st.cache_data(ttl=CACHE_MODEL_TTL, show_spinner=False)
def load_elbow(dataset):
    return compute_elbow(dataset, max_k=MAX_K)


@st.cache_data(ttl=CACHE_MODEL_TTL, show_spinner=False)
def load_silhouette(dataset, k: int):
    return compute_silhouette(dataset, n_clusters=k)

# ==========================================================
# LOAD DATASET
# ==========================================================

try:

    df = load_dataset()

except Exception as e:

    st.error("Failed to load clustering dataset.")

    st.exception(e)

    st.stop()

if df.empty:

    st.warning("No monitoring data available.")

    st.stop()

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🧠 Clustering Analysis")

st.caption(
    "K-Means clustering of electrical operating patterns, including Elbow Method and Silhouette Score evaluation."
)

st.divider()

# ==========================================================
# OVERVIEW
# ==========================================================

metric1, metric2, metric3 = st.columns(3)

with metric1:

    metric_card(
        title="Total Records",
        value=len(df),
        icon="📄",
    )

with metric2:

    metric_card(
        title="Features",
        value=len(FEATURES),
        icon="🧩",
    )

with metric3:

    n_clusters = st.slider(
        "Number of Clusters (K)",
        min_value=2,
        max_value=MAX_K,
        value=DEFAULT_K,
    )

st.divider()

tab_overview, tab_elbow, tab_silhouette = st.tabs(
    [
        "K-Means Overview",
        "Elbow Method",
        "Silhouette Score",
    ]
)

# ==========================================================
# TAB 1 — K-MEANS OVERVIEW
# ==========================================================
with tab_overview:

    st.subheader("📊 K-Means Clustering")

    if st.button(
        "Run K-Means Clustering",
        type="primary",
        use_container_width=True,
    ):

        try:

            with st.spinner("Running clustering..."):

                km = load_kmeans(df, n_clusters)

                result = km["result"]
                model = km["model"]
                scaler = km["scaler"]
                X_scaled = km["scaled"]
                labels = km["labels"]

                statistics = cluster_statistics(result)
                centroid = cluster_centroid(model, scaler)
                distribution = cluster_distribution(result)

        except Exception as e:

            st.error("Failed to run K-Means clustering.")
            st.exception(e)
            st.stop()

        # ======================================================
        # SUMMARY
        # ======================================================

        st.divider()

        st.subheader("Clustering Summary")

        summary_cards = [

            {
                "title": "Clusters",
                "value": n_clusters,
                "icon": "🧠",
            },

            {
                "title": "Samples",
                "value": len(result),
                "icon": "📄",
            },

            {
                "title": "Inertia",
                "value": f"{model.inertia_:.2f}",
                "icon": "🎯",
            },

        ]

        columns = st.columns(len(summary_cards))

        for column, card in zip(columns, summary_cards):

            with column:

                metric_card(
                    title=card["title"],
                    value=card["value"],
                    icon=card["icon"],
                )

        # ======================================================
        # PCA VISUALIZATION
        # ======================================================

        st.divider()

        st.subheader("Cluster Visualization")

        plot_df = cluster_pca(
            X_scaled,
            labels,
        )

        fig = px.scatter(
            plot_df,
            x="PC1",
            y="PC2",
            color="Cluster",
            template="plotly_dark",
            height=PCA_HEIGHT,
            color_discrete_sequence=px.colors.sequential.Blues_r,
        )

        fig.update_traces(
            marker=dict(
                size=9,
                line=dict(
                    width=1,
                    color="#0E0F11",
                ),
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#E8E9EB",
                family="Inter",
            ),
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

        # ======================================================
        # DISTRIBUTION
        # ======================================================

        st.divider()

        st.subheader("Cluster Distribution & Statistics")

        left_column, right_column = st.columns(
            [1, 2],
            gap="large",
        )

        with left_column:

            fig_bar = px.bar(
                distribution,
                x="Cluster",
                y="Samples",
                text="Samples",
                template="plotly_dark",
                height=BAR_HEIGHT,
                color_discrete_sequence=["#5B8DEF"],
            )

            fig_bar.update_traces(
                textposition="outside",
            )

            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                font=dict(
                    color="#E8E9EB",
                    family="Inter",
                ),
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True,
                config={"displayModeBar": False},
            )

        with right_column:

            st.dataframe(
                statistics,
                use_container_width=True,
            )

        # ======================================================
        # INTERPRETATION
        # ======================================================

        st.divider()

        st.subheader("Cluster Interpretation")

        largest_cluster = distribution.loc[
            distribution["Samples"].idxmax(),
            "Cluster",
        ]

        smallest_cluster = distribution.loc[
            distribution["Samples"].idxmin(),
            "Cluster",
        ]

        left_column, right_column = st.columns(2)

        with left_column:

            panel(
                "Clustering Result",
                {
                    "Clusters": n_clusters,
                    "Samples": len(result),
                    "Largest Cluster": f"Cluster {largest_cluster}",
                    "Smallest Cluster": f"Cluster {smallest_cluster}",
                    "Inertia": f"{model.inertia_:.2f}",
                },
                icon="📋",
            )

        with right_column:

            panel(
                "Model Information",
                {
                    "Algorithm": "K-Means",
                    "Scaler": "StandardScaler",
                    "Features": len(FEATURES),
                    "Centroids": len(centroid),
                    "Status": "READY",
                },
                icon="⚙️",
            )

        # ======================================================
        # CLUSTER CHARACTERISTICS
        # ======================================================

        st.divider()

        st.subheader("Cluster Characteristics")

        cluster_columns = st.columns(n_clusters)

        for column, cluster_id in zip(
            cluster_columns,
            sorted(statistics.index),
        ):

            row = statistics.loc[cluster_id]

            with column:

                panel(
                    f"Cluster {cluster_id}",
                    {
                        "Voltage": f"{row['voltage']:.2f} V",
                        "Current": f"{row['current']:.2f} A",
                        "Power": f"{row['power']:.2f} W",
                        "Frequency": f"{row['frequency']:.2f} Hz",
                        "Power Factor": f"{row['power_factor']:.2f}",
                    },
                )

        # ======================================================
        # DOWNLOAD
        # ======================================================

        st.divider()

        st.download_button(
            label="📥 Download Cluster Result",
            data=result.to_csv(index=False).encode("utf-8"),
            file_name="cluster_result.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ==========================================================
# TAB 2 — ELBOW METHOD
# ==========================================================

with tab_elbow:

    st.subheader("📈 Elbow Method")

    try:

        elbow = load_elbow(df)

        elbow_df = elbow["elbow_df"]

        recommended_k = elbow["recommended_k"]

    except Exception as e:

        st.error("Failed to compute Elbow Method.")

        st.exception(e)

        st.stop()

    summary_cards = [

        {
            "title": "Recommended K",
            "value": recommended_k,
            "icon": "🎯",
        },

        {
            "title": "K Range",
            "value": f"2 - {MAX_K}",
            "icon": "📊",
        },

    ]

    columns = st.columns(len(summary_cards))

    for column, card in zip(columns, summary_cards):

        with column:

            metric_card(
                title=card["title"],
                value=card["value"],
                icon=card["icon"],
            )

    st.divider()

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=elbow_df["K"],

            y=elbow_df["WCSS"],

            mode="lines+markers",

            line=dict(
                color="#5B8DEF",
                width=2,
            ),

            marker=dict(size=8),

        )

    )

    fig.add_vline(

        x=recommended_k,

        line_dash="dash",

        line_color="#C9973E",

    )

    fig.update_layout(

        template="plotly_dark",

        height=ELBOW_HEIGHT,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#E8E9EB",
            family="Inter",
        ),

        xaxis_title="Number of Clusters (K)",

        yaxis_title="WCSS (Inertia)",

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar": False},

    )

    panel(

        "Elbow Method Interpretation",

        {

            "Recommended Cluster": recommended_k,

            "Method": "Elbow Method",

            "Metric": "WCSS (Inertia)",

            "Status": "READY",

        },

        icon="📈",

    )

# ==========================================================
# TAB 3 — SILHOUETTE SCORE
# ==========================================================

with tab_silhouette:

    st.subheader("⭐ Silhouette Score")

    try:

        silhouette = load_silhouette(

            df,

            n_clusters,

        )

        average_score = silhouette["avg_score"]

        cluster_score = silhouette["cluster_score"]

        quality_label, quality_description = (

            silhouette_quality(

                average_score

            )

        )

    except Exception as e:

        st.error("Failed to compute Silhouette Score.")

        st.exception(e)

        st.stop()

    summary_cards = [

        {

            "title": "Average Score",

            "value": f"{average_score:.4f}",

            "icon": "🎯",

        },

        {

            "title": "Quality",

            "value": quality_label,

            "icon": "⭐",

        },

    ]

    columns = st.columns(len(summary_cards))

    for column, card in zip(columns, summary_cards):

        with column:

            metric_card(

                title=card["title"],

                value=card["value"],

                icon=card["icon"],

            )

    st.divider()

    fig = px.bar(

        cluster_score,

        x="cluster",

        y="silhouette",

        text="silhouette",

        template="plotly_dark",

        height=SILHOUETTE_HEIGHT,

        color_discrete_sequence=["#5B8DEF"],

        labels={

            "cluster": "Cluster",

            "silhouette": "Average Silhouette",

        },

    )

    fig.update_traces(

        texttemplate="%{text:.3f}",

        textposition="outside",

    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(

            color="#E8E9EB",

            family="Inter",

        ),

        showlegend=False,

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar": False},

    )

    panel(

        "Silhouette Interpretation",

        {

            "Average Score": f"{average_score:.4f}",

            "Quality": quality_label,

            "Assessment": quality_description,

        },

        icon="⭐",

    )

# ==========================================================
# FOOTER
# ==========================================================

render_footer()