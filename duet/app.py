import os
import streamlit as st
from openai import OpenAI
import base64
import json
import requests
import re
import pandas as pd
from huggingface_hub import InferenceClient

HF_MODEL_MISTRAL = "mistralai/Mistral-7B-Instruct-v0.3"
HF_MODEL_LLAMA = "meta-llama/Llama-3.3-70B-Instruct"
HF_MODEL_DEEPSEEK = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"

UML_PROMPTS_DOC_URL = os.environ['UML_PROMPTS_DOC_URL']
ERD_PROMPTS_DOC_URL = os.environ['ERD_PROMPTS_DOC_URL']

STEP1_SYSTEM_PROMPT = "STEP1 SYSPROMPT"
STEP1_USER_PROMPT = "STEP1 USERPROMPT"
STEP2_SYSTEM_PROMPT = "STEP2 SYSPROMPT"
STEP2_USER_PROMPT = "STEP2 USERPROMPT"
STEP3A_SYSTEM_PROMPT = "STEP3A SYSPROMPT"
STEP3A_USER_PROMPT = "STEP3A USERPROMPT"
STEP3B_SYSTEM_PROMPT = "STEP3B SYSPROMPT"
STEP3B_USER_PROMPT = "STEP3B USERPROMPT"


def fetch_prompts_from_google_doc(diagram_type="UML"):
    if diagram_type == "UML":
        response = requests.get(UML_PROMPTS_DOC_URL)
    elif diagram_type == "ERD":
        response = requests.get(ERD_PROMPTS_DOC_URL)
    if response.status_code != 200:
        raise Exception("Failed to fetch document")
    
    text = response.text
    prompts = {}

    pattern = r"\{BEGIN (.*?)\}([\s\S]*?)\{END \1\}"
    matches = re.findall(pattern, text)

    for key, content in matches:
        prompts[key.strip()] = content.strip()

    return prompts

# Step 1: Extract PlantUML Code
def extract_plantuml_code(client_openai, uploaded_file, model_choice, prompts):

    st.write("Model: ", model_choice)

    encoded_image = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

    response = client_openai.chat.completions.create(
        model=model_choice,
        messages=[
            {
                "role": "system",
                "content": prompts[STEP1_SYSTEM_PROMPT],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompts[STEP1_USER_PROMPT]},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encoded_image}"},
                    },
                ],
            },
        ],
        temperature=0.2,
        top_p=0.1,
        max_tokens=4096,
    )

    return response.choices[0].message.content


