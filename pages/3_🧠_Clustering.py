import streamlit as st

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/🔐_Login.py")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer
from components.cards import metric_card
from components.panel import panel

from backend.database import get_last
from backend.clustering import (
    run_kmeans, cluster_statistics, cluster_centroid,
    cluster_pca, cluster_distribution,
    compute_elbow, compute_silhouette, silhouette_quality,
    FEATURES,
)

st.set_page_config(page_title="Clustering Analysis", page_icon="🧠", layout="wide")

with open("assets/style.css", encoding="utf-8") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

render_sidebar()
render_header()

st.title("🧠 Clustering Analysis")
st.caption("K-Means clustering of electrical operating patterns, with Elbow Method and Silhouette Score to validate the chosen number of clusters.")

df = get_last(500)

if df.empty:
    st.warning("No monitoring data available.")
    st.stop()

# ==========================================================
# SHARED CONFIG
# ==========================================================

st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    metric_card("Total Records", len(df), icon="📄")
with c2:
    metric_card("Features", len(FEATURES), icon="🧩")
with c3:
    n_clusters = st.slider("Number of Clusters (k)", min_value=2, max_value=10, value=3)

st.divider()

tab_overview, tab_elbow, tab_silhouette = st.tabs(["K-Means Overview", "Elbow Method", "Silhouette Score"])

# ==========================================================
# TAB 1 — K-MEANS OVERVIEW
# ==========================================================

with tab_overview:

    run = st.button("Run K-Means Clustering", use_container_width=True, type="primary")

    if run:
        with st.spinner("Running K-Means..."):
            km = run_kmeans(df, n_clusters=n_clusters)
            result, model, scaler, X_scaled, labels = (
                km["result"], km["model"], km["scaler"], km["scaled"], km["labels"]
            )
            cluster_stats = cluster_statistics(result)
            centroid = cluster_centroid(model, scaler)
            dist_df = cluster_distribution(result)

        st.divider()
        st.subheader("Clustering Summary")

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Clusters", n_clusters, icon="🧠")
        with c2:
            metric_card("Samples", len(result), icon="📄")
        with c3:
            metric_card("Inertia", f"{model.inertia_:.2f}", icon="🎯")

        st.divider()
        st.subheader("Cluster Visualization")

        plot_df = cluster_pca(X_scaled, labels)

        fig = px.scatter(
            plot_df, x="PC1", y="PC2", color="Cluster",
            template="plotly_dark", height=560,
            color_discrete_sequence=px.colors.sequential.Blues_r,
        )
        fig.update_traces(marker=dict(size=9, line=dict(width=1, color="#0E0F11")))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E8E9EB", family="Inter"),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("Cluster Distribution & Statistics")

        left, right = st.columns([1, 2], gap="large")

        with left:
            fig_bar = px.bar(
                dist_df, x="Cluster", y="Samples", text="Samples",
                template="plotly_dark", height=340,
                color_discrete_sequence=["#5B8DEF"],
            )
            fig_bar.update_traces(textposition="outside")
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E8E9EB", family="Inter"),
                showlegend=False,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with right:
            st.dataframe(cluster_stats, use_container_width=True)

        st.divider()
        st.subheader("Cluster Interpretation")

        largest = dist_df.loc[dist_df["Samples"].idxmax(), "Cluster"]
        smallest = dist_df.loc[dist_df["Samples"].idxmin(), "Cluster"]

        left, right = st.columns(2, gap="large")

        with left:
            panel("Clustering Result", {
                "Total Cluster": n_clusters,
                "Total Samples": len(result),
                "Largest Cluster": f"Cluster {largest}",
                "Smallest Cluster": f"Cluster {smallest}",
                "Inertia": f"{model.inertia_:.2f}",
            }, icon="📋")

        with right:
            panel("Model Information", {
                "Algorithm": "K-Means",
                "Features": len(FEATURES),
                "Scaler": "StandardScaler",
                "Status": "READY",
            }, icon="⚙️")

        st.divider()
        st.subheader("Cluster Characteristics")

        cols = st.columns(n_clusters)
        for i, cluster_id in enumerate(sorted(cluster_stats.index)):
            row = cluster_stats.loc[cluster_id]
            with cols[i]:
                panel(f"Cluster {cluster_id}", {
                    "Voltage": f"{row['voltage']:.2f} V",
                    "Current": f"{row['current']:.2f} A",
                    "Power": f"{row['power']:.2f} W",
                    "Frequency": f"{row['frequency']:.2f} Hz",
                    "Power Factor": f"{row['power_factor']:.2f}",
                })

        st.divider()

        csv = result.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Cluster Result", data=csv,
            file_name="cluster_result.csv", mime="text/csv",
            use_container_width=True,
        )

# ==========================================================
# TAB 2 — ELBOW METHOD
# ==========================================================

with tab_elbow:

    elbow = compute_elbow(df, max_k=10)
    elbow_df = elbow["elbow_df"]
    recommended_k = elbow["recommended_k"]

    c1, c2 = st.columns(2)
    with c1:
        metric_card("Recommended K", recommended_k, icon="🎯")
    with c2:
        metric_card("K Range Tested", "2 – 10", icon="📈")

    st.divider()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=elbow_df["K"], y=elbow_df["WCSS"],
        mode="lines+markers", line=dict(color="#5B8DEF", width=2),
        marker=dict(size=8),
    ))
    fig.add_vline(x=recommended_k, line_dash="dash", line_color="#C9973E")
    fig.update_layout(
        template="plotly_dark", height=440,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E8E9EB", family="Inter"),
        xaxis_title="Number of Clusters (K)", yaxis_title="WCSS (Inertia)",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(f"The elbow point suggests **K = {recommended_k}** as the optimal number of clusters, based on the point of maximum curvature in the WCSS curve.")

# ==========================================================
# TAB 3 — SILHOUETTE SCORE
# ==========================================================

with tab_silhouette:

    sil = compute_silhouette(df, n_clusters=n_clusters)
    avg_score = sil["avg_score"]
    cluster_score = sil["cluster_score"]
    quality_label, quality_desc = silhouette_quality(avg_score)

    c1, c2 = st.columns(2)
    with c1:
        metric_card("Average Silhouette Score", f"{avg_score:.4f}", icon="🎯")
    with c2:
        metric_card("Quality", quality_label, icon="⭐")

    st.divider()

    fig = px.bar(
        cluster_score, x="cluster", y="silhouette", text="silhouette",
        template="plotly_dark", height=380,
        color_discrete_sequence=["#5B8DEF"],
        labels={"cluster": "Cluster", "silhouette": "Avg. Silhouette"},
    )
    fig.update_traces(textposition="outside", texttemplate="%{text:.3f}")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E8E9EB", family="Inter"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(quality_desc)

render_footer()