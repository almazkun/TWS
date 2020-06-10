from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from users.models import CustomUser

from .models import LoanProgram, LoanBorrower, LoanInquiry, Untrusted
from .utils import IIN_to_DOB, calculate_age

from .API_request import create_new_borrower, create_new_inquiry

class ModelsTest(TestCase):
    def setUp(self):

        self.test_iin = "020202300000"
        self.test_dob = "1902-02-02"
        self.test_amount = 500
        
        self.loan_program_test = LoanProgram.objects.create(
            loan_program_name="test_program",
            loan_min=100,
            loan_max=999999,
            borrower_age_min=18,
            borrower_age_max=65,
            current_loan_program = True
        )
        self.loan_borrower_test = LoanBorrower.objects.create(
            IIN=self.test_iin,
            
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
        assert self.loan_program_test.current_loan_program == True

        assert self.loan_borrower_test.IIN == self.test_iin
        assert self.loan_borrower_test.dob == "0001-01-01"

        assert str(self.loan_inquiry_test.inquiry_program) == "test_program"
        assert str(self.loan_inquiry_test.inquiry_borrower) == self.test_iin
        assert self.loan_inquiry_test.inquiry_amount == 100
        assert self.loan_inquiry_test.inquiry_approved == False
        assert self.loan_inquiry_test.inquiry_rejected_because == "Not Applied Yet"

        assert str(self.untrusted_test) == self.test_iin


    def test_create_new_borrower(self):
        self.test_iin = "9912313100200"
        self.test_dob = "1999-12-31"
        create_new_borrower(self.test_iin)
        self.test_create_new_borrower = LoanBorrower.objects.get(IIN=self.test_iin)
        
        assert self.test_create_new_borrower.IIN == self.test_iin
        assert str(self.test_create_new_borrower.dob) == self.test_dob
        
        
    def test_create_new_inquiry(self):
        self.test_iin = "8812313100200"
        self.test_dob = "1988-12-31"
        create_new_inquiry(self.test_iin, self.test_amount)
        self.test_create_new_inquiry_obj = LoanInquiry.objects.get(pk=2)
        
        assert str(self.test_create_new_inquiry_obj.inquiry_program) == "test_program"
        assert str(self.test_create_new_inquiry_obj.inquiry_borrower) == self.test_iin
        assert self.test_create_new_inquiry_obj.inquiry_amount == self.test_amount
        
        methods_IIN = "7712313100200"
        methods_amount = 500
        request = create_new_inquiry(methods_IIN, methods_amount)

        assert request == {"status": True, "msg": "Approved!"}

    def test_IIN_to_DOB(self):
        assert IIN_to_DOB("000000100000") == "1800-00-00"
        assert IIN_to_DOB("000000200000") == "1800-00-00"
        assert IIN_to_DOB("000000300000") == "1900-00-00"
        assert IIN_to_DOB("000000400000") == "1900-00-00"
        assert IIN_to_DOB("000000500000") == "2000-00-00"
        assert IIN_to_DOB("000000600000") == "2000-00-00"
        
        
    def test_calculate_age(self):
        assert calculate_age("1800-01-01") == 220
        assert calculate_age("1899-01-01") == 121
        assert calculate_age("1999-01-01") == 21
        assert calculate_age("2000-01-01") == 20
        assert calculate_age("2010-01-01") == 10
        assert calculate_age("2020-01-01") == 0
        assert calculate_age("2002-06-08") == 18
        assert calculate_age("2002-06-09") == 18
        assert calculate_age("2002-06-10") == 18
        assert calculate_age("2002-06-11") == 17


    def test_models_methods(self):
        methods_IIN = "7712313100200000"
        methods_amount = 500
        create_new_inquiry(methods_IIN, methods_amount)
        self.test_models_methods = LoanInquiry.objects.get(pk=2)
        
        #ULB = LoanBorrower.objects.get(IIN=methods_IIN)
        #untrusted_object = Untrusted.objects.create(untrusted_IIN=ULB)
    
        
        assert str(self.test_models_methods.inquiry_program) == "test_program"
        assert str(self.test_models_methods.inquiry_borrower) == methods_IIN
        assert self.test_models_methods.inquiry_amount == methods_amount
        assert self.test_models_methods.amount_is_valid() == True
        assert self.test_models_methods.age_is_valid() == True
        assert self.test_models_methods.IIN_is_a_business() == False
        assert self.test_models_methods.IIN_is_untrusted() == False
        
        self.test_models_methods.inquiry_is_approved()
        assert self.test_models_methods.inquiry_approved == True
        assert self.test_models_methods.inquiry_rejected_because == "Approved!"
       