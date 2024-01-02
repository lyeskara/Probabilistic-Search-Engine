import json, math, os, time
from nltk import word_tokenize
from collections import defaultdict
from utilityFunctions import text_extraction

def load_index(filePath: str) -> dict:
    with open(filePath, 'r') as json_file:
        data_dict = json.load(json_file) 
    return data_dict


def calculate_document_size(documents):
    document_size = {}
    for doc_id, text in documents:
        document_size[doc_id] = len(word_tokenize(text))
    return document_size

def calculate_idf_values(inverted_index, total_documents):
    idf_dict = defaultdict(float) 
    for term, postings in inverted_index.items():
        # number of documents that contain term
        dft = len(postings)
        if term in idf_dict:
            idf_dict[term] = math.log((total_documents) / (dft ))
        else: idf_dict[term] = 0.0
    
    return idf_dict


def calculate_bm25_score(query, doc_id, inverted_index, documents_sizes, idf_dict, k1, k3, b):
    doc_score = 0
    doc_length = documents_sizes[doc_id]
    avgdl = sum(documents_sizes.values()) / len(documents_sizes)

    for term in query:
        if term in inverted_index:
            f_t_d = inverted_index[term].count(doc_id)
            qf_t = query.count(term)
            idf_t = idf_dict[term]

            # Calculate the term's contribution to the document score
            term_score = (idf_t * f_t_d * (k1 + 1)) / (f_t_d + k1 * (1 - b + b * doc_length / avgdl))
            term_score *= (qf_t * (k3 + 1)) / (qf_t + k3)

            # Add the term's contribution to the document score
            doc_score += term_score

    return doc_score

def searchWithBM25Ranking(query, inverted_index, documents_sizes, idf_dict, k1, k3, b):
    # Tokenize and process the user's query
    query_terms =word_tokenize(query)  

    # Create a dictionary to store document scores
    doc_scores = {}

    # Calculate BM25 scores for each document in the collection
    for doc_id, _ in documents_sizes.items():
        doc_score = calculate_bm25_score(query_terms, doc_id, inverted_index, documents_sizes, idf_dict, k1, k3, b)
        doc_scores[doc_id] = doc_score

    # Sort documents by their BM25 scores in descending order
    ranked_documents = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)

    return ranked_documents

def documents_sizes_exist(filepath):
    if os.path.exists(filepath):
        return True
    else: return False   
    
if __name__ == "__main__":
   
    index = load_index("/home/comp479_assignments/assignment3/SPMI_index.json")
    documents_sizes_path = "/home/comp479_assignments/assignment3/documents_sizes.json"
    idf_dict_path = "/home/comp479_assignments/assignment3/documents_sizes.json"
    
    documents_sizes = {}
    
    if not documents_sizes_exist(documents_sizes_path):
        documents = text_extraction("/home/comp479_assignments/reuters_data")
        documents_sizes = calculate_document_size(documents)
        with open(documents_sizes_path, 'w') as file:
            json.dump(documents_sizes, file)
    else:
        with open(documents_sizes_path, 'r') as json_file:
            documents_sizes = json.load(json_file) 
    
    idf_dict = {}
    if not documents_sizes_exist(idf_dict_path):
       idf_dict = calculate_idf_values(index, len(documents))
       with open(idf_dict_path, 'w') as file:
            json.dump(idf_dict, file)
    else: 
        with open(idf_dict_path, 'r') as json_file:
            idf_dict = json.load(json_file) 
    
    
    k1 = 1.2
    k3 = 1.5 
    b = 0.75

     
    queries=["Democrats welfare and healthcare reform policies","Drug company bankruptcies","George Bush"]
    
    for query in queries:
        folder_path = os.path.join("/home/comp479_assignments/assignment3", query)
        os.makedirs(folder_path, exist_ok=True)
        
        # Perform the search
        start = time.perf_counter()
        ranked_results = searchWithBM25Ranking(query, index, documents_sizes, idf_dict, k1, k3, b)
        end = time.perf_counter()
        
        print(f"the time it took to rank the pages: {(end - start)}")
        # Save the result file inside the folder
        result_file_path = os.path.join(folder_path, f"{query}_BM25.json")
        with open(result_file_path, 'w') as file:
            json.dump(ranked_results, file)
                
    personal_queries = ["Hello World!", "Java is best programming language", "C++ is for legends", "Canada is cool", "Montreal is cold", "a Monad is a monoid in the category of endofunctors"]
    
    for query in personal_queries:
        folder_path = os.path.join("/home/comp479_assignments/assignment3", query)
        os.makedirs(folder_path, exist_ok=True)
        # Perform the search
        ranked_results = searchWithBM25Ranking(query, index, documents_sizes, idf_dict, k1, k3, b)

        # Save the result file inside the folder
        result_file_path = os.path.join(folder_path, f"{query}_BM25.json")
        with open(result_file_path, 'w') as file:
            json.dump(ranked_results, file)
