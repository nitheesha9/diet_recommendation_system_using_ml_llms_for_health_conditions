import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score
import time

# Hide sidebar navigation & set wide layout
st.set_page_config(page_title="Personalized Diet Recommendation System Using ML and LLMs", layout="wide", initial_sidebar_state="collapsed")

# Hide Streamlit's left-side navigation menu
st.markdown("""
    <style>
        body {
            background-color: #f8f9fc;
            color: #4b0082;
        }
        .st-emotion-cache-10trblm {
            background-color: white !important;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .stButton > button {
            background-color: #6a0dad;
            color: white;
            border-radius: 8px;
        }
        .stButton > button:hover {
            background-color: #4b0082;
        }
        .title-style {
            font-size: 35px;
            font-weight: bold;
            color: #6a0dad;
            text-align: center;
            padding: 10px;
            border-bottom: 3px solid #4b0082;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .st-emotion-cache-1y4p8pa {display: block;} /* Show page navigation */
    </style>
""", unsafe_allow_html=True)

# Load dataset
file_path = 'dataset_food.xlsx'  # Updated dataset
df = pd.read_excel(file_path)

df.columns = df.columns.str.strip().str.lower()

# Initialize session state
if "selected_meals" not in st.session_state:
    st.session_state["selected_meals"] = {"Breakfast": [], "Lunch": [], "Dinner": [], "Snacks": []}
if "profile_submitted" not in st.session_state:
    st.session_state["profile_submitted"] = False

# User Profile (Hidden Until Submitted)
st.sidebar.header("👤 User Profile")
age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=220, value=170)
activity_level = st.sidebar.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
health_condition = st.sidebar.selectbox("Health Condition", ["None", "Diabetes", "Cardiac", "High_BP"]).lower()

if st.sidebar.button("Submit"):
    st.session_state["profile_submitted"] = True

