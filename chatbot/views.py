import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from . import nlp
from .models import Course, Fee, FAQ, Facility, Contact, ChatMessage


def chat_page(request):
    """Renders the chatbot UI (chat.html)."""
    return render(request, 'chat.html')


# ---------------------------------------------------------------------
# STEP 6: Helper functions that turn (intent, course) into a real
# answer by querying the SQLite database. Each function is small and
# focused on one intent, which makes it easy to explain in a viva:
# "for the 'fees' intent, we look up the Fee table for that course".
# ---------------------------------------------------------------------

def get_courses_response():
    courses = Course.objects.all()
    if not courses:
        return "Sorry, course information is not available right now."
    lines = [f"- {c.name} ({c.degree}, {c.duration})" for c in courses]
    return "TCET offers the following courses:\n" + "\n".join(lines)


def get_branches_response(course_name):
    if course_name is None:
        return "Please tell me which course - for example, 'What B.Tech branches are available?'"
    try:
        course = Course.objects.get(name=course_name)
    except Course.DoesNotExist:
        return f"Sorry, I don't have branch information for {course_name}."

    branches = course.branches.all()
    if not branches:
        return f"{course_name} does not have separate branches."
    lines = [f"- {b.name}" for b in branches]
    return f"{course_name} branches:\n" + "\n".join(lines)


def get_fees_response(course_name):
    if course_name is None:
        fees = Fee.objects.select_related('course').all()
        if not fees:
            return "Sorry, fee information is not available right now."
        lines = []
        for f in fees:
            extra = f" + Rs.{f.additional_fee:.0f} additional" if f.additional_fee else ""
            lines.append(f"- {f.course.name}: Rs.{f.amount:.0f}{extra} ({f.academic_year})")
        return "Current fees:\n" + "\n".join(lines)

    try:
        course = Course.objects.get(name=course_name)
    except Course.DoesNotExist:
        return f"Sorry, I don't have fee information for {course_name}."

    fee = course.fees.order_by('-academic_year').first()
    if not fee:
        return f"Sorry, fee information for {course_name} is not available yet."
    extra = f" + Rs.{fee.additional_fee:.0f} additional fee" if fee.additional_fee else ""
    return f"The {course_name} fee for {fee.academic_year} is Rs.{fee.amount:.0f}{extra}."


def get_duration_response(course_name):
    if course_name is None:
        return "Please tell me which course, e.g. 'How long is BCA?'"
    try:
        course = Course.objects.get(name=course_name)
    except Course.DoesNotExist:
        return f"Sorry, I don't have duration information for {course_name}."
    return f"{course_name} is a {course.duration} programme."


def _find_course_specific_faq(intent, course_name):
    """Look for an FAQ of this intent whose question mentions the given
    course. Returns the answer text, or None if no matching FAQ exists -
    NEVER falls back to a different course's answer, since that would
    be misleading (e.g. returning BCA's eligibility for a B.Tech question)."""
    faqs = FAQ.objects.filter(intent=intent)
    short_name = course_name.split('/')[0]  # "B.Tech/B.E." -> "B.Tech"
    for f in faqs:
        if short_name.lower() in f.question.lower() or course_name.lower() in f.question.lower():
            return f.answer
    return None


def get_eligibility_response(course_name):
    if course_name is None:
        return "Which course's eligibility would you like to know - BCA, B.Tech/B.E., or B.Voc?"
    answer = _find_course_specific_faq('eligibility', course_name)
    if answer:
        return answer
    return (f"Sorry, I don't have specific eligibility details for {course_name} yet. "
            f"Please check https://admission.tcetmumbai.in for the current requirements.")


def get_career_response(course_name):
    if course_name is None:
        return "Which course are you asking about - BCA, B.Tech/B.E., or B.Voc? I can tell you the career options after that."
    answer = _find_course_specific_faq('career', course_name)
    if answer:
        return answer
    return f"Sorry, I don't have specific career details for {course_name} yet."


def get_admission_response():
    """Admission process is the same general process regardless of
    course, so this doesn't need a course to be specified."""
    faq = FAQ.objects.filter(intent='admission').first()
    if faq:
        return faq.answer
    return "Sorry, admission process information is not available right now."


def get_facilities_response(message):
    facilities = Facility.objects.all()
    if not facilities:
        return "Sorry, facility information is not available."

    text = message.lower()
    for f in facilities:
        for word in f.name.lower().split():
            if len(word) > 3 and word in text:
                return f"{f.name}: {f.description}"

    lines = [f"- {f.name}" for f in facilities]
    return "TCET facilities include:\n" + "\n".join(lines)


def get_contact_response():
    contact = Contact.objects.first()
    if not contact:
        return "Sorry, contact information is not available."
    return f"You can contact the {contact.department} at {contact.phone} or {contact.email}."


def get_location_response():
    contact = Contact.objects.first()
    if not contact or not contact.address:
        return "Sorry, location information is not available."
    return f"TCET is located at: {contact.address}"


UNKNOWN_RESPONSE = ("I'm sorry, I couldn't understand that. You can ask me about "
                     "courses, branches, fees, admissions, eligibility, facilities "
                     "or contact information.")


def build_response(message, intent, course):
    """
    STEP 6: This is the piece that connects NLP output to the database.
    Given the intent detected by nlp.py (and the course, if any was
    mentioned), it decides which helper function above to call.
    """
    if intent == "greeting":
        return "Hello! Ask me about courses, branches, fees, admissions, eligibility, facilities or contact info."

    if intent == "goodbye":
        return "You're welcome! All the best with your admission to TCET."

    if intent == "unknown":
        # Fallback: e.g. "Does TCET have BCA?" doesn't match a keyword
        # above, but it DOES mention a course - so treat it as a
        # "courses" question about that specific course.
        if course:
            return f"Yes, TCET offers {course}. Ask me about its branches, fees, eligibility or duration for more details."
        return UNKNOWN_RESPONSE

    if intent == "courses":
        return get_courses_response()

    if intent == "branches":
        return get_branches_response(course)

    if intent == "fees":
        return get_fees_response(course)

    if intent == "duration":
        return get_duration_response(course)

    if intent == "eligibility":
        return get_eligibility_response(course)

    if intent == "career":
        return get_career_response(course)

    if intent == "admission":
        return get_admission_response()

    if intent == "facilities":
        return get_facilities_response(message)

    if intent == "contact":
        return get_contact_response()

    if intent == "location":
        return get_location_response()

    return UNKNOWN_RESPONSE


@require_POST
def get_response(request):
    """Receives a user's message as JSON, runs it through nlp.py to
    detect intent + course, builds a real database-backed answer, logs
    the conversation, and returns the answer as JSON."""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'response': "Sorry, I couldn't read that message."}, status=400)

    if not user_message:
        return JsonResponse({'response': "Please type a question."}, status=400)

    result = nlp.analyze_message(user_message)
    intent = result['intent']
    course = result['course']

    bot_response = build_response(user_message, intent, course)

    # Log every conversation turn to the database (ChatMessage table)
    ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)

    return JsonResponse({'response': bot_response, 'intent': intent, 'course': course})
