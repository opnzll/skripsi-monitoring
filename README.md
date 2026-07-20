# ⚡ Smart Energy Analytics Platform

An IoT-based electrical energy monitoring and analytics platform developed as an undergraduate thesis project. The system collects real-time electrical parameters from an ESP32 and PZEM-004T energy meter, stores the data in a MySQL database, and provides interactive visualization and machine learning analysis through a Streamlit web dashboard.

## Features

* Real-time electrical parameter monitoring
* Interactive Streamlit dashboard
* Historical data visualization and export
* Energy analytics and descriptive statistics
* K-Means clustering for operating pattern analysis
* Elbow Method for optimal cluster selection
* Silhouette Score for clustering validation
* MySQL database integration
* Responsive and modern user interface

## Technology Stack

* **Hardware**

  * ESP32
  * PZEM-004T Energy Meter

* **Software**

  * Python
  * Streamlit
  * MySQL
  * SQLAlchemy
  * Pandas
  * Plotly
  * Scikit-learn

## Machine Learning

This platform implements unsupervised learning using the K-Means algorithm to identify electrical consumption patterns. The clustering process is evaluated using:

* Elbow Method
* Silhouette Score
* Principal Component Analysis (PCA) Visualization

## Project Structure

```text
backend/
components/
pages/
assets/
logs/
```

## Author

**Naufal Zul Fikri**

Undergraduate Thesis Project

Department of Electrical Engineering Education

Universitas Pendidikan Indonesia (UPI)

2026
