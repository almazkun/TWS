from django.db import models

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

    created_on = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name="Updated", auto_now=True)

    class Meta:
        verbose_name = "Loan Program"
        verbose_name_plural = "Loan Programs"
        ordering = ["created_on"]

    def __str__(self):
        return str(self.loan_program_name)


class LoanBorrower(models.Model):
    IIN = models.CharField(
        verbose_name="Individual Identification Number", max_length=12
    )
    dob = models.DateField(verbose_name="Date of Birth")

    created_on = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name="Updated", auto_now=True)

    class Meta:
        verbose_name = "IIN"
        verbose_name_plural = "IINs"
        ordering = ["created_on"]

    def __str__(self):
        return str(self.IIN)


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
