import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# New imports for AI Search
from sentence_transformers import SentenceTransformer, util

# =====================================================================
# PAGE CONFIGURATION
# =====================================================================
st.set_page_config(layout="wide", page_title="Bukit Vista AI Dashboard")
st.title("Dashboard & AI Search Properti Bukit Vista")

# =====================================================================
# FUNCTION & DATA LOADING (CACHED FOR PERFORMANCE)
# =====================================================================

# Code comment in English
# Cache the CSV data so it's loaded only once
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('cleaned_properties.csv')
        return df
    except FileNotFoundError:
        st.error("File 'cleaned_properties.csv' tidak ditemukan.")
        return None

# Code comment in English
# Cache the AI "brain" (embeddings)
@st.cache_data
def load_embeddings():
    try:
        embeddings = np.load('property_embeddings.npy')
        return embeddings
    except FileNotFoundError:
        st.error("File 'property_embeddings.npy' tidak ditemukan.")
        return None

# Code comment in English
# Cache the AI model itself (this is the heaviest resource)
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-MiniLM-L6-v2')

# --- Load all data on startup ---
df = load_data()
property_embeddings = load_embeddings()
model = load_model()

# Code comment in English
# Stop the app if data loading failed
if df is None or property_embeddings is None:
    st.stop()

# =====================================================================
# CREATE TABS
# =====================================================================

tab1, tab2 = st.tabs(["Dashboard EDA Portofolio", "Mesin Pencari Cerdas GAIA"])

# =====================================================================
# TAB 1: EDA DASHBOARD
# =====================================================================
with tab1:
    st.header("Peta Lokasi Properti")
    # Code comment in English
    # Filter out properties without valid lat/lon for mapping
    df_mapped = df.dropna(subset=['latitude', 'longitude'])
    st.markdown(f"Menampilkan **{len(df_mapped)}** dari **{len(df)}** properti di peta.")
    st.map(df_mapped, latitude='latitude', longitude='longitude', size=10)

    st.header("Analisis Portofolio")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tipe Properti")
        prop_type_counts = df['property_type'].value_counts()
        st.bar_chart(prop_type_counts)
    with col2:
        st.subheader("Status Properti")
        prop_status_counts = df['property_status'].value_counts()
        st.bar_chart(prop_status_counts)

    col4, col5 = st.columns(2)
    with col4:
        # ===== PERBAIKAN 1: Menggunakan Histogram untuk Rating =====
        st.subheader("Sebaran Rating Airbnb")
        # Code comment in English
        # Filter NaNs before plotting
        fig_rating = px.histogram(df.dropna(subset=['airbnb_rating']), x='airbnb_rating', nbins=10, color_discrete_sequence=['#0068C9'])
        st.plotly_chart(fig_rating, use_container_width=True)
        # =========================================================
        
    with col5:
        st.subheader("Sebaran Kapasitas Tamu")
        fig_guests = px.histogram(df, x='number_of_guests', nbins=10, color_discrete_sequence=['#00A36C'])
        st.plotly_chart(fig_guests, use_container_width=True)

    st.header("Data Properti")
    st.dataframe(df())

# =====================================================================
# TAB 2: SEMANTIC SEARCH
# =====================================================================
with tab2:
    st.header("Cari Properti Berdasarkan Keinginan Anda")
    st.markdown("Contoh: _'Villa dengan kolam renang pribadi dan pemandangan laut'_ atau _'tempat yang tenang untuk kerja'_")

    # Code comment in English
    # 1. Get user query from text input
    user_query = st.text_input("Apa yang Anda cari?", "")

    if user_query:
        # Code comment in English
        # 2. Encode the user's query into a vector
        query_embedding = model.encode(user_query, convert_to_tensor=True)

        # Code comment in English
        # 3. Calculate cosine similarity between the query and all 51 property embeddings
        cosine_scores = util.cos_sim(query_embedding, property_embeddings)[0]

        # Code comment in English
        # 4. Get the top 5 results
        top_results_indices = np.argsort(-cosine_scores)[0:5]

        st.subheader("Hasil Pencarian Teratas:")
        
        # Code comment in English
        # 5. Display the results
        for idx in top_results_indices:
            
            # ===== PERBAIKAN 2: Mengubah Tipe Data `idx` =====
            # Code comment in English
            # We must cast 'idx' (which is numpy.int64) to a standard Python 'int'
            # because 'df.iloc[]' is strict and only accepts standard 'int'.
            
            py_idx = int(idx) # <-- Konversi ke int
            
            # Code comment in English
            # Use the new 'py_idx' to safely index the DataFrame
            property_data = df.iloc[py_idx] 
            
            # Code comment in English
            # We can use either 'idx' or 'py_idx' to index the tensor
            score = cosine_scores[idx] 
            # =================================================

            st.markdown("---")
            
            # Code comment in English
            # Create columns for image and info
            col_img, col_info = st.columns([1, 3])
            
            with col_img:
                st.image(property_data['picture_url'], width=200)

            with col_info:
                st.markdown(f"**{property_data['name']}**")
                st.markdown(f"**Tipe:** {property_data['property_type']} | **Rating:** {property_data['airbnb_rating']} | **Kapasitas:** {property_data['number_of_guests']} tamu")
                st.markdown(f"**Skor Kecocokan:** {score:.2f}")
                
                # Code comment in English
                # Show a snippet of the description
                st.caption(f"{property_data['all_text_clean'][:200]}...")
                
                # Code comment in English
                # Add a link button if the URL exists
                if pd.notna(property_data['airbnb_url']):
                    st.link_button("Lihat di Airbnb", property_data['airbnb_url'])