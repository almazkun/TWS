from .models import LoanProgram, LoanBorrower, LoanInquiry


def create_new_borrower(IIN):
    obj = LoanBorrower(IIN=IIN)
    obj.dob_assignment()
    obj.save()
    
    
def create_new_inquiry(IIN, amount):
    inquiry_program = LoanProgram.objects.get(current_loan_program=True)
    create_new_borrower(IIN)
    inquiry_borrower = LoanBorrower.objects.get(IIN=IIN)
    obj = LoanInquiry(
        inquiry_program=inquiry_program, 
        inquiry_borrower=inquiry_borrower,
        inquiry_amount=amount)
    obj.save()
    
    
    