if st.session_state["profile_submitted"]:
    def calculate_daily_requirements(weight, height, age, gender, activity_level):
        if gender == "Male":
            bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
        else:
            bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
        activity_multipliers = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725}
        tdee = bmr * activity_multipliers[activity_level]
        return {
            "energy_kcal": round(tdee),
            "protein_g": round(weight * 1.2),
            "carb_g": round((tdee * 0.5) / 4),
            "fat_g": round((tdee * 0.3) / 9),
            "fibre_g": 25
        }

    daily_requirements = calculate_daily_requirements(weight, height, age, gender, activity_level)

    st.sidebar.subheader("📊 Daily Nutritional Requirements")
    for nutrient, value in daily_requirements.items():
        st.sidebar.write(f"{nutrient.replace('_', ' ').title()}: {value}")
    def evaluate_clustering(df_scaled, clustering):
        labels = clustering.labels_
        unique_labels = set(labels)
        
        num_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
        num_noise = list(labels).count(-1)

        # Default scores
        silhouette, davies_bouldin = -1, -1

        if num_clusters > 1 and np.count_nonzero(labels != -1) > 1:
            valid_indices = labels != -1
            silhouette = silhouette_score(df_scaled[valid_indices], labels[valid_indices])
            davies_bouldin = davies_bouldin_score(df_scaled[valid_indices], labels[valid_indices])

        return num_clusters, num_noise, silhouette, davies_bouldin

    

    def fine_tune_dbscan(df_scaled):
        best_eps, best_min_samples, best_metric = 1.2, 5, "manhattan"
        best_score, best_model = -1, None

        for eps in np.arange(1.0, 2.0, 0.02):
            for min_samples in range(3, 11):
                for metric in ["euclidean", "manhattan", "chebyshev"]:
                    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric=metric).fit(df_scaled)
                    labels = clustering.labels_
                    unique_clusters = set(labels) - {-1}

                    if len(unique_clusters) > 1 and np.count_nonzero(labels != -1) > 1:
                        valid_indices = labels != -1
                        score = silhouette_score(df_scaled[valid_indices], labels[valid_indices])

                        if score > best_score:
                            best_score = score
                            best_eps = eps
                            best_min_samples = min_samples
                            best_metric = metric
                            best_model = clustering

                        if best_score >= 0.7:
                            return best_model, best_eps, best_min_samples, best_metric, best_score

        return best_model, best_eps, best_min_samples, best_metric, best_score

    def recommend_meals(health_condition):
        features = ['carb_g', 'protein_g', 'fat_g', 'freesugar_g', 'sodium_mg', 'fibre_g']
        df_features = df[features].fillna(0)
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_features)
        start_time = time.time()
        clustering, best_eps, best_min_samples, best_metric, best_silhouette = fine_tune_dbscan(df_scaled)
        execution_time = time.time() - start_time

        df['Cluster'] = clustering.labels_

        num_clusters, num_noise, silhouette, davies_bouldin = evaluate_clustering(df_scaled, clustering)
     

       

        if health_condition == "diabetes":
            condition_filter = (df['freesugar_g'] < 5) & (df['carb_g'] < 50)
        elif health_condition == "high_bp":
            condition_filter = df['sodium_mg'] < 140
        elif health_condition == "cardiac":
            condition_filter = (df['fat_g'] < 25) & (df['fibre_g'] > 2)
        else:
            condition_filter = df.index >= 0  # Select all rows if no health condition is specified
        
        recommended_foods = df[condition_filter]
        meals = {
            "Breakfast": recommended_foods[recommended_foods['breakfast'] == 1]['food_name'].tolist(),
            "Lunch": recommended_foods[recommended_foods['lunch'] == 1]['food_name'].tolist(),
            "Dinner": recommended_foods[recommended_foods['dinner'] == 1]['food_name'].tolist(),
            "Snacks": recommended_foods[recommended_foods['snacks'] == 1]['food_name'].tolist()
        }
        return meals,best_silhouette,davies_bouldin
    
    st.markdown("<div class='title-style'>PERSONALIZED DIET RECOMMENDATION SYSTEM USING ML AND LLMS FOR VARIOUS HEALTH CONDITIONS</div>", unsafe_allow_html=True)
    

    # Meal Recommendations
    st.header("🍽️ Meal Recommendations")
    meals, silhouette, davies_bouldin = recommend_meals(health_condition)
    st.session_state["selected_meals"] = meals
    
    if isinstance(meals, dict):
        st.subheader("Select Your Meal Options")
        breakfast = st.multiselect("Breakfast Recommendations", meals["Breakfast"])
        lunch = st.multiselect("Lunch Recommendations", meals["Lunch"])
        dinner = st.multiselect("Dinner Recommendations", meals["Dinner"])
        snacks = st.multiselect("Snacks Recommendations", meals["Snacks"])
        
    st.header("📊 Meal Tracker")

    selected_meals = breakfast + lunch + dinner + snacks
    daily_intake = {nutrient: 0 for nutrient in daily_requirements.keys()}
    for meal in selected_meals:
        meal_data = df[df['food_name'] == meal]
        for nutrient in daily_intake.keys():
            if nutrient in meal_data.columns:
                daily_intake[nutrient] += meal_data[nutrient].sum()
    
    for nutrient, value in daily_intake.items():
        max_value = daily_requirements.get(nutrient, 100)
        progress = min(value / max_value, 1)
        color = "#FF0000" if value > max_value else "#4CAF50"
        st.markdown(f'<p style="color: {color}; font-weight: bold; margin-top: 10px;">{nutrient.replace("_", " ").title()}: {value:.1f}</p>', unsafe_allow_html=True)
        st.progress(progress)
        if value > max_value:
            st.warning(f"⚠️ {nutrient.replace('_', ' ').title()} intake exceeded daily requirement!")
    
    st.subheader("📊 Clustering Evaluation Metrics")
    st.write(f"Silhouette Score: {silhouette:.4f}")
    st.write(f"Davies-Bouldin Score: {davies_bouldin:.4f}")

