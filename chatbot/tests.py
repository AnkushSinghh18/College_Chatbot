"""
STEP 7: Automated tests for the chatbot.

Run all of these with:
    python manage.py test

Django will create a temporary, throw-away test database, run every
test below, and delete it afterwards - your real db.sqlite3 is never
touched.

There are two kinds of tests here:

1. NLPTests       - test chatbot/nlp.py directly (intent + course
                     detection), with no database involved at all.
2. ChatbotViewTests - test the full flow: POST a question to
                     /get-response/ and check the reply that comes
                     back from the database-backed view.
"""

from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse

from . import nlp


class NLPTests(TestCase):
    """Unit tests for the keyword-based intent detector (Step 5)."""

    def test_greeting_intent(self):
        self.assertEqual(nlp.detect_intent("Hello there"), "greeting")

    def test_fees_intent(self):
        self.assertEqual(nlp.detect_intent("How much does BCA cost?"), "fees")

    def test_branches_intent(self):
        self.assertEqual(nlp.detect_intent("What branches are available?"), "branches")

    def test_eligibility_intent(self):
        self.assertEqual(nlp.detect_intent("What is the eligibility for BCA?"), "eligibility")

    def test_unknown_intent(self):
        self.assertEqual(nlp.detect_intent("asdkjqwoie randomtext"), "unknown")

    def test_course_detection_bca(self):
        self.assertEqual(nlp.detect_course("Does TCET have BCA?"), "BCA")

    def test_course_detection_btech(self):
        self.assertEqual(nlp.detect_course("What is the B.Tech fee?"), "B.Tech/B.E.")

    def test_course_detection_bvoc(self):
        self.assertEqual(nlp.detect_course("What are the B.Voc courses?"), "B.Voc")

    def test_course_detection_none(self):
        self.assertIsNone(nlp.detect_course("Where is the college located?"))


class ChatbotViewTests(TestCase):
    """
    End-to-end tests: send real questions to the /get-response/ endpoint
    and check the database-backed answer that comes back (Step 6).
    """

    @classmethod
    def setUpTestData(cls):
        # Load the same seed data used in the real app, into the test DB.
        call_command('seed_data')

    def setUp(self):
        self.client = Client()
        self.url = reverse('get_response')

    def ask(self, message):
        """Helper: POST a question and return the bot's text reply."""
        response = self.client.post(
            self.url,
            data={'message': message},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        return response.json()['response']

    # ---- The sample questions from the project brief ----

    def test_what_courses_does_tcet_offer(self):
        reply = self.ask("What courses does TCET offer?")
        self.assertIn("BCA", reply)
        self.assertIn("B.Tech/B.E.", reply)
        self.assertIn("B.Voc", reply)

    def test_what_btech_branches_are_available(self):
        reply = self.ask("What B.Tech branches are available?")
        self.assertIn("Computer Engineering", reply)

    def test_does_tcet_have_bca(self):
        reply = self.ask("Does TCET have BCA?")
        self.assertIn("BCA", reply)

    def test_what_is_the_bca_fee(self):
        reply = self.ask("What is the BCA fee?")
        self.assertIn("115000", reply.replace(",", ""))

    def test_how_much_does_btech_cost(self):
        reply = self.ask("How much does B.Tech cost?")
        self.assertIn("154000", reply.replace(",", ""))

    def test_what_are_the_bvoc_courses(self):
        reply = self.ask("What are the B.Voc courses?")
        self.assertIn("Data Analytics", reply)

    def test_eligibility_for_bca(self):
        reply = self.ask("What is the eligibility for BCA?")
        self.assertIn("Eligibility", reply)
        self.assertIn("BCA", reply)

    def test_eligibility_for_btech_is_not_bca_answer(self):
        # Regression test: this used to incorrectly return the BCA
        # eligibility answer for ANY course, including B.Tech.
        reply = self.ask("What is the admission criteria for B.Tech in TCET")
        self.assertIn("B.Tech", reply)
        self.assertNotIn("BCA", reply)

    def test_eligibility_for_bvoc(self):
        reply = self.ask("What is the eligibility for B.Voc?")
        self.assertIn("B.Voc", reply)
        self.assertNotIn("BCA", reply)

    def test_eligibility_without_course_asks_which_course(self):
        reply = self.ask("What is the eligibility?")
        self.assertIn("Which course", reply)

    def test_career_after_btech(self):
        reply = self.ask("What can I do after B.Tech?")
        self.assertIn("M.Tech", reply)

    def test_how_can_i_get_admission(self):
        reply = self.ask("How can I get admission?")
        self.assertIn("admission", reply.lower())

    def test_how_long_is_bca(self):
        reply = self.ask("How long is BCA?")
        self.assertIn("3 Years", reply)

    def test_does_tcet_have_a_library(self):
        reply = self.ask("Does TCET have a library?")
        self.assertIn("Library", reply)

    def test_does_tcet_have_sports_facilities(self):
        reply = self.ask("Does TCET have sports facilities?")
        self.assertIn("Sports", reply)

    def test_where_is_tcet_located(self):
        reply = self.ask("Where is TCET located?")
        self.assertIn("Kandivali", reply)

    def test_college_contact_number(self):
        reply = self.ask("What is the college contact number?")
        self.assertIn("6730", reply)

    def test_what_can_i_do_after_bca(self):
        reply = self.ask("What can I do after BCA?")
        self.assertIn("MCA", reply)

    def test_what_can_i_do_after_bvoc(self):
        reply = self.ask("What can I do after B.Voc?")
        self.assertIn("vocational", reply.lower())

    def test_greeting(self):
        reply = self.ask("Hi")
        self.assertIn("Hello", reply)

    def test_goodbye(self):
        reply = self.ask("Thank you, bye")
        self.assertIn("welcome", reply.lower())

    def test_unknown_question(self):
        reply = self.ask("asdkj qoweiqj random gibberish")
        self.assertIn("couldn't understand", reply)

    def test_conversation_is_logged_to_database(self):
        from .models import ChatMessage
        count_before = ChatMessage.objects.count()
        self.ask("What courses does TCET offer?")
        count_after = ChatMessage.objects.count()
        self.assertEqual(count_after, count_before + 1)
