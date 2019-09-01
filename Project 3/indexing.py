from bs4 import BeautifulSoup
import os
import re
from collections import defaultdict
from nltk.corpus import stopwords
import math
import db
import page_url_db
import search_engine_gui as seg





directory = 'WEBPAGES_RAW'
#used to store inverted index 
index_dict = defaultdict(list)


def loop_dir(dir):
    count = 0
        
    #set of stops words to not include
    stop = set(stopwords.words('english'))
    
    #dirName = all directories
    #fileList = all files within directory
    for i,(dirName, subdirList, fileList) in enumerate(os.walk(dir)):
        #skips main directory folder
        if i == 0:
            continue
        
        #gets only folder name
        nameOfFolder = re.search('\d+\Z', dirName).group()
        
        #loops all files found in folder
        for doc in fileList:
            
            #formats the name of the folders
            dir_ID = nameOfFolder + '/' + doc
            #adds to number of total documents
            count +=1
            print(count)
             
            try:
                file = open(dirName + '/' + doc,'r',encoding='utf-8')
                
            except IOError:
                print("There was an error opening the file")
                return
             
            #puts everything in doc within tags into a string
            soup = BeautifulSoup(file.read(),'html.parser')
            
            soup = remove_script_style_tags(soup)
            
            # gets all the text from all the tags
            file_content = soup.getText()
            
            #tokenizes all the words
            words = re.findall('[0-9a-zA-Z]+', file_content)
            #used to store the term frequency for each file
            word_count = defaultdict(int)
            
            for word in words:
                #strips words from whitespace and makes it lower
                word = word.strip().lower()
                
                #doesnt include stop words 
                if word not in stop:
                    #add one for each occurrence the word has in doc
                    word_count[word] += 1
            
            #used to store the words with their scores
            custom_scores = defaultdict(int)
            #custom ranking done here
            custom_ranking('title', 5, soup, stop,custom_scores)
            custom_ranking('h1',4,soup,stop,custom_scores)
            custom_ranking({'b':True, 'strong':True, 'h2':True},3,soup,stop,custom_scores)
            custom_ranking('h3', 2, soup, stop, custom_scores)
            custom_ranking('p',1,soup, stop, custom_scores)
           
            #loops through word_count dictionary
            for k,v in word_count.items():  
                #tf stores the term frequency
                #stores the word as a key and its postings list as a value 
                index_dict[k].append({'docID':dir_ID, 'tf':1+math.log10(v), 'tf-idf':0, 'custom_score':custom_scores[k]})
             
            
    calculate_tfidf(index_dict, count)
    
    print('Number of files in the corpus: ' + str(count))
    print('Number of unique words found: ' + str(len(index_dict)))  
    
    
   
def custom_ranking(tag,point,soup,stop,custom_scores):
    ''' take in tag,custom point, beautifulsoup object, set of stop words
    to not include, dictionary to store custom ranking
    '''
    content = ''
    #finds all text within specific tag
    for words in soup.findAll(tag):
        content += words.getText().strip() + '\n'
        
    #tokenizes the words found 
    words = re.findall('[0-9a-zA-z]+', content)
    
    #adds it to the custom_scores dictionary with specified points
    for word in words:
        if word not in stop:
            custom_scores[word.lower()] += point
    
    
def remove_script_style_tags(soup):
    '''removes undesirable tags from document
    '''
    for tags in soup(['script', 'style']):
        #eliminates from object
        tags.decompose()
    return soup 

  
def calculate_tfidf(index_dict,count):
    '''calculates the tf-idf score
    '''
    #loops index_dict dictionary
    for v in index_dict.values():
        #loops through the list of dictionary
        for d in v:
            #gets term frequency
            tf = d['tf']
            #number of documents that the word appears in
            occur = len(v)
            #log of the number of the documents in the corpus/by number of documents where specific term appears
            idf = math.log10(count/occur)
            d['tf-idf'] = tf * idf



def store_links():
    '''Used to store the links from the folder_name/doc_name
    '''
    #used to store folder/file name with its respective url 
    url_dict = dict()
    file = open('WEBPAGES_RAW/bookkeeping.tsv','r',encoding='utf-8')
    
    for line in file.readlines():
        url_dict[line.split('\t')[0]] = line.strip().split('\t')[1]
    
    #inserts the dictionary to the database
    page_url_db.insert(url_dict)
 
 
def process_query(query):
    '''Used to process the user query
    '''
    #used to store the results of the first query
    query1_results = []
    #used to store the results of the second query
    query2_results = []
    #stores all the results from both queries
    final = []
    
    
    

    if len(query) != 0:
        try:
            result = db.find(query[0])
            query1_results.extend(result['info'])
        except Exception:
            pass

    #ignores 2nd query if same as first
    if len(query) >= 2 and query[1] != query[0]:
        try:
            result =db.find(query[1])
            query2_results.extend(result['info'])
        except Exception:
            pass
    

    #checks both postings list for similar docID
    for q1 in query1_results[:]:
        for q2 in query2_results[:]:
            if q2['docID'] == q1['docID']:
                #adds tf,tf-idf,custom_score of both results and appends to final list
                final.append({'docID':q1['docID'], 'tf':q1['tf'] + q2['tf'], 'tf-idf':q1['tf-idf'] + q2['tf-idf'], 'custom_score':q1['custom_score']+q2['custom_score'] })
                #removes that entry from both lists since it was appended to final list 
                query2_results.remove(q2)
                query1_results.remove(q1)
    
    
    
    #adds remaining results to the final list of results
    final.extend(query1_results)
    final.extend(query2_results)
    
        
    return final

def print_results(query_results):
    '''used to print out the results to the console '''
    final_results = []
    try:
        
        #used to get first 10 results
        result_amount = 0
        for result in query_results:
            if result_amount == 10:
                break
              
            file_name = result['docID']
            #finds the file name in another database containing the URL of that file name
            link = page_url_db.find(file_name)
            #prints out link and then postings list
            final_results.append('LINK: {} \n Postings List: {}\n'.format(link['URL'], result))
             
            result_amount +=1 
             
    except Exception:
        print("Sorry, no results were found.")
        
    return final_results
        
        
 
if __name__ == '__main__':  
    ###############################################################
    #used to make the entire inverted index  
    #loop_dir(directory)
    
    #used to store the inverted index into the database
    #db.insert(index_dict)
    
    #used for testing purposes
    #db.print_db()
    #db.remove()
    
    #store_links()
    #page_url_db.print_db()
    #page_url_db.remove()
    
    #print('Done')
    #################################################################
    
    #displays the interface that asks for the user query
    engine_interface = seg.display_main_window()
    query = engine_interface.search_button_clicked().lower()
    
    
    #print('Welcome to our search engine!')
    #query = input('Please enter a word or two words to search for: ').lower()
    #print("\n")
    
    #stores the results form the query
    results = process_query(query.split())
    results = sorted((results), key=lambda k: k['tf-idf'] + k['custom_score'], reverse = True)
    
    
    results_interface = seg.display_results_window(print_results(results))
    #print_results(results_interface.query_results)
    

        
        
        
        
        