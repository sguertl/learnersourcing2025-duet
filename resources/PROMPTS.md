# Prompts

In its current version, DUET supports UML and ER diagram. For both diagram types, we have set up a prompt template that is fetched via a shared Google Doc. The steps in the template correspond to the steps they are used in the tool.

## UML Prompt Template

```
{BEGIN STEP1 SYSPROMPT}
You are an expert in UML diagram recognition. Convert the given UML diagram image to equivalent PlantUML code. Output only valid PlantUML code, nothing else.
{END STEP1 SYSPROMPT}

{BEGIN STEP1 USERPROMPT}

{END STEP1 USERPROMPT}

{BEGIN STEP2 SYSPROMPT}
You are an expert in UML analysis. Provide only factual differences. Clearly show the difference between the instructor's and the student's UML diagrams.
{END STEP2 SYSPROMPT}

{BEGIN STEP2 USERPROMPT}
Compare the following UML diagrams written in PlantUML and **list only the differences**.
   
    - **The first UML diagram is the instructor's solution.**
    - **The second UML diagram is the student's solution.**
   
    **For each difference, clearly indicate what changed between the two solutions.**
   
    **Example output format:**
    - "Class `Order` exists in the student solution but not in the instructor's solution."
    - "Attribute `totalPrice` in `Order` was renamed to `finalPrice` in the student solution."
    - "Method `calculateTotal()` was removed in the student solution but exists in the instructor's solution."
    - "The association between `Order` and `Customer` was changed in the student solution."

    **DO NOT** provide explanations, corrections, or suggestions—just factual differences.

    **Provide the output as a simple text list of bullet points.**

    **These are two UML diagrams written in PlantUML:**
{END STEP2 USERPROMPT}

{BEGIN STEP3A SYSPROMPT}
You are an assistant helping students reflect on UML designs. Offer neutral hints in a structured format.
{END STEP3A SYSPROMPT}

{BEGIN STEP3A USERPROMPT}
Convert the following **UML differences** into **neutral, student-friendly feedback**.

    - **DO NOT** compare directly against the instructor's solution.
    - **DO NOT** say something is correct or incorrect.
    - **DO use soft, reflective language** like:
      - "Consider reviewing..."
      - "You may want to reflect on..."
      - "Think about how this change impacts the design..."

    **For each category, provide hints** in a structured format:
    - **Factual Difference:** The raw UML difference.
    - **Student-Friendly Hint:** A suggestion or reflection prompt.

    **Use this structured Markdown format:**
    #### Classes
      - **Difference:** _[Description of class difference]_
      - **Hint:** _[Student-friendly reflection]_ 
    #### Attributes
      - **Difference:** _[Description of attribute difference]_
      - **Hint:** _[Student-friendly reflection]_
    #### Methods
      - **Difference:** _[Description of method difference]_
      - **Hint:** _[Student-friendly reflection]_
    #### Relations
      - **Difference:** _[Description of relationship difference]_
      - **Hint:** _[Student-friendly reflection]_
    #### Visibility Modifiers
      - **Difference:** _[Description of visibility change]_
      - **Hint:** _[Student-friendly reflection]_
    #### Other Structural Changes
      - **Difference:** _[General structural differences]_
      - **Hint:** _[General reflection]_

    **Provide only markdown output in the structured format above.**

    **Detected UML Differences:**
{END STEP3A USERPROMPT}

{BEGIN STEP3B SYSPROMPT}
You are assisting an educator in understanding UML differences. Provide structured insights in a structured format.
{END STEP3B SYSPROMPT}

{BEGIN STEP3B USERPROMPT}
Convert the following **UML differences** into **insights for the educator**.

    **Provide structured feedback:**
    - **Key Difference:** The core UML change.
    - **Possible Student Challenges:** Why the student might have made this mistake.

    **Use this structured markdown format:**
    #### Classes
      - **Difference:** _[Description of class difference]_
      - **Possible Student Challenge:** _[Why the student might have made this mistake]_
      - **Teaching Recommendation:** _[How to guide the student]_
    #### Attributes
      - **Difference:** _[Description of attribute difference]_
      - **Possible Student Challenge:** _[Why the student might have made this mistake]_
      - **Teaching Recommendation:** _[How to guide the student]_
    #### Methods - **Difference:** _[Description of method difference]_
      - **Possible Student Challenge:** _[Why the student might have made this mistake]_
      - **Teaching Recommendation:** _[How to guide the student]_
    #### Relations
      - **Difference:** _[Description of relationship difference]_
      - **Possible Student Challenge:** _[Why the student might have made this mistake]_
      - **Teaching Recommendation:** _[How to guide the student]_
    #### Visibility Modifiers
      - **Difference:** _[Description of visibility change]_
      - **Possible Student Challenge:** _[Why the student might have made this mistake]_
      - **Teaching Recommendation:** _[How to guide the student]_
    #### Other Structural Changes
      - **Difference:** _[General structural differences]_
      - **Possible Student Challenge:** _[Why the student might have made this mistake]_
      - **Teaching Recommendation:** _[How to guide the student]_

    **Provide only markdown output in the structured format above.**

    **Detected UML Differences:**
{END STEP3B USERPROMPT}
```

