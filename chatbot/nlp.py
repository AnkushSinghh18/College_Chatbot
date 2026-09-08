"""
STEP 5: Simple keyword-based NLP / intent detection.

This is intentionally NOT machine learning - it's plain Python string
matching. That's fine for a college project and it's easy to explain
in a viva:

    1. Lowercase the user's message.
    2. Check which keywords appear in it.
    3. Whichever intent has a matching keyword "wins".
    4. Separately, try to detect which course (BCA / B.Tech / B.Voc)
       the message is about, using another keyword list.

STEP 6 will take the (intent, course) this file returns and use it to
look up real data in the SQLite database (Course, Fee, Branch, FAQ, etc).
For now, this module can be used and tested completely on its own.
"""

# Each intent maps to a list of keywords/phrases that suggest that intent.
# Order matters a little: we check them in this order and the first
# intent with a keyword match wins.
INTENT_KEYWORDS = {
    "greeting": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"],
    "goodbye": ["bye", "goodbye", "see you", "thank you", "thanks"],
    "fees": ["fee", "fees", "cost", "price", "how much"],
    "branches": ["branch", "branches", "specialization", "specialisation"],
    "eligibility": ["eligibility", "eligible", "criteria", "qualify"],
    "admission": ["admission", "admissions", "apply", "application", "how can i get in", "enroll"],
    "duration": ["duration", "how long", "years", "length of course"],
    "career": ["career", "job", "after bca", "after b.voc", "after graduation", "scope"],
    "facilities": ["library", "sports", "facility", "facilities", "hostel", "wifi", "lab"],
    "contact": ["contact", "phone", "number", "email", "reach you"],
    "location": ["located", "location", "address", "where is"],
    "courses": ["course", "courses", "programme", "program", "offer"],
}

# Keywords used to detect which course the user is talking about.
COURSE_KEYWORDS = {
    "BCA": ["bca"],
    "B.Tech/B.E.": ["b.tech", "btech", "b.e.", "be ", "engineering"],
    "B.Voc": ["b.voc", "bvoc", "vocation", "vocational"],
}


def detect_intent(message):
    """
    Look at the user's message and return the best-matching intent
    as a string, e.g. "fees", "branches", "greeting", "unknown".
    """
    text = message.lower()

    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return intent

    return "unknown"


def detect_course(message):
    """
    Look at the user's message and return which course it refers to,
    e.g. "BCA", "B.Tech/B.E.", "B.Voc", or None if no course is mentioned.
    """
    text = message.lower()

    for course_name, keywords in COURSE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return course_name

    return None


def analyze_message(message):
    """
    Convenience function that returns both pieces of information
    together, e.g.:

        analyze_message("How much does BCA cost?")
        -> {"intent": "fees", "course": "BCA"}
    """
    return {
        "intent": detect_intent(message),
        "course": detect_course(message),
    }
