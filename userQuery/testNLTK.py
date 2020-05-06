import nltk
from nltk.corpus import wordnet as wn
# nltk.download('wordnet')
syns = wn.synsets("game")

print(syns[0].name())
print(syns[0].lemmas()[0].name())


# 7. 同义词集的上位词

a = wn.synset('car.n.01').hypernyms()
# 8. 同义词集的下位词


car = wn.synsets('car')
print(car)
b = wn.synset(car[0].name()).hyponyms()

print(a)
print(b)
print(wn.synsets('motorcar'))



# 词形还原
lemmatizer = nltk.stem.WordNetLemmatizer()

def word_reduction(word_list):
    words = [lemmatizer.lemmatize(word) for word in word_list]
    return words


# 词干化
stemmer = nltk.stem.SnowballStemmer('english')
def word_stemming(word_list):
    words = [stemmer.stem(word) for word in word_list]
    return words

sentence = "the heisman vote filled with cases"
sentence = "she ran leg  care. she"
outputData = sentence.split(' ')
# outputData = ["you","are","girls"]
outputData = word_reduction(outputData)
print(outputData)
outputData = word_stemming(outputData)
print(outputData)
