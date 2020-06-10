from .models import LoanProgram, LoanBorrower, LoanInquiry


def create_new_borrower(IIN):
    try:
        obj = LoanBorrower(IIN=IIN)
        obj.dob_assignment()
        obj.save()
    except:
        pass
    
def create_new_inquiry(IIN, amount):
    inquiry_program = LoanProgram.objects.get(current_loan_program=True)
    create_new_borrower(IIN)
    inquiry_borrower = LoanBorrower.objects.get(IIN=IIN)

    obj = LoanInquiry(
        inquiry_program=inquiry_program, 
        inquiry_borrower=inquiry_borrower,
        inquiry_amount=int(amount))
    obj.inquiry_is_approved()
    obj.save()
    
    return {"status": obj.inquiry_approved, "msg": obj.inquiry_rejected_because}
