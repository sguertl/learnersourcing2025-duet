# Automated Feedback on Student-Generated UML and ER Diagrams Using Large Language Models

## Supplement Materials for Learnersourcing 2025

In this GitHub repository you can find supplement materials for our Learnersourcing 2025 paper *Automated Feedback on Student-Generated UML and ER Diagrams Using Large Language Models*.

It contains both the source code of the tool *DUET* as well as further resources.

## Usage of DUET

Requirements:
* Python (3.10+)
* OpenAI API Key
* HuggingFace API Key (alternative: Ollama)

To run DUET locally, install the requirements from the `requirements.txt` file and run the application with the following command:
```
streamlit run app.py
```

You should be able to access the application at [http://localhost:8501](http://localhost:8501).

As an alternative to HuggingFace's inference endpoints, you can Ollama to access smaller LLMs locally by replacing the HuggingFace inference clients with Ollama inference clients. For example, you can access an LLM hosted locally via Ollama using this code snippet:
```python
response = ollama.chat(
    model=model_choice,
    messages=[{"role": "system", "content": prompts[STEP2_SYSTEM_PROMPT]},
            {"role": "user", "content": user_prompt}],
    options={"temperature": 0.2},
)
```

## Resources

* [Prompts](resources/PROMPTS.md) - All system and user prompts used for UML and ER diagram conversion, identification of differences and generation of structured feedback.
* [UML Diagram Example](resources/UML.md)
* [ER Diagram Example](resources/ERD.md)
* [Results of Data Analysis](resources/Interviews-Analysis.xlsx)

# Authors

This research was conducted by:
* Sebastian Gürtl (sebastian.guertl@tugraz.at), Graz University of Technology, Austria
* Gloria Schimetta (gloria.schimetta@student.tugraz.at), Graz University of Technology, Austria
* David Kerschbaumer (david.kerschbaumer@tugraz.at), Graz University of Technology, Austria
* Michael Liut (michael.liut@utoronto.ca), University of Toronto, Canada
* Alexander Steinmaurer (alexander.steinmaurer@it-u.at), Interdisciplinary Transformation University Austria, Austria

# Acknowledgements
The authors thank the Natural Sciences and Engineering Research Council of Canada (NSERC), Discovery Grant #RGPIN-2024-04348, for their financial support.
