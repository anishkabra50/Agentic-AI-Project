# Understanding the Setup Files (Config)

When building a software project, you always need a few small utility/setup files. These are not the main code, but they are essential for the project to run properly. Here is what each file does in simple terms:

## 1. `requirements.txt` (The Grocery List)
Think of this file as a recipe's ingredient list. Our code relies on tools built by other people (like Streamlit for the webpage, or Google's API for the AI). This file tells your computer exactly which tools it needs to download from the internet before it can run the program. 
(When we type `pip install -r requirements.txt`, the computer reads this grocery list and goes shopping).

## 2. `.env` and `.env.example` (The Locked Safe)
To use AI like Google Gemini or the Tavily web searcher, we have to create accounts and get secret passwords known as **API Keys**. 
* **`.env`**: This is a hidden file on your computer that acts like a locked safe holding your actual, private API keys. Our code opens this safe to get the keys when it runs. 
* **`.env.example`**: Since we don't want to upload our private `.env` safe to the public internet (GitHub), we upload `.env.example` instead. It’s an empty template that shows other people *how* to set up their own safe.

## 3. `.gitignore` (The "Do Not Touch" List)
When you upload your project to the internet using GitHub, you don't want to accidentally upload your secret passwords or temporary junk files that your computer created. This file acts as a bouncer. Any file name written inside `.gitignore` is permanently blocked from being uploaded to GitHub. This keeps our code clean and our passwords safe!
