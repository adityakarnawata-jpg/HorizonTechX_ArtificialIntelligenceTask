"""Chat UI for the FAQ chatbot. Run: streamlit run ai_task2_faq_ui.py"""
import streamlit as st

from ai_task2_faq_chatbot import FAQS, FAQChatbot

st.set_page_config(page_title="ShopEase FAQ Bot", page_icon="🤖")
st.title("🤖 ShopEase FAQ Chatbot")
st.caption("Horizon TechX - AI Internship | Task 2")


@st.cache_resource
def load_bot():
    return FAQChatbot()


bot = load_bot()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me about orders, returns, payments or delivery."}
    ]

with st.sidebar:
    st.subheader("Sample questions")
    for q, _ in FAQS[:6]:
        st.write("•", q)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if query := st.chat_input("Type your question..."):
    st.session_state.messages.append({"role": "user", "content": query})
    answer, matched, score = bot.get_answer(query)
    if matched:
        answer += f"\n\n*Matched FAQ: {matched} (similarity {score:.2f})*"
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
