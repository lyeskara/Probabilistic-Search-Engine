'''
1. implement the lossy dictionary compression techniques for the first two columns of Table 5.1 in the textbook
and compile a similar table for Reuters-21578. (Remember that your corpus is much smaller than the
Reuters corpus used for Table 5.1.) Are the changes similar? Discuss your findings.

1- lossy compression for table 5.1 and similar table for reuters corpus. compare changes and discuss findings

2. compare retrieval results for your three sample queries of Subproject II when you run them on your
compressed index. Discuss your findings in the Project Report

run queries again. and compare

'''
from utilityFunctions import load_index, write_index
from nltk.corpus import stopwords
from nltk import PorterStemmer
import re


def compressionByLowercasing(index: dict):
    compressed_indexByLowercasing = {}
    # Iterate through the original dictionary
    for term, postings in index.items():
        # Apply lowercasing to the term
        term_lower = term.lower()

        # Check if the lowercase term exists in the collapsed dictionary
        if term_lower in compressed_indexByLowercasing:
            # Append the postings list to the existing one
            compressed_indexByLowercasing[term_lower].extend(postings)
        else:
            # Create a new entry with the lowercase term and its postings list
            compressed_indexByLowercasing[term_lower] = postings

    for term, postings in compressed_indexByLowercasing.items():
        compressed_indexByLowercasing[term] = sorted(list(set(postings)))
    return compressed_indexByLowercasing


def compressionByStemming(index: dict, stemmer: PorterStemmer):
    compressed_indexByStemming = {}

    for term, postings in index.items():
        stemmed_term = stemmer.stem(term)
        if stemmed_term in compressed_indexByStemming:
            compressed_indexByStemming[stemmed_term].extend(postings)
        else:
            compressed_indexByStemming[stemmed_term] = postings
    for term, postings in compressed_indexByStemming.items():
        compressed_indexByStemming[term] = sorted(list(set(postings)))
    return compressed_indexByStemming


def compressionByNumberRemoval(index: dict):
    compressed_indexByNumberRemoval = {}

    for term, postings in index.items():
        if re.match(r'^[a-zA-Z]+$', term):
                compressed_indexByNumberRemoval[term] = postings

    return compressed_indexByNumberRemoval


def compressionByThirtySW(index: dict, thirtyList: []):
    compressed_indexByThirtySW = {}

    for term, postings in index.items():
        if term not in thirtyList:
                compressed_indexByThirtySW[term] = postings
                
    return compressed_indexByThirtySW


def compressionByOneFiftySW(index: dict, onefiftyList: []):
    compressed_indexByOneFiftySW = {}

    for term, postings in index.items():
        if term not in onefiftyList:
                compressed_indexByOneFiftySW[term] = postings
        
    return compressed_indexByOneFiftySW


def countPostings(postingsList):
    postings = 0
    for plist in postingsList:
        postings += len(plist)
    return postings

def sizeComparaison(index_name, previous_index_name,prev_dict, prev_pcount, curr_dict, curr_pcount, unfiltered_dict, unfiltered_pcount):
    
    print(f"{index_name} vs {previous_index_name}:")
    print(f"Current Dictionary Length: {len(curr_dict)}", end=" ")
    print(f"Previous Dictionary Length: {len(prev_dict)}")
    print(f"Negative Difference in Length (Current - Previous): {-(len(prev_dict) - len(curr_dict))}")
    print(f"Current Postings Length: {curr_pcount}", end=" ")
    print(f"Previous Postings Length: {prev_pcount}")
    print(f"Negative Difference in Length (Current - Previous): {-(prev_pcount - curr_pcount)}\n")
    
    print(f"{index_name} vs. Unfiltered:")
    print(f"Current Dictionary Length: {len(curr_dict)}", end=" ")
    print(f"Unfiltered Dictionary Length: {len(unfiltered_dict)}")
    print(f"Negative Difference in Length (Current - Unfiltered): {-(len(unfiltered_dict) - len(curr_dict))}")
    print(f"Current Postings Length: {curr_pcount}", end=" ")
    print(f"Unfiltered Postings Length: {unfiltered_pcount}")
    print(f"Negative Difference in Length (Current - Unfiltered): {-(unfiltered_pcount - curr_pcount)}\n")
    

def LossyCompression(unfiltered_index: dict, stemmer, thirtyList, onefiftyList):

    unfiltered_dictionary = list(unfiltered_index.keys())
    unfiltered_postingsList = list(unfiltered_index.values())

    # compression
    nonumber_index = compressionByNumberRemoval(unfiltered_index)
    lowercased_index = compressionByLowercasing(nonumber_index)
    thirty_index = compressionByThirtySW(lowercased_index, thirtyList)
    onefifty_index = compressionByOneFiftySW(thirty_index, onefiftyList)
    stemmed_index = compressionByStemming(onefifty_index, stemmer)
    
    write_index("/home/comp479_assignments/assignment2/compressed_index.json", index=stemmed_index)
    
    
    # dictionaries
    lowercased_dictionary = list(lowercased_index.keys())
    stemmed_dictionary = list(stemmed_index.keys())
    onefifty_dictionary = list(onefifty_index.keys())
    thirty_dictionary = list(thirty_index.keys())
    nonumber_dictionary = list(nonumber_index.keys())
    # postings lists
    lowercased_postingsList = list(lowercased_index.values())
    stemmed_postingsList = list(stemmed_index.values())
    onefifty_postingsList = list(onefifty_index.values())
    thirty_postingsList = list(thirty_index.values())
    nonumber_postingsList = list(nonumber_index.values())

    # postings count
    unfilteredpcount = countPostings(unfiltered_postingsList)
    lowercasepcount = countPostings(lowercased_postingsList)
    stemmedpcount = countPostings(stemmed_postingsList)
    onefiftypcount = countPostings(onefifty_postingsList)
    thirtypcount = countPostings(thirty_postingsList)
    nonumberpcount = countPostings(nonumber_postingsList)

    # Compare each index to the index before it and to unfiltered
    sizeComparaison("Nonumber", "unfiltered", unfiltered_dictionary, unfilteredpcount, nonumber_dictionary, nonumberpcount, unfiltered_dictionary, unfilteredpcount)
    sizeComparaison("Lowercased","Nonumber", nonumber_dictionary, nonumberpcount, lowercased_dictionary, lowercasepcount, unfiltered_dictionary, unfilteredpcount)
    sizeComparaison("Thirty", "Lowercased",lowercased_dictionary, lowercasepcount, thirty_dictionary, thirtypcount, unfiltered_dictionary, unfilteredpcount)
    sizeComparaison("OneFifty", "Thirty",thirty_dictionary, thirtypcount, onefifty_dictionary, onefiftypcount, unfiltered_dictionary, unfilteredpcount)
    sizeComparaison("Stemmed", "OneFifty",onefifty_dictionary, onefiftypcount, stemmed_dictionary, stemmedpcount, unfiltered_dictionary, unfilteredpcount)



if __name__ == "__main__":

    unfiltered_index = load_index("/home/comp479_assignments/assignment2/naive_index.json")
    stemmer = PorterStemmer()
    stopwordsList = stopwords.words('english')
    thirtyList = list(set(stopwordsList))[:30]
    onefiftyList = [stopword for stopword in stopwordsList if stopword not in thirtyList ]
    LossyCompression(unfiltered_index, stemmer, thirtyList, onefiftyList)
