import streamlit as st
import google.generativeai as genai

# ✅ Configure Google AI Studio API Key
API_KEY = "AIzaSyCLVJL6RuQa3l7sDzzHQYzXdNl1YQobhxE"  # 🔥 Replace with your actual Google AI Studio API key
genai.configure(api_key=API_KEY)

# ✅ Load Gemini Model (Use "gemini-1.5-flash" for free access)
model = genai.GenerativeModel("gemini-1.5-flash")

# 🎨 Streamlit UI
st.title("🍛 AI-Powered Indian Recipe Generator")
st.write("Get customized Indian recipes based on your available ingredients and health needs.")

# 📌 User Input: Ingredients
ingredients = st.text_area(
    "Enter the ingredients you have (comma-separated):",
    placeholder="e.g., rice, lentils, tomatoes, turmeric"
)

# 📌 User Input: Health Condition
health_condition = st.selectbox(
    "Select Your Health Condition:",
    ["None", "Diabetes", "Cardiac", "Obesity", "General Health"]
)

# 📌 User Input: Meal Type
meal_type = st.radio(
    "Select Meal Type:",
    ["Breakfast", "Lunch", "Dinner", "Snack"]
)

# 📌 Fetch Recipe Button
if st.button("Generate Recipe"):
    with st.spinner("Fetching your custom Indian recipe... 🍽️"):
        # 🔥 AI Prompt
        prompt = f"""
        Suggest a **detailed** Indian {meal_type} recipe using the following ingredients: {ingredients}.
        Consider the health condition: {health_condition}.

        **Recipe Details:**
        - Name of the dish
        - Ingredients with quantity
        - Step-by-step cooking instructions
        - Estimated cooking time
        - Nutritional information
        - Add-ons (e.g., chutneys, side dishes, beverages)

        Keep it simple, authentic, and flavorful!
        """

        try:
            response = model.generate_content(prompt)
            st.session_state.recipe = response.text
            st.session_state.show_modify_option = True
            st.success("Here's your custom recipe! 👇")
            st.write(response.text)
        except Exception as e:
            st.error("⚠️ Error fetching recipe. Please check your API key or try again later.")
            st.write(e)

# 📌 Modification Option
if st.session_state.get("show_modify_option", False):
    st.subheader("Need Changes?")
    modifications = st.text_area("Specify modifications (e.g., remove potatoes, add spinach)")
    
    if st.button("Modify Recipe"):
        with st.spinner("Updating your recipe... 🔄"):
            mod_prompt = f"""
            Modify the following recipe based on these user preferences: {modifications}.
            
            {st.session_state.recipe}
            """
            
            try:
                mod_response = model.generate_content(mod_prompt)
                st.session_state.recipe = mod_response.text
                st.success("Here's your updated recipe! 👇")
                st.write(mod_response.text)
            except Exception as e:
                st.error("⚠️ Error modifying the recipe. Please try again.")
                st.write(e)

# 🎨 Footer
st.markdown("---")
st.markdown("Made with ❤️")