# Step 2: Compare PlantUML Code
def compare_plantuml(client_openai, client_hf_mistral, client_hf_llama, client_hf_deepseek, plantuml_instructor, plantuml_student, model_choice, prompts, diagram_type="UML"):

    st.write("Model: ", model_choice)

    user_prompt=f"""
    {prompts[STEP2_USER_PROMPT]}
    
    **Instructor's {diagram_type} Diagram:**
    {plantuml_instructor}

    **Student's {diagram_type} Diagram:**
    {plantuml_student}
    """

    if model_choice in [HF_MODEL_MISTRAL]:
        response = client_hf_mistral.chat_completion(
            [
                {
                    "role": "system",
                    "content": prompts[STEP2_SYSTEM_PROMPT],
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1024,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"]
    
    elif model_choice in [HF_MODEL_LLAMA]:
        response = client_hf_llama.chat_completion(
            [
                {
                    "role": "system",
                    "content": prompts[STEP2_SYSTEM_PROMPT],
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1024,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"]

    elif model_choice in [HF_MODEL_DEEPSEEK]:
        response = client_hf_deepseek.chat_completion(
            [
                {
                    "role": "system",
                    "content": prompts[STEP2_SYSTEM_PROMPT],
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1024,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"]
    
    else:
        response = client_openai.chat.completions.create(
            model=model_choice,
            messages=[
                {
                    "role": "system",
                    "content": prompts[STEP2_SYSTEM_PROMPT],
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
            top_p=0.1,
            max_tokens=4096,
        )
        return response.choices[0].message.content

# Step 3A: Generate Student Feedback
def generate_student_feedback(client_openai, client_hf_mistral, client_hf_llama, client_hf_deepseek, differences, model_choice, prompts):

    st.write("Model (Student Feedback):", model_choice)  

    user_prompt=f"""
    {prompts[STEP3A_USER_PROMPT]}
    {json.dumps(differences, indent=2)}
    """

    if model_choice in [HF_MODEL_MISTRAL]:
        response = client_hf_mistral.chat_completion(
            [
                {
                    "role": "system",
                    "content": prompts[STEP3A_SYSTEM_PROMPT],
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1024,
            temperature=0.2,
        )

        return response["choices"][0]["message"]["content"]
      
    elif model_choice in [HF_MODEL_LLAMA]:
        response = client_hf_llama.chat_completion(
            [
                {
                    "role": "system",
                    "content": prompts[STEP3A_SYSTEM_PROMPT],
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1024,
            temperature=0.2,
        )

        return response["choices"][0]["message"]["content"]

    elif model_choice in [HF_MODEL_DEEPSEEK]:
        response = client_hf_deepseek.chat_completion(
            [
                {
                    "role": "system",
                    "content": prompts[STEP2_SYSTEM_PROMPT],
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1024,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"]
    
    else:
        response = client_openai.chat.completions.create(
            model=model_choice,
            messages=[
                {
                    "role": "system",
                    "content": prompts[STEP3A_SYSTEM_PROMPT],
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
            top_p=0.1,
            max_tokens=4096,
        )

        return response.choices[0].message.content


# Step 3B: Generate Educator Feedback
def generate_educator_feedback(client_openai, client_hf_mistral, client_hf_llama, client_hf_deepseek, differences, model_choice, prompts):
  
    st.write("Model (Educator Feedback): ", model_choice)

    user_prompt=f"""
    {prompts[STEP3B_USER_PROMPT]}
    {json.dumps(differences, indent=2)}
    """

    if model_choice in [HF_MODEL_MISTRAL]:
        response = client_hf_mistral.chat_completion(
            [
                {
                    "role": "system",
                    "content": prompts[STEP3B_SYSTEM_PROMPT],
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1024,
            temperature=0.2,
        )

        return response["choices"][0]["message"]["content"]
      
    elif model_choice in [HF_MODEL_LLAMA]:
        response = client_hf_llama.chat_completion(
            [
                {
                    "role": "system",
                    "content": prompts[STEP3B_SYSTEM_PROMPT],
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1024,
            temperature=0.2,
        )

        return response["choices"][0]["message"]["content"]

    elif model_choice in [HF_MODEL_DEEPSEEK]:
        response = client_hf_deepseek.chat_completion(
            [
                {
                    "role": "system",
                    "content": prompts[STEP2_SYSTEM_PROMPT],
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1024,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"]
    
    else:
        response = client_openai.chat.completions.create(
            model=model_choice,
            messages=[
                {
                    "role": "system",
                    "content": prompts[STEP3B_SYSTEM_PROMPT],
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
            top_p=0.1,
            max_tokens=4096,
        )

        return response.choices[0].message.content


# Streamlit app layout
st.set_page_config(
    page_title="LLM-based Analysis and Feedback of a UML or ER Diagram",
    page_icon="📝",
    initial_sidebar_state="expanded",
)

st.title("LLM-based Analysis and Feedback of a UML or ERD Diagram")
st.write("The pipeline consists of three steps:")
st.write("1. Extract PlantUML code from the uploaded UML or ER diagrams using GPT-4o or GPT-4o Mini.")
st.write("2. Compare the extracted PlantUML code.")
st.write("3. Analyse the differences and present them in a structured format.")

diagram_type = st.selectbox("Select the diagram type", ["UML", "ERD"])
prompts = fetch_prompts_from_google_doc(diagram_type)

openai_api_key = st.text_input("OpenAI API key", type="password")
hf_api_key = st.text_input("Hugging Face API key", type="password")

if openai_api_key and hf_api_key:
    client_openai = OpenAI(api_key=openai_api_key)
    client_hf_mistral = InferenceClient(model=HF_MODEL_MISTRAL, token=hf_api_key)
    client_hf_llama = InferenceClient(model=HF_MODEL_LLAMA, token=hf_api_key)
    client_hf_deepseek = InferenceClient(model=HF_MODEL_DEEPSEEK, token=hf_api_key)
    
    model_choice_step1 = st.selectbox("Select the model for Step 1", ["gpt-4o", "gpt-4o-mini"])
    model_choice_step2 = st.selectbox("Select the model for Step 2", [HF_MODEL_MISTRAL, HF_MODEL_LLAMA, "gpt-4o", "gpt-4o-mini"])
    model_choice_step3 = st.selectbox("Select the model for Step 3", [HF_MODEL_MISTRAL, HF_MODEL_LLAMA, "gpt-4o", "gpt-4o-mini"])

    st.subheader("Step 1: PlantUML Code Extraction using GPT-4o or GPT-4o Mini")

    col1, col2 = st.columns(2)
    with col1:
        uploaded_instructor_solution = st.file_uploader(
            "Upload Instructor " + ("UML" if diagram_type == 'UML' else "ER") + " Diagram", type=["jpg", "jpeg", "png"]
        )
    with col2:
        uploaded_student_solution = st.file_uploader(
            "Upload Student " + ("UML" if diagram_type == 'UML' else "ER") + " Diagram", type=["jpg", "jpeg", "png"]
        )

    if (uploaded_instructor_solution is not None and uploaded_student_solution is not None):
        try:
            with st.spinner(
                "Extracting PlantUML code from the uploaded " + ("UML" if diagram_type == 'UML' else "ER") + " diagrams..."
            ):
                with col1:
                    st.image(
                        uploaded_instructor_solution,
                        caption="Uploaded Instructor " + ("UML" if diagram_type == 'UML' else "ER") + " Diagram",
                        use_container_width=True,
                    )
                    st.write("")
                    plantuml_instructor_solution = extract_plantuml_code(
                        client_openai, uploaded_instructor_solution, model_choice_step1, prompts
                    )
                with col2:
                    st.write("")
                    st.image(
                        uploaded_student_solution,
                        caption="Uploaded Student " + ("UML" if diagram_type == 'UML' else "ER") + " Diagram",
                        use_container_width=True,
                    )
                    st.write("")
                    plantuml_student_solution = extract_plantuml_code(
                        client_openai, uploaded_student_solution, model_choice_step1, prompts
                    )

            st.write("Extracted PlantUML Code")
            col1, col2 = st.columns(2)
            with col1:
                st.text_area(
                    "PlantUML Code for Instructor Solution",
                    plantuml_instructor_solution,
                    height=600,
                )
            with col2:
                st.text_area(
                    "PlantUML Code for Student Solution",
                    plantuml_student_solution,
                    height=600,
                )

            st.subheader("Step 2: " + ("UML" if diagram_type == 'UML' else "ER") + " Diagram Comparison")
            with st.spinner("Comparing instructor and student " + ("UML" if diagram_type == 'UML' else "ER") + " diagrams..."):
                differences = compare_plantuml(
                    client_openai,
                    client_hf_mistral,
                    client_hf_llama,
                    client_hf_deepseek,
                    plantuml_instructor_solution,
                    plantuml_student_solution,
                    model_choice_step2,
                    prompts,
                    diagram_type
                )
                with st.expander("View differences"):
                    for difference in differences.split("\n"):
                        st.write(difference)

            st.subheader("Step 3: Structured Feedback")
            with st.spinner("Preparing structured feedback..."):
                student_feedback = generate_student_feedback(client_openai, client_hf_mistral, client_hf_llama, client_hf_deepseek, differences, model_choice_step3, prompts)
                educator_feedback = generate_educator_feedback(client_openai, client_hf_mistral, client_hf_llama, client_hf_deepseek, differences, model_choice_step3, prompts)

                col1, col2 = st.columns(2)
                with col1:
                    st.write("Student Feedback")
                    st.markdown(f"{student_feedback}")
                with col2:
                    st.write("Educator Feedback")
                    st.markdown(f"{educator_feedback}")

        except Exception as e:
            st.error(f"Error: {e}")
else:
    if not openai_api_key:
        st.error("Please provide a valid OpenAI API key.")
    else:
        st.error("Please provide a valid Hugging Face API key.") 