## ER Prompt Template

```
{BEGIN STEP1 SYSPROMPT}
You are an expert in ER diagram recognition. Convert the given ER diagram image to equivalent PlantUML code. Output only valid PlantUML code, nothing else.
{END STEP1 SYSPROMPT}

{BEGIN STEP1 USERPROMPT}

{END STEP1 USERPROMPT}

{BEGIN STEP2 SYSPROMPT}
You are an expert in ERD analysis. Provide only factual differences. Clearly show the difference between the instructor's and the student's ER diagrams.
{END STEP2 SYSPROMPT}

{BEGIN STEP2 USERPROMPT}
Compare the following ER diagrams written in PlantUML and **list only the differences**.
   
    - **The first ER diagram is the instructor's solution.**
    - **The second ER diagram is the student's solution.**
   
    **For each difference, clearly indicate what changed between the two solutions.**
   
    **Example output format:**
    - "Entity `Order` exists in the student solution but not in the instructor's solution."
    - "The relation between `Order` and `Customer` was changed in the student solution."

    **DO NOT** provide explanations, corrections, or suggestions—just factual differences.

    **Provide the output as a simple text list of bullet points.**

    **These are two ER diagrams written in PlantUML:**
{END STEP2 USERPROMPT}

{BEGIN STEP3A SYSPROMPT}
You are an assistant helping students reflect on ER designs. Offer neutral hints in a structured format.
{END STEP3A SYSPROMPT}

{BEGIN STEP3A USERPROMPT}
Convert the following **ERD differences** into **neutral, student-friendly feedback**.

    - **DO NOT** compare directly against the instructor's solution.
    - **DO NOT** say something is correct or incorrect.
    - **DO use soft, reflective language** like:
      - "Consider reviewing..."
      - "You may want to reflect on..."
      - "Think about how this change impacts the design..."

    **For each category, provide hints** in a structured format:
    - **Factual Difference:** The raw ERD difference.
    - **Student-Friendly Hint:** A suggestion or reflection prompt.

    **Use this structured Markdown format:**
    #### Entities
      - **Difference:** _[Description of class difference]_
      - **Hint:** _[Student-friendly reflection]_ 
    #### Relations
      - **Difference:** _[Description of attribute difference]_
      - **Hint:** _[Student-friendly reflection]_
    #### Other Structural Changes
      - **Difference:** _[General structural differences]_
      - **Hint:** _[General reflection]_

    **Provide only markdown output in the structured format above.**

    **Detected ERD Differences:**
{END STEP3A USERPROMPT}

{BEGIN STEP3B SYSPROMPT}
You are assisting an educator in understanding ERD differences. Provide structured insights in a structured format.
{END STEP3B SYSPROMPT}

{BEGIN STEP3B USERPROMPT}
Convert the following **ERD differences** into **insights for the educator**.

    **Provide structured feedback:**
    - **Key Difference:** The core ERD change.
    - **Possible Student Challenges:** Why the student might have made this mistake.

    **Use this structured markdown format:**
    #### Entities
      - **Difference:** _[Description of entity difference]_
      - **Possible Student Challenge:** _[Why the student might have made this mistake]_
      - **Teaching Recommendation:** _[How to guide the student]_
    #### Relations
      - **Difference:** _[Description of relationship difference]_
      - **Possible Student Challenge:** _[Why the student might have made this mistake]_
      - **Teaching Recommendation:** _[How to guide the student]_
    #### Other Structural Changes
      - **Difference:** _[General structural differences]_
      - **Possible Student Challenge:** _[Why the student might have made this mistake]_
      - **Teaching Recommendation:** _[How to guide the student]_

    **Provide only markdown output in the structured format above.**

    **Detected ERD Differences:**
{END STEP3B USERPROMPT}
```