import os
from numpy import *

from matplotlib.pyplot import *

from collections import Counter

from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix

    
def matrix_of_occurrences(path,dictionary):
# returns the matrix whose components are the numbers of occurrences of word features (i.e. words in the dictionary) in the emails tested

      testing_emails = [os.path.join(path,paths) for paths in os.listdir(path)]
      occurrences = zeros((len(testing_emails),len(dictionary)))
      email_number = 0;
      
      for email in testing_emails:
        with open(email) as message:
          for line_count,line in enumerate(message):
            if line_count == 2: # interesting part of the email is line 2
              words = line.split()
              for word in words:
                word_number = 0
                for number,dict in enumerate(dictionary):
                # "enumerate(dictionary)" generates the following index series: (0,dictionary[0]), (1,dictionary[1]), etc. - that is to say (0,('word0',count0)), (1,('word1',count1)), etc.
                  if dict[0] == word:
                    word_number = number
                    occurrences[email_number,word_number] = words.count(word)
                    # "words.count(word)" return the count of how many times word occurs in list words
          email_number += 1     
      
      return occurrences
      
      
def words_in_dictionary(path,size_of_dictionary):
# returns the words in the dictionary used for classification and their frequencies in the training data set
    
      training_emails = [os.path.join(path,paths) for paths in os.listdir(path)]
      # "os.path.join(path,paths)" returns the concatenation of path and any members of paths and "os.listdir(dirname)" lists the files in the directory    
      words = []       
      
      for email in training_emails:    
          with open(email) as message:
              for number,line in enumerate(message):
              # "enumerate(message)" generates the following index series: (0,message[0]), (1,message[1]), etc.
                  if number == 2: # interesting part of the email is line 2
                      words += line.split()
                      
      return Counter(words).most_common(size_of_dictionary)
      # "Counter(words)" returns an unordered collection where elements of words are stored as dictionary keys and their counts are stored as dictionary values : [('word0', count0), ('word1', count1), etc.]
      # "most common(n)" return a list of the n most common elements and their counts  


training_array = zeros(702)
training_array[351:701] = 1
# array representing preclassified (spam/legitimate) emails (i.e. training emails)


# Filter training :

size_of_dictionary = 2500
word_features = words_in_dictionary('train-mails',size_of_dictionary)
print("dictionary:",word_features)
# words in the dictionary used for classification
training_occurrences = matrix_of_occurrences('train-mails',word_features)
# matrix of occurrences of the dictionary words in the training data set 

M_filter = MultinomialNB()
M_filter.fit(training_occurrences,training_array)
  
# Filter testing :

testing_occurrences = matrix_of_occurrences('spam',word_features)
print("matrix of occurrences:",testing_occurrences)
# matrix of occurrences of the dictionary words in the email tested

# Analysis of spam message :
  
M_log_proba = M_filter.predict_log_proba(testing_occurrences)
# returns log-probability estimates for the test vector "testing_occurrences"

M_proba = M_filter.predict_proba(testing_occurrences)
# returns probability estimates for the test vector "testing_occurrences"
  
M_prior = M_filter.class_log_prior_
# returns smoothed empirical log probability for each class (legitimate/spam)
    
def c_legitimate(array_1,array_2):
  i = exp(array_1[0])
  for j in range(len(array_2[:,0])):
    i = i*array_2[j,0]
  return i
  
def c_spam(array_1,array_2):
  i = exp(array_1[1])
  for j in range(len(array_2[:,1])):
    i = i*array_2[j,1]
  return i
  
M_c_legitimate = c_legitimate(M_prior,M_proba)
# returns the value of c for the legitimate class (cf. equation (1) in report) for the email tested
M_c_spam = c_spam(M_prior,M_proba)
# returns the value of c for the spam class (cf. equation (1) in report) for the email tested

print("prior proba legitimate class (determined through training):",exp(M_prior[0]))
print("prior proba spam class (determined through training):",exp(M_prior[1]))

print("c value legitimate class:",M_c_legitimate)
print("c value spam class:",M_c_spam)

proba_constant = M_c_legitimate + M_c_spam

print("P(L|d)=",M_c_legitimate/proba_constant)
print("P(S|d)=",M_c_spam/proba_constant)