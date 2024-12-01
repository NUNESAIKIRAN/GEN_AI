import streamlit as st
import google.generativeai as ai

#------------------------------------------------------------------------------------

st.title("Market Research & Use Case Generation Agent")
#--------------------------------------------------------------------------------------
key = "AIzaSyCLS41AvwqkeMVo3w6WINTBhTJaR_putUw"
ai.configure(api_key=key)

# Selecting the model
model = ai.GenerativeModel(model_name="gemini-1.5-flash")
#--------------------------------------------------------------------------------------
def main(company_name, research_prompt, use_case_prompt):
    try:
        # Industry Research
        st.subheader("Industry Research")
        industry_research = model.generate_content(research_prompt)
        st.write(industry_research.text)

        # Generating AI use cases
        st.subheader("Generated AI Use Cases")
        use_cases = model.generate_content(use_case_prompt)
        st.write(use_cases.text)

        # Parse and structure use cases for the dataset prompt
        structured_use_cases = "\n".join(
            [f"- {line.strip()}" for line in use_cases.text.split("\n") if line.strip()]
        )

        if not structured_use_cases:
            st.error("No valid use cases generated. Please refine the prompts or input.")
            return

        # Creating dataset prompt based on structured use cases
        dataset_prompt = f"""
        Based on the following AI/ML use cases:

        {structured_use_cases}

        Provide a detailed list of open-source datasets or platforms where data can be found to support these use cases. 
        Include details about the type of data (e.g., text, images, numerical, sensor data, etc.) and the specific 
        platforms or repositories (e.g., Kaggle, Hugging Face, GitHub) that are most relevant.
        """
        
        # Collecting datasets
        st.subheader("Relevant Datasets")
        datasets = model.generate_content(dataset_prompt)
        st.write(datasets.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.write("### Step 1: Enter Company Name")
company_name = st.text_input("Company Name", placeholder="Enter a company name here...")

if st.button("Generate Report"):
    if company_name.strip():  # Check if a valid company name is provided
        # Generate prompts
        research_prompt = f"""
        Research the company '{company_name}' and provide:
        - Industry segment.
        - Key offerings and focus areas.
        - Competitors and their market strategies.
        """
        use_case_prompt = f"""
        Based on the industry research for '{company_name}', suggest:
        - AI/ML use cases to improve operations.
        - GenAI applications to enhance customer experience.
        """
        
        # Execute the main logic
        main(company_name, research_prompt, use_case_prompt)
    else:
        st.error("Please enter a valid company name to generate the report.")
