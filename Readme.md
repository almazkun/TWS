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

## Things to learn from that.
[from subreddit django](https://www.reddit.com/r/django/comments/h7cmvf/code_review_my_job_interview_assignment/)

* https://www.reddit.com/r/django/comments/h7cmvf/code_review_my_job_interview_assignment/ftrp6hv?utm_source=share&utm_medium=web2x
  - No tests against the actual api urls, coverage is probably low.

  - No use of model viewsets or model serializers.

  - Your django project and django apps aren't well separated. The urls layout is a bit off.

  - Some debugging code left over.

  - No tagged release.

  - External api should probably have had a client class.
  
 ```python
class GovAPI(object):
    base_url = "https://api.com"

    def __init__(self, version, api_key, api_secret):
        self.version = version
        self.client = requests.session()
        self.client.auth = (api_key, api_secret) 
        self.client.headers.update({'api-version': version})       

    def companies_list(self)
        return self.client.get(f"{self.base_url}/companies")

    def companies_detail(self, c_id)
        return self.client.get(f"{self.base_url}/companies/{c_id}")
```

* https://www.reddit.com/r/django/comments/h7cmvf/code_review_my_job_interview_assignment/fukpe2g?utm_source=share&utm_medium=web2x

I've done a good deal of Django and DRF and I've taken a look at your source. I can immediately tell you are not familiar with the idioms. Not sure if this was expected or not.

However a few things that I noticed:

    Code organization is really bad. The top level directories of api, drfx, users are apps I assume. What is drfx? Why is it different than api?

    Inside your API directory you have a file called API_request.py. The naming is off (the word API is in all capitals). Also what is the actual file for? No comments. Just basically two methods with parameters that are in all caps. Line 9 you are doing a global catch for exceptions and just ignoring them. Not even bubbling it up or letting Python handle the exception for you.

    Your models are not very polished. For example the date of birth field: https://github.com/almazkun/TWS/blob/master/api/models.py#L56 Why not allow it to be nullable? You have a default of "0001-01-01" which seems a bit weird.

    You have Christmas tree if/else nesting going on here: https://github.com/almazkun/TWS/blob/master/api/models.py#L124 This is generally a bad code smell. The nesting is really deep (generally I don't like more than 2 or 3 levels if I can help it)

    I'm glad you have tests. However for me the bar for senior level code would be something that is autogenerated and test cases that are covering multiple scenarios. For example the use of FactoryBoy or something similar. Even fixtures wouldn't be terrible but I'd expect you to justify it. I don't see any tests that hit the API endpoint using the Django's test client or something along those lines.

Hopefully this doesn't come off as too harsh but just trying to point out areas that a more senior developer might see and thus disqualify you from just the code sample you provided.


* https://www.reddit.com/r/django/comments/h7cmvf/code_review_my_job_interview_assignment/fulill4?utm_source=share&utm_medium=web2x

Idioms aren't a specific thing, so I suspect your googling won't help. /u/zemmekkis means "the way things are usually done". You want to do things in a consistent way that other Django developers will recognise, so they don't have to spend time figuring out things that seem unfamiliar.

- You could become familiar with PEP 8: The Style Guide for Python Code.

- And then there's the Django coding style.

- But more generally, look at the code written by other people and note the things that are often done in similar ways. The names people use for common files, class names, variable names, etc. The similar ways of structuring projects, apps, files. How do they write comments and tests?

Also, aim to be consistent in how you do things yourself. It really helps -- it makes it much easier to find things, to work out what they do when you return to them, to search and replace...

Once you start deviating from things that -- to experienced devs -- are common ways of doing things, and being inconsistent, it indicates there might be more serious problems with your code.

* https://www.reddit.com/r/django/comments/h7cmvf/code_review_my_job_interview_assignment/fukuzuf?utm_source=share&utm_medium=web2x

Read PEP 8.
