from nltk.corpus import wordnet as wn
import nltk
# bag of words
from sklearn.feature_extraction.text import CountVectorizer


def data_cleaning(data):
    data["s1"] = data["s1"].str.lower()
    data["s2"] = data["s2"].str.lower()

    # 分词
    tokenizer = nltk.stem.RegexpTokenizer(r'[a-zA-Z]+')
    data["s1_token"] = data["s1"].apply(tokenizer.tokenize)
    data["s2_token"] = data["s2"].apply(tokenizer.tokenize)

    # 去停用词
    stop_words = nltk.stem.stopwords.words('english')

    def word_clean_stopword(word_list):
        words = [word for word in word_list if word not in stop_words]
        return words

    data["s1_token"] = data["s1_token"].apply(word_clean_stopword)
    data["s2_token"] = data["s2_token"].apply(word_clean_stopword)

    # 词形还原
    lemmatizer = nltk.stem.WordNetLemmatizer()

    def word_reduction(word_list):
        words = [lemmatizer.lemmatize(word) for word in word_list]
        return words

    data["s1_token"] = data["s1_token"].apply(word_reduction)
    data["s2_token"] = data["s2_token"].apply(word_reduction)

    # 词干化
    stemmer = nltk.stem.SnowballStemmer('english')

    def word_stemming(word_list):
        words = [stemmer.stem(word) for word in word_list]
        return words

    data["s1_token"] = data["s1_token"].apply(word_stemming)
    data["s2_token"] = data["s2_token"].apply(word_stemming)

    return data

def count_vector(words):
    count_vectorizer = CountVectorizer(stop_words='english')
    emb = count_vectorizer.fit_transform(words)

    return emb, count_vectorizer

bow_data = data
bow_data["words_bow"] = bow_data["s1"] + bow_data["s2"]
bow_test = bow_data[bow_data.score.isnull()]
bow_train = bow_data[~bow_data.score.isnull()]

list_test = bow_test["words_bow"].tolist()
list_train = bow_train["words_bow"].tolist()
list_labels = bow_train["score"].tolist()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(list_train, list_labels, test_size=0.2, random_state=42)
X_train_counts, count_vectorizer = count_vector(X_train)
X_test_counts = count_vectorizer.transform(X_test)
test_counts = count_vectorizer.transform(list_test)
# print(X_train_counts.shape, X_test_counts.shape, test_counts.shape)