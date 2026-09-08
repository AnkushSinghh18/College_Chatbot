"""
STEP 3: Seed the database with initial TCET data.

Run with:
    python manage.py seed_data

This is a Django "management command" - a simple, safe, repeatable way
to load starter data without manually typing it into the admin panel.
It is safe to run more than once; it clears old data first so you
don't end up with duplicates.

IMPORTANT (read before your viva / before submitting):
The fee amounts and branch list below are based on the figures you
gave me. Please double check the current, official numbers on
https://www.tcetmumbai.in and https://admission.tcetmumbai.in and
update them in the Admin Panel if they've changed - college fees and
the exact branch list can change every admission cycle.
"""

from django.core.management.base import BaseCommand
from chatbot.models import Course, Branch, Fee, FAQ, Facility, Contact


class Command(BaseCommand):
    help = "Seed the database with initial TCET course, fee, facility and FAQ data"

    def handle(self, *args, **options):
        # ---- Clear old data so re-running this command doesn't duplicate rows ----
        Branch.objects.all().delete()
        Fee.objects.all().delete()
        Course.objects.all().delete()
        FAQ.objects.all().delete()
        Facility.objects.all().delete()
        Contact.objects.all().delete()

        # ---------------------------------------------------------------
        # COURSES
        # ---------------------------------------------------------------
        bca = Course.objects.create(
            name="BCA",
            degree="Bachelor of Computer Applications",
            duration="3 Years",
            description="An undergraduate computer applications programme focused on "
                         "programming, software development and computer fundamentals.",
        )

        btech = Course.objects.create(
            name="B.Tech/B.E.",
            degree="Bachelor of Engineering / Bachelor of Technology",
            duration="4 Years",
            description="An undergraduate engineering programme affiliated to the "
                         "University of Mumbai, offered across multiple branches.",
        )

        bvoc = Course.objects.create(
            name="B.Voc",
            degree="Bachelor of Vocation",
            duration="3 Years",
            description="A skill-based undergraduate programme that combines "
                         "academic learning with hands-on vocational training.",
        )

        # ---------------------------------------------------------------
        # BRANCHES
        # ---------------------------------------------------------------
        btech_branches = [
            "Computer Engineering",
            "Information Technology",
            "Electronics & Tele-Communication",
            "Electronics and Computer Science",
            "Mechanical Engineering",
            "Civil Engineering",
            "Artificial Intelligence & Machine Learning",
            "Artificial Intelligence & Data Science",
            "Computer Science & Engineering (IoT)",
            "Computer Science & Engineering (Cyber Security)",
            "Mechanical & Mechatronics Engineering (Additive Manufacturing)",
        ]
        for branch_name in btech_branches:
            Branch.objects.create(course=btech, name=branch_name)

        bvoc_branches = [
            "Animation & Graphic Design",
            "Artificial Intelligence & Data Science",
            "Software Development",
            "Data Analytics",
        ]
        for branch_name in bvoc_branches:
            Branch.objects.create(course=bvoc, name=branch_name)

        # ---------------------------------------------------------------
        # FEES (academic year 2026-27 - VERIFY against the official site)
        # ---------------------------------------------------------------
        Fee.objects.create(course=bca, amount=115000, additional_fee=0, academic_year="2026-27")
        Fee.objects.create(course=btech, amount=154000, additional_fee=0, academic_year="2026-27")
        Fee.objects.create(course=bvoc, amount=130000, additional_fee=3000, academic_year="2026-27")

        # ---------------------------------------------------------------
        # FACILITIES
        # ---------------------------------------------------------------
        facilities = [
            ("Library", "A well-stocked central library with textbooks, journals and digital resources."),
            ("Sports Facilities", "Indoor and outdoor sports facilities for student recreation and fitness."),
            ("Hostel", "Separate hostel accommodation available for male and female students."),
            ("Computer Labs", "Well-equipped computer and engineering labs across departments."),
            ("Wi-Fi Campus", "Campus-wide Wi-Fi connectivity for students and staff."),
        ]
        for name, desc in facilities:
            Facility.objects.create(name=name, description=desc)

        # ---------------------------------------------------------------
        # CONTACT
        # ---------------------------------------------------------------
        Contact.objects.create(
            department="Admission Office",
            phone="+91-22-6730 8000",
            email="info@tcetmumbai.in",
            address="A-Block, Thakur Educational Campus, Shyamnarayan Thakur Marg, "
                    "Thakur Village, Kandivali (East), Mumbai - 400101, Maharashtra.",
        )

        # ---------------------------------------------------------------
        # FAQs (for intents that aren't simple DB lookups)
        # ---------------------------------------------------------------
        faqs = [
            (
                "What is the eligibility for BCA?",
                "Eligibility for BCA generally requires passing 10+2 (HSC) or an equivalent "
                "examination. Please check the official admission site for the exact "
                "subject and percentage requirements for the current year.",
                "eligibility",
            ),
            (
                "What is the eligibility for B.Tech/B.E.?",
                "Eligibility for B.Tech/B.E. generally requires passing 10+2 (HSC) with "
                "Physics and Mathematics as compulsory subjects (along with Chemistry, "
                "Biology, Biotechnology or a Technical/Vocational subject), with a minimum "
                "aggregate percentage as set by DTE Maharashtra, OR a Diploma in "
                "Engineering with the required minimum percentage for lateral entry. "
                "Please check the official admission site for the exact current requirements.",
                "eligibility",
            ),
            (
                "What is the eligibility for B.Voc?",
                "Eligibility for B.Voc generally requires passing 10+2 (HSC) or an "
                "equivalent examination in any stream. Please check the official "
                "admission site for the exact current requirements.",
                "eligibility",
            ),
            (
                "How can I get admission?",
                "Admission at TCET is done through the relevant entrance exam/counselling "
                "process (such as MHT-CET for BCA/B.Tech, or the applicable CAP round), "
                "followed by document verification. Visit "
                "https://admission.tcetmumbai.in for the current admission process and dates.",
                "admission",
            ),
            (
                "What can I do after BCA?",
                "After completing BCA, students commonly pursue further studies such as "
                "an MCA or MBA, or start careers in software development, web development, "
                "IT support, or data-related roles.",
                "career",
            ),
            (
                "What can I do after B.Tech/B.E.?",
                "After completing B.Tech/B.E., students commonly pursue an M.Tech/M.E., "
                "an MBA, prepare for competitive/PSU exams, or start careers as engineers "
                "in their branch's industry.",
                "career",
            ),
            (
                "What can I do after B.Voc?",
                "After completing a B.Voc programme, students can pursue further vocational "
                "or academic studies, or start industry careers directly related to their "
                "chosen specialization (e.g. software development, data analytics, "
                "animation & graphic design).",
                "career",
            ),
        ]
        for question, answer, intent in faqs:
            FAQ.objects.create(question=question, answer=answer, intent=intent)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with TCET data."))
