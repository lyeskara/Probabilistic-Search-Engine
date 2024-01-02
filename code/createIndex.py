# Import necessary libraries
from utilityFunctions import text_extraction, Tokenizer
import os
import json

# Define a function to normalize a given corpus of news articles


def TokenNormalization(corpus):
    # Extract text from the corpus
    textsList = text_extraction(corpus)
    # Tokenize the extracted texts
    tokensList = Tokenizer(textsList)
    return tokensList

# 1. Develop a module that, while there are still more documents to be processed,
# accepts a document as a list/stream of tokens and outputs term-documentID pairs to a list F.


def createTermVocabulary(normalized_articles):
    F = []  # F will be a list of term-documentID pairs
    for article in normalized_articles:
        for term in article[1]:
            # Add the term-documentID pair to F
            F.append((term, article[0]))
    return F

# 2. When there is no more input, sort F and remove duplicates


def sortedTerms(TermVocabulary):
    # Sort the term-documentID pairs by the term (alphabetically)
    sorted_array = sorted(TermVocabulary, key=lambda x: x[0])

    # Remove duplicates while preserving the order
    uniqueTerms = set()
    nonDuplicateSortedList = []

    for term in sorted_array:
        if term not in uniqueTerms:
            nonDuplicateSortedList.append(term)
            uniqueTerms.add(term)

    # Return the result
    return nonDuplicateSortedList

# 3. Turn the sorted file F into an index by turning the docIDs paired with the same term
# into a postings list and linking it to the term


def create_inverted_index(term_list):
    inverted_index = {}  # Initialize the inverted index as a dictionary
    for term, term_id in term_list:
        if term not in inverted_index:
            # Create an empty list for each unique term
            inverted_index[term] = []
        # Append the document ID to the postings list
        inverted_index[term].append(term_id)

    return inverted_index
##

# Entry point of the script
if __name__ == "__main__":

    # Normalize the articles and obtain a list of term-documentID pairs
    normalized_articles = TokenNormalization("/home/comp479_assignments/reuters_data")

    # Create the term-document vocabulary (F)
    F = createTermVocabulary(normalized_articles)

    # Sort the vocabulary and remove duplicates
    sortedF = sortedTerms(F)

    # Create the inverted index
    index = create_inverted_index(sortedF)

    # Define the directory path for saving the index as a JSON file
    directory_path = "/home/comp479_assignments/assignment2"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Save the inverted index to a JSON file
    with open(os.path.join(directory_path, "naive_index.json"), 'w') as file:
        json.dump(index, file)
