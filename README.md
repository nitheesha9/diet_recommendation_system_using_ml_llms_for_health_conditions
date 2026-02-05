# diet_recommendation_system_using_ml_llms_for_health_conditions
1️⃣ Project Title
Personalized Diet Recommendation System Using ML & LLMs for various health conditions.

2️⃣ Abstract
Maintaining  a  healthy  diet  for  conditions  like  diabetes,  heart  disease,  and High BP is  difficult.  Many  people  struggle  to  choose  the  right  foods  and calculate nutritional values.The Proposed model suggests Indian meals (breakfast, lunch, dinner) based on user health conditions.Uses Machine Learning (ML) and Large Language Models (LLMs) for meal recommendations  and  Provides  nutritional  information  like  calories,  carbs, proteins, and fats.Helps users make better food choices and manage their health effectively.

3️⃣ Problem Statement
Chronic  diseases  like  diabetes,  cardiovascular  issues,  and  High BP require  strict dietary management, but many individuals struggle to make informed food choices due to a lack of tools or knowledge. Existing dietary guidance is often generic and insufficiently personalized. The objective is to provide individuals with chronic conditions  access to personalized, accessible dietary tools that  help them make informed food choices.

4️⃣ Proposed Solution
The system takes user health details as input, processes nutritional data from the Indian Nutrient Databank, applies DBSCAN clustering to group food items, and uses an LLM to generate meal plans and recipes. The output is displayed through a Streamlit web application.

5️⃣ System Architecture
The system takes user health details as input, processes nutritional data from the Indian Nutrient Databank, applies DBSCAN clustering to group food items, and uses an LLM to generate meal plans and recipes. The output is displayed through a Streamlit web application.
FLOW:
User Input → Data Preprocessing → DBSCAN Clustering → Rule-Based Filtering → LLM Recipe Generator → Output

6️⃣ Technologies Used
Python
Machine Learning
DBSCAN Clustering
Large Language Models (LLMs – Gemini)
Streamlit
Pandas, NumPy
Scikit-learn

7️⃣ Dataset
ANUVAAD_DATASET
Dataset: Contains 1,014 food items and 82 columns with detailed nutritional information, including macronutrients (carbohydrates, proteins, fats), micronutrients (vitamins, minerals), and other essential dietary factors.

Conclusion & Future Scope
->AI-Powered Meal Planning: Uses DBSCAN clustering and rule-based filtering to provide personalized dietary recommendations.
->LLM-Driven Recipe Generation: Dynamically creates meal ideas based on user-selected ingredients and health conditions.

Future Scope: Expand to support thyroid disorders, PCOS, kidney diseases, and other health conditions for comprehensive nutrition guidance.
















