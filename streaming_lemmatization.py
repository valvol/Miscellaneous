from joblib import Parallel, delayed, cpu_count
from more_itertools import chunked

from txt4iw_light import natasha_lemmatize, lemmatize_corpus
from streaming_base import StreamingProcessor

MIN_TOKEN_LEN, MAX_TOKEN_LEN = 4, 20
LEMMA_N_JOBS = 2
LEMMA_BATCH_SIZE = 64


class NatashaStreamingLemmatizer(StreamingProcessor):
    def __init__(self, min_token_len=MIN_TOKEN_LEN, max_token_len=MAX_TOKEN_LEN,
                 lang="russian", n_jobs=LEMMA_N_JOBS, batch_size=LEMMA_BATCH_SIZE):
        self.min_token_len = min_token_len
        self.max_token_len = max_token_len
        self.lang = lang
        self.lemmatizer = natasha_lemmatize
        self._n_jobs = n_jobs
        self.batch_size = batch_size

    def _lemmatize_batch(self, batch):
        tokenized_texts, tags4texts = lemmatize_corpus(batch, lemmatizer=self.lemmatizer,
                                               minlen=self.min_token_len, maxlen=self.max_token_len,
                                               language=self.lang)
        return tokenized_texts

    def process_batch(self, batch):
        result = Parallel(n_jobs=self._n_jobs)(
             delayed(self._lemmatize_batch)(sub_batch)
             for sub_batch in chunked(batch, n = len(batch) // self.batch_size)
        )
        final_list_of_lists = result[0]
        for sublist in result[1:]:
            final_list_of_lists.extend(sublist)
        return final_list_of_lists
