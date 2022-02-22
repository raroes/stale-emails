# Scientific email addresses going stale

Author: Raul Rodriguez-Esteban

Reference: Rodriguez-Esteban R, Vishnyakova D, Rinaldi F. Revisiting the decay of scientific email addresses. J Assoc Inf Sci Technol. 2021;1-4.

Paper link: https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24545

Scripts and methods used for the analysis of stale emails in the MEDLINE database

* *bounce_model.ipynb*: log-likelihood solution of the Bernoulli model

* *classify_email_addresses.py*: counts the number of new email addresses in MEDLINE per year and the number that belong to free email providers

* *count_medline_emails.py*: counts the number of new email addresses in MEDLINE per year

* *estimate_number_of_stale_emails.py*: using a Bernoulli process with a linearly time-dependent parameter this script estimates the number of email addresses that are invalid in MEDLINE
