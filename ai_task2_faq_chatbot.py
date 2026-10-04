"""
AI Task 2: AI-Based FAQ Chatbot - Horizon TechX
Topic: ShopEase (an online store)
NLP: NLTK (stemming) + TF-IDF + cosine similarity (scikit-learn)

Run in terminal:   python ai_task2_faq_chatbot.py
Run chat UI:       streamlit run ai_task2_faq_ui.py
"""
import re

from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Collect FAQs for the chosen topic
FAQS = [
    ("How can I track my order?",
     "Go to 'My Orders' and click 'Track'. You will also get tracking links by SMS and email."),
    ("What is your return policy?",
     "You can return most items within 7 days of delivery if they are unused and in original packaging."),
    ("How do I cancel my order?",
     "Open 'My Orders', select the item and tap 'Cancel'. Orders can be cancelled before they are shipped."),
    ("What payment methods do you accept?",
     "We accept credit/debit cards, UPI, net banking, wallets and cash on delivery."),
    ("How long does delivery take?",
     "Standard delivery takes 3-5 business days. Express delivery takes 1-2 business days."),
    ("How do I get a refund?",
     "Refunds are processed within 5-7 business days to your original payment method after we receive the returned item."),
    ("Do you offer cash on delivery?",
     "Yes, cash on delivery is available on orders up to Rs. 10,000 in most pin codes."),
    ("How do I reset my password?",
     "Click 'Forgot Password' on the login page and follow the link sent to your registered email."),
    ("How can I contact customer support?",
     "Email support@shopease.example or call 1800-000-000 between 9 AM and 9 PM, Monday to Saturday."),
    ("Is there a warranty on electronics?",
     "Yes, all electronics carry a manufacturer warranty of 1 year. Keep your invoice for claims."),
    ("Do you deliver internationally?",
     "Currently we deliver only within India. International shipping will be launched soon."),
    ("How do I apply a discount coupon?",
     "Enter the coupon code in the 'Apply Coupon' box at checkout and click Apply."),
    ("Can I change my delivery address?",
     "You can change the address before the order is shipped from the 'My Orders' page."),
    ("My item arrived damaged. What should I do?",
     "Sorry about that! Raise a complaint within 48 hours from 'My Orders' with a photo and we will replace or refund it."),
]

GREETINGS = {"hi", "hello", "hey", "good morning", "good evening"}
EXIT_WORDS = {"bye", "exit", "quit", "goodbye"}
THRESHOLD = 0.3  # minimum similarity to accept a match

# small built-in stopword list (no NLTK data download needed)
STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "was", "were", "be", "to", "of", "in",
    "on", "at", "for", "and", "or", "do", "does", "did", "you", "your", "i",
    "me", "my", "we", "it", "this", "that", "can", "how", "what", "please",
    "with", "have", "has", "will", "should", "take",
}
stemmer = PorterStemmer()

# map common user wording to the words used in the FAQs (intent matching help)
SYNONYMS = {
    "package": "order", "parcel": "order", "shipment": "order", "purchase": "order",
    "where": "track", "status": "track",
    "money": "refund", "reimbursement": "refund", "reimburse": "refund",
    "broken": "damaged", "defective": "damaged", "faulty": "damaged",
    "torn": "damaged", "cracked": "damaged",
    "upi": "payment", "gpay": "payment", "paytm": "payment", "pay": "payment",
    "card": "payment", "paying": "payment",
    "send back": "return", "exchange": "return",
    "shipping": "delivery", "deliver": "delivery", "delivered": "delivery", "arrive": "delivery",
    "arrival": "delivery",
    "login": "password", "signin": "password", "account": "password",
    "phone": "contact", "call": "contact", "help": "support", "agent": "support",
    "when": "long", "cod": "cash", "promo": "coupon", "voucher": "coupon", "code": "coupon",
    "guarantee": "warranty", "abroad": "internationally", "overseas": "internationally",
    "stop": "cancel",
}


def preprocess(text):
    """Lowercase, remove punctuation, tokenize, drop stopwords, stem."""
    text = text.lower().replace("send back", "return")
    tokens = re.findall(r"[a-z0-9]+", text)
    tokens = [SYNONYMS.get(t, t) for t in tokens]
    return " ".join(stemmer.stem(t) for t in tokens if t not in STOPWORDS)


class FAQChatbot:
    def __init__(self, faqs=FAQS):
        self.faqs = faqs
        self.vectorizer = TfidfVectorizer()
        # index the question (twice, for weight) plus its answer for richer matching
        cleaned = [preprocess(q) + " " + preprocess(q) + " " + preprocess(a) for q, a in faqs]
        self.faq_matrix = self.vectorizer.fit_transform(cleaned)

    def get_answer(self, query):
        """Return (answer, matched_question, score)."""
        text = query.strip().lower().rstrip("!?.")
        if text in GREETINGS:
            return "Hello! Ask me anything about orders, returns, payments or delivery.", None, 1.0
        if text in EXIT_WORDS:
            return "Goodbye! Happy shopping!", None, 1.0

        vec = self.vectorizer.transform([preprocess(query)])
        scores = cosine_similarity(vec, self.faq_matrix)[0]
        best = scores.argmax()

        if scores[best] < THRESHOLD:
            return ("Sorry, I couldn't find an answer to that. Try rephrasing, "
                    "or contact support@shopease.example."), None, float(scores[best])
        question, answer = self.faqs[best]
        return answer, question, float(scores[best])


def main():
    bot = FAQChatbot()
    print("ShopEase FAQ Bot: Hi! Ask me a question (type 'bye' to exit).")
    while True:
        query = input("You: ")
        if not query.strip():
            continue
        answer, matched, score = bot.get_answer(query)
        print(f"Bot: {answer}")
        if matched:
            print(f"     (matched FAQ: '{matched}', similarity {score:.2f})")
        if query.strip().lower().rstrip("!?.") in EXIT_WORDS:
            break


if __name__ == "__main__":
    main()
