import collections

file=open('C:\Users\CiphersNUC\Downloads\word_cloud\98-0.txt')

# if you want to use stopwords, here's an example of how to do this
stopwords = set(line.strip() for line in open('C:\Users\CiphersNUC\Downloads\word_cloud\stopwords'))

# create your data structure here.
wordcount={}

# Instantiate a dictionary, and for every word in the file, add to 
# the dictionary if it doesn't exist. If it does, increase the count.

# Hint: To eliminate duplicates, remember to split by punctuation, 
# and use case demiliters. The functions lower() and split() will be useful!

for word in file.read().lower().split():
    word = word.replace(".","").replace(",","").replace("\"","").replace("_","")
    # word = word.replace(".","")
    # word = word.replace(",","")
    # word = word.replace("\"","")
    if word not in stopwords:
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1

# after building your wordcount, you can then sort it and return the first
# n words. If you want, collections.Counter may be useful.

d = collections.Counter(wordcount)

#print(d.most_common(10))
for word, count in d.most_common(10):
    print(word, ": ", count)