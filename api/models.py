from django.db import models
from django.db.models.query_utils import Q


from .utils import IIN_to_DOB

# Create your models here.
class LoanProgram(models.Model):
    loan_program_name = models.CharField(verbose_name="Program name", max_length=100)
    loan_min = models.PositiveIntegerField(
        verbose_name="Lowest Loan Possible", default=0
    )
    loan_max = models.PositiveIntegerField(
        verbose_name="Highest Loan Possible", default=0
    )
    borrower_age_min = models.PositiveIntegerField(
        verbose_name="Youngest Possible", default=0
    )
    borrower_age_max = models.PositiveIntegerField(
        verbose_name="Oldest Possible", default=0
    )

    current_loan_program = models.BooleanField(verbose_name="Current loan program", default=False)
    
    created_on = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name="Updated", auto_now=True)

    class Meta:
        verbose_name = "Loan Program"
        verbose_name_plural = "Loan Programs"
        ordering = ["created_on"]
        
        constraints = [
            models.UniqueConstraint(fields=['current_loan_program'], condition=Q(current_loan_program=True), name='unique_current_loan_program')
        ]

    def __str__(self):
        return str(self.loan_program_name)


class LoanBorrower(models.Model):
    IIN = models.CharField(
        verbose_name="Individual Identification Number", max_length=12
    )
    dob = models.DateField(verbose_name="Date of Birth", default="0001-01-01")

    created_on = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name="Updated", auto_now=True)

    class Meta:
        verbose_name = "IIN"
        verbose_name_plural = "IINs"
        ordering = ["created_on"]

    def __str__(self):
        return str(self.IIN)
    
    def dob_assignment(self):
        self.dob = IIN_to_DOB(self.IIN)


class LoanInquiry(models.Model):
    inquiry_program = models.ForeignKey(LoanProgram, on_delete=models.CASCADE)
    inquiry_borrower = models.ForeignKey(LoanBorrower, on_delete=models.CASCADE)
    inquiry_amount = models.IntegerField()
    inquiry_approved = models.BooleanField(default=False)
    inquiry_rejected_because = models.CharField(
        default="Not Applied Yet", max_length=100
    )

    created_on = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name="Updated", auto_now=True)

    
    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"
        ordering = ["created_on"]

    
    def __str__(self):
        return str(self.id)
    
    
    def amount_is_valid(self):
        if self.inquiry_program.loan_min <= self.inquiry_amount <= self.inquiry_program.loan_max:
            return True
        return False
    
    
    def inquiry_is_approved(self):
        if self.amount_is_valid():
            self.inquiry_approved = True
            self.inquiry_rejected_because = ""
        else:
            self.inquiry_rejected_because = "Error, Amount is incorrect"

        
    


class Untrusted(models.Model):
    untrusted_IIN = models.ForeignKey(LoanBorrower, on_delete=models.CASCADE)

    created_on = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name="Updated", auto_now=True)

    class Meta:
        verbose_name = "Untrusted person"
        verbose_name_plural = "Untrusted people"
        ordering = ["created_on"]

    def __str__(self):
        return str(self.untrusted_IIN)
