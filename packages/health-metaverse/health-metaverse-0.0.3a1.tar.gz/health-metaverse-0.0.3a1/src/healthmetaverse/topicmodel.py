from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import pickle
import pyLDAvis.gensim
import warnings
from nltk.stem import WordNetLemmatizer
import pandas as pd
from nltk.tokenize import word_tokenize
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings("ignore")

def build_topic_model(
    list_abstract,
    MAX_TOPICS=10,
    MIN_PERC=0.8
    ):


    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    en_stop = get_stop_words('en')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # create sample documents

    # compile sample documents into a list
    # doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]


    def singularize(text):
        wnl = WordNetLemmatizer()
        tokens = [token.lower() for token in word_tokenize(text)]
        lemmatized_words = [wnl.lemmatize(token) for token in tokens]
        return (' '.join(lemmatized_words)).strip()

    docs = []
    doc_ids = []
    for idx, keywords in enumerate(list_abstract):
        list_words = keywords.split(";")
        list_tokens = []
        for w in list_words:
            w = w.lower()
            w = singularize(w)
            list_tokens.append(w)

        docs.append(list_tokens)
        doc_ids.append(idx)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(docs)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in docs]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=MAX_TOPICS, id2word=dictionary, passes=20,
                                               alpha='auto', eta='auto')

    # print keywords
    topics = ldamodel.print_topics(num_words=10)
    for topic in topics:
        print(topic)



    return ldamodel,corpus,dictionary,docs,doc_ids

def format_topics_sentences(MAX_TOPICS, MIN_PERC,ldamodel, corpus, docs,doc_ids):
    list_tags = []
    for i in range(MAX_TOPICS):
        list_tags.append("t" + str(i + 1))

    # Init output
    sent_topics_df = pd.DataFrame()

    fout = open("covid19_topics_" + str(MAX_TOPICS) + ".csv", "w", encoding="utf-8")
    fout.write("id,symptoms," + ",".join(list_tags) + "\n")
    # Get main topic in each document
    for i, row_list in enumerate(ldamodel[corpus]):
        doc_id = doc_ids[i]
        text = docs[doc_id]
        # print("------------Document " + str(doc_id) + "----------------------")
        row = row_list[0] if ldamodel.per_word_topics else row_list

        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        # print(row)
        ts = ["0" for i in range(MAX_TOPICS)]
        for j, (topic_num, prop_topic) in enumerate(row):
            # print("Topic " + str(topic_num) + "\t" + str(prop_topic))
            if prop_topic >= MIN_PERC and prop_topic <= 1:
                ts[topic_num] = "1"
            else:
                ts[topic_num] = "0"
            '''
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
            '''
        line = str(doc_id) + ",\"" + text + "\"," + ",".join(ts) + "\n"
        fout.write(line)
    fout.close()
    return sent_topics_df

def start_to_build_topic_model(
        list_abstract,
        MAX_TOPICS=10,
        MIN_PERC=0.8,
        export_html=False,
        export_html_path="visualize.html",
        need_format=False,
        save_model=False,
        save_model_path="model.gensim"
):
    # list_abstract = pickle.load(open("datasets/virtual reality and health.pickle", "rb"))
    lda_model,corpus,dictionary,docs,doc_ids=build_topic_model(list_abstract,MAX_TOPICS,MIN_PERC)
    # Compute Perplexity
    perplexity= lda_model.log_perplexity(corpus)
    print('\nPerplexity: ',perplexity)  # a measure of how good the model is. lower the better.

    # Compute Coherence Score
    from gensim.models import CoherenceModel
    # coherence_model_lda = CoherenceModel(model=ldamodel, texts=docs, dictionary=dictionary, coherence='c_v')
    # coherence_lda = coherence_model_lda.get_coherence()
    # print('\nCoherence Score (CV): ', coherence_lda)

    # Visualize the topics
    if export_html:
        vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
        pyLDAvis.save_html(vis, export_html_path)
    if need_format==True:
        df_topic_sents_keywords = format_topics_sentences(MAX_TOPICS=MAX_TOPICS,MIN_PERC=MIN_PERC, ldamodel=lda_model, corpus=corpus, docs=list_abstract,doc_ids=doc_ids)
    else:
        df_topic_sents_keywords=None
    if save_model:
        lda_model.save(save_model_path)
    return perplexity,df_topic_sents_keywords





