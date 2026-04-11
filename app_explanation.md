# Understanding `app.py` (The Face of the Tool)

This file contains the code for the **User Interface (UI)**. In simple terms, this is the webpage that the user actually sees and interacts with. 

We built this using a tool called **Streamlit**, which is a magic wand for Python. Instead of using complex HTML code to build a website, Streamlit lets us build a website using just a few simple Python commands.

## How it Works, Step-by-Step

1. **The Look and Feel:** 
   At the very top of the file, we add some custom styles (CSS) to make the webpage look beautiful. We give it nice fonts, colorful gradient text, and rounded boxes to make it look like a premium, modern app instead of a boring college project.

2. **The Search Box:** 
   We create a simple input box (`st.text_input`) that asks the user: *"What kind of developer tool are you looking for?"* followed by a Search button.

3. **Connecting to the Brain (The AI):** 
   When the user clicks the "Search" button, `app.py` takes the text the user typed and sends it to the `run_pipeline` function (which lives over in the `simple_agent.py` file). While the AI is busy thinking and searching the web, this file displays a "Loading..." spinner so the user knows it's working.

4. **Displaying the Results:** 
   Once the AI finishes its job, `app.py` changes the loading spinner into a green checkmark. It then takes the final answer (the Top 3 Recommended Tools) and the AI Judge's Scores, and prints them beautifully on the screen using clean boxes and layout columns.
