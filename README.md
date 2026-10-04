# HorizonTechX_ArtificialIntelligenceTask
This project consists of two Python-based AI applications developed as part of the Horizon TechX AI Internship, demonstrating practical implementation of Python programming, Natural Language Processing (NLP), interactive web application development, and external service integration using Streamlit.
Projects

Task 1 -- Translator --- Streamlit translation interface using
deep-translator / GoogleTranslator.

Task 2 -- ShopEase FAQ Chatbot --- Streamlit FAQ chatbot using
the project's FAQChatbot, NLTK PorterStemmer, and scikit-learn
TfidfVectorizer.

Project structure

Horizon-TechX-Tasks:
1. ai_task1_translator.py
2. ai_task2_faq_chatbot.py
3. ai_task2_faq_ui.py

ai_task2_faq_chatbot.py and ai_task2_faq_ui.py must be in the same
folder.

Requirements

Python 3.x

VS Code

Internet connection for Task 1's external translation service

Packages:

streamlit

deep-translator

nltk

scikit-learn

Install:

python -m pip install streamlit deep-translator nltk scikit-learn

If VS Code uses a specific interpreter, use that executable, e.g.:

C:\python314\python.exe -m pip install streamlit deep-translator nltk scikit-learn

Run Task 1 -- Translator

python -m streamlit run ai_task1_translator.py

Open http://localhost:8501.

Use it by selecting From, selecting To, entering text, and
clicking Translate.

Task 1 limitation

The translator depends on an external service through deep-translator.
A server/rate-limit error can occur when too many requests are made.
Wait and retry rather than repeatedly clicking Translate.

Run Task 2 -- ShopEase FAQ Chatbot

Make sure these files are together:

ai_task2_faq_chatbot.py
ai_task2_faq_ui.py

Run:

python -m streamlit run ai_task2_faq_ui.py

Open http://localhost:8501.

Enter a ShopEase-related FAQ question in the chatbot interface and
submit it.

Important

Do not launch these Streamlit apps using the normal Python-file run
command. Prefer:

python -m streamlit run ai_task1_translator.py
python -m streamlit run ai_task2_faq_ui.py

Common errors

Error                                      Fix

No module named 'streamlit'              python -m pip install streamlit

No module named 'deep_translator'        python -m pip install deep-translator

No module named 'nltk'                   python -m pip install nltk

No module named 'sklearn'                python -m pip install scikit-learn

No module named 'ai_task2_faq_chatbot'   Keep both Task 2 .py files in the same
folder

cd Downloads path error                  Use the full project path,
e.g. cd "C:\Users\<username>\Downloads"

Translation server/rate-limit error        Wait and retry later

Stop an app

In the running Streamlit terminal, press Ctrl + C.
