from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from users.models import CustomUser

from .models import LoanProgram, LoanBorrower, LoanInquiry, Untrusted
from .utils import IIN_to_DOB

from .API_request import create_new_borrower, create_new_inquiry

class ModelsTest(TestCase):
    def setUp(self):

        self.loan_program_test = LoanProgram.objects.create(
            loan_program_name="test_program",
            loan_min=100,
            loan_max=999999,
            borrower_age_min=18,
            borrower_age_max=65,
            current_loan_program = True
        )
        self.loan_borrower_test = LoanBorrower.objects.create(
            IIN="000000100000",
            
        )
        
        self.loan_inquiry_test = LoanInquiry.objects.create(
            inquiry_program=self.loan_program_test,
            inquiry_borrower=self.loan_borrower_test,
            inquiry_amount=100,
        )

        self.untrusted_test = Untrusted.objects.create(
            untrusted_IIN=self.loan_borrower_test
        )
        
        self.test_iin = "020202300000"
        self.test_dob = "1902-02-02"
        self.test_amount = 500
        
        
    def test_model_creation(self):
        assert self.loan_program_test.loan_program_name == "test_program"
        assert self.loan_program_test.loan_min == 100
        assert self.loan_program_test.loan_max == 999999
        assert self.loan_program_test.borrower_age_min == 18
        assert self.loan_program_test.borrower_age_max == 65
        assert self.loan_program_test.current_loan_program == True

        assert self.loan_borrower_test.IIN == "000000100000"
        assert self.loan_borrower_test.dob == "0001-01-01"

        assert str(self.loan_inquiry_test.inquiry_program) == "test_program"
        assert str(self.loan_inquiry_test.inquiry_borrower) == "000000100000"
        assert self.loan_inquiry_test.inquiry_amount == 100
        assert self.loan_inquiry_test.inquiry_approved == False
        assert self.loan_inquiry_test.inquiry_rejected_because == "Not Applied Yet"

        assert str(self.untrusted_test) == "000000100000"


    def test_create_new_borrower(self):
        create_new_borrower(self.test_iin)
        self.test_create_new_borrower = LoanBorrower.objects.get(IIN=self.test_iin)
        
        assert self.test_create_new_borrower.IIN == self.test_iin
        assert str(self.test_create_new_borrower.dob) == self.test_dob
        
        
    def test_create_new_inquiry(self):
        create_new_inquiry(self.test_iin, self.test_amount)
        self.test_create_new_inquiry_obj = LoanInquiry.objects.get(pk=2)
        
        assert str(self.test_create_new_inquiry_obj.inquiry_program) == "test_program"
        assert str(self.test_create_new_inquiry_obj.inquiry_borrower) == self.test_iin
        assert self.test_create_new_inquiry_obj.inquiry_amount == self.test_amount
        

    def test_IIN_to_DOB(self):
        assert IIN_to_DOB("000000100000") == "1800-00-00"
        assert IIN_to_DOB("000000200000") == "1800-00-00"
        assert IIN_to_DOB("000000300000") == "1900-00-00"
        assert IIN_to_DOB("000000400000") == "1900-00-00"
        assert IIN_to_DOB("000000500000") == "2000-00-00"
        assert IIN_to_DOB("000000600000") == "2000-00-00"


class ValidationTest(TestCase):
    