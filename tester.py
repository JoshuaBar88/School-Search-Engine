# ===============================
# AUTHORS: Joshua Barnett, Karly Disanto

# SUBMIT DATE: 12/04

# CLASS: AI

# PROF: JORGE
# ===============================



from preprocess import Cleaner
from crawlerFinal import Crawler
from retrieval import Retrive



crawl = Crawler("http://muhlenberg.edu")
clean = Cleaner(crawl.total, None)

print("Enter a query ")
query =  input()
queryClean = Cleaner(0,query)
final = queryClean.query
retrive = Retrive(final)



