# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import numpy as np

from text2vec.utils.rank_bm25 import BM25Okapi
from text2vec.utils.log import logger
from text2vec.utils.tokenizer import Tokenizer
from text2vec.word2vec import Word2Vec
from text2vec.sbert import SBert, cos_sim


class EmbType(object):
    W2V = 'w2v'
    SBERT = 'sbert'


class SimType(object):
    COSINE = 'cosine'
    WMD = 'wmd'


class Similarity(object):
    def __init__(self, similarity_type=SimType.COSINE, embedding_type=EmbType.SBERT):
        """
        Cal text similarity
        :param similarity_type:
        :param embedding_type:
        """
        if similarity_type == SimType.WMD and embedding_type != EmbType.W2V:
            logger.warning('wmd sim type, emb type must be w2v')
            embedding_type = EmbType.W2V
        # logger.debug('embedding type: {}'.format(embedding_type))
        self.similarity_type = similarity_type
        self.embedding_type = embedding_type
        self.tokenizer = Tokenizer()
        self.model = None

    def load_model(self):
        if self.model is None:
            if self.embedding_type == EmbType.W2V:
                self.model = Word2Vec()
            elif self.embedding_type == EmbType.SBERT:
                self.model = SBert()
            else:
                raise ValueError('model not found.')

    def get_score(self, text1, text2):
        """
        Get score between text1 and text2
        :param text1: str
        :param text2: str
        :return: float, score
        """
        res = 0.0
        text1 = text1.strip()
        text2 = text2.strip()
        if not text1 or not text2:
            return res
        self.load_model()
        if self.similarity_type == SimType.COSINE:
            emb1 = self.model.encode(text1)
            emb2 = self.model.encode(text2)
            res = cos_sim(emb1, emb2)[0]
            res = float(res)
        elif self.similarity_type == SimType.WMD:
            token1 = self.tokenizer.tokenize(text1)
            token2 = self.tokenizer.tokenize(text2)
            res = 1. / (1. + self.model.w2v.wmdistance(token1, token2))
        return res


class SearchSimilarity(object):
    def __init__(self, corpus):
        """
        Search sim doc with rank bm25
        :param corpus: list of str.
            A list of doc.(no need segment, do it in init)
        """
        self.corpus = corpus
        self.corpus_seg = None
        self.bm25_instance = None
        self.tokenizer = Tokenizer()

    def init(self):
        if not self.bm25_instance:
            if not self.corpus:
                logger.error('corpus is none, set corpus with docs.')
                raise ValueError("must set corpus, which is documents, list of str")

            if isinstance(self.corpus, str):
                self.corpus = [self.corpus]

            self.corpus_seg = {k: self.tokenizer.tokenize(k) for k in self.corpus}
            self.bm25_instance = BM25Okapi(corpus=list(self.corpus_seg.values()))

    def get_similarities(self, query, n=5):
        """
        Get similarity between `query` and this docs.
        :param query: str
        :param n: int, num_best
        :return: result, dict, float scores, docs rank
        """
        scores = self.get_scores(query)
        rank_n = np.argsort(scores)[::-1]
        if n > 0:
            rank_n = rank_n[:n]
        return [self.corpus[i] for i in rank_n]

    def get_scores(self, query):
        """
        Get scores between query and docs
        :param query: input str
        :return: numpy array, scores for query between docs
        """
        self.init()
        tokens = self.tokenizer.tokenize(query)
        return self.bm25_instance.get_scores(query=tokens)
