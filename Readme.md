# Requirements 

Task: Create a API end point for loan inquiries. 

Django, Django REST framework needs to be used. 
Django Admin for all app Models.

Models:
1. Program - min and max loan amount, min and max age applicable age.
2. Borrower - ID number, DOB.
3. Inquiry - Program, Borrower, Loan Amount, Status (approved, rejected), reason for rejection.
4. List of Untrusted ID numbers

API INPUT: ID number and Amount.

Following things needs to be checked:
1. Check if the amount is within the min/max loan amount from the Program, (if not -> reject).
2. Check if the Age of the Borrower within the applicable range (Assign DOB -  based on first 6 numbers of ID (YYMMDD) are DOB), (if not -> reject).
3. Check if the individual is a Sole Proprietor (make API request to the Governmental service https://stat.gov.kz/api/juridical/gov/?bin={IDnumber}&lang=ru), (if yes -> reject). 
4. If in Untrusted List, (if yes -> reject).

OUTPUT: Approved or Rejected, reason. 
