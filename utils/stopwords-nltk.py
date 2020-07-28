from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#sentence = "This is a sample sentence, showing off the stop words filtration."
sentence = "All work and no play makes jack dull boy. All work and no play makes jack a dull boy."
stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(sentence)
filtered_sentence = [w for w in word_tokens if not w in stop_words]
print(word_tokens)
print(filtered_sentence)
