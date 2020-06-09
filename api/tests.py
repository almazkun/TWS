from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from users.models import CustomUser

from .models import LoanProgram, LoanBorrower, LoanInquiry, Untrusted


class ModelsTest(TestCase):
    def setUp(self):

        self.loan_program_test = LoanProgram.objects.create(
            loan_program_name="test_program",
            loan_min=100,
            loan_max=999999,
            borrower_age_min=18,
            borrower_age_max=65,
        )
        self.loan_borrower_test = LoanBorrower.objects.create(
            IIN="998877100200", dob="1999-12-31"
        )
        self.loan_inquiry_test = LoanInquiry.objects.create(
            inquiry_program=self.loan_program_test,
            inquiry_borrower=self.loan_borrower_test,
            inquiry_amount=100,
        )

        self.untrusted_test = Untrusted.objects.create(
            untrusted_IIN=self.loan_borrower_test
        )

    def test_model_creation(self):
        assert self.loan_program_test.loan_program_name == "test_program"
        assert self.loan_program_test.loan_min == 100
        assert self.loan_program_test.loan_max == 999999
        assert self.loan_program_test.borrower_age_min == 18
        assert self.loan_program_test.borrower_age_max == 65

        assert self.loan_borrower_test.IIN == "998877100200"
        assert self.loan_borrower_test.dob == "1999-12-31"

        assert str(self.loan_inquiry_test.inquiry_program) == "test_program"
        assert str(self.loan_inquiry_test.inquiry_borrower) == "998877100200"
        assert self.loan_inquiry_test.inquiry_amount == 100
        assert self.loan_inquiry_test.inquiry_approved == False
        assert self.loan_inquiry_test.inquiry_rejected_because == "Not Applied Yet"

        assert str(self.untrusted_test) == "998877100200"
