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

dictionary_size = arange(10,100,10)
M_accuracy = zeros(9)
G_accuracy = zeros(9)
M_falsealarmrate = zeros(9)
G_falsealarmrate = zeros(9)

for j in range(0,9):
# for various sizes of dictionary
  
  # Filter training :

  size_of_dictionary = 10+10*j
  word_features = words_in_dictionary('train-mails',size_of_dictionary)
  # words in the dictionary used for classification
  training_occurrences = matrix_of_occurrences('train-mails',word_features)
  # matrix of occurrences of the dictionary words in the training data set 

  M_filter = MultinomialNB()
  M_filter.fit(training_occurrences,training_array)
  
  G_filter = GaussianNB()
  G_filter.fit(training_occurrences,training_array)
  
  # Filter testing :

  testing_occurrences = matrix_of_occurrences('test-mails',word_features)
  # matrix of occurrences of the dictionary words in the emails tested
  
  M_classification = M_filter.predict(testing_occurrences)
  G_classification = G_filter.predict(testing_occurrences) 
  # performs classification

  # Analysis of performance :
  
  testing_array = zeros(260)
  testing_array[130:260] = 1 
  # array representing classified (spam/legitimate) emails (i.e. test emails) to check results
  
  M_confusion_matrix = confusion_matrix(testing_array,M_classification)
  G_confusion_matrix = confusion_matrix(testing_array,G_classification)
  
  print("Multinomial Confusion matrix Dictionary size:", size_of_dictionary)
  print(M_confusion_matrix)
  print("Gaussian Confusion matrix Dictionary size:", size_of_dictionary)
  print(G_confusion_matrix)

  M_accuracy[j] = (M_confusion_matrix[0][0]+M_confusion_matrix[1][1])/260
  G_accuracy[j] = (G_confusion_matrix[0][0]+G_confusion_matrix[1][1])/260
  M_falsealarmrate[j] = M_confusion_matrix[1][0]/130
  G_falsealarmrate[j] = G_confusion_matrix[1][0]/130

print("List of dictionary sizes:",dictionary_size,"Multinomial accuracy :",M_accuracy,"Gaussian accuracy:", G_accuracy, "Multinomial falsealarmrate :",M_falsealarmrate, "Gaussian falsealarmrate :",G_falsealarmrate)      