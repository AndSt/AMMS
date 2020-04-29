from metaflow import FlowSpec, step

import os
import numpy as np
import joblib
import time

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier


class SimpleTextClassificationFlow(FlowSpec):

    @step
    def start(self):
        self.model_name = 'simple_twenty_news_clf'
        self.model_version = '1_0_1'

        self.train_dir = os.environ['TRAIN_DIR']
        self.next(self.load_data)

    @step
    def load_data(self):
        self.twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
        self.twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
        self.next(self.create_model)

    @step
    def create_model(self):
        self.clf = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf-svm', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, max_iter=5, random_state=42))
        ])
        self.next(self.train)

    @step
    def train(self):
        self.clf.fit(self.twenty_train.data, self.twenty_train.target)
        self.next(self.evaluate)

    @step
    def evaluate(self):
        predicted_svm = self.clf.predict(self.twenty_test.data)
        self.accuracy = np.mean(predicted_svm == self.twenty_test.target)
        print('Accuracy: {}'.format(self.accuracy))
        self.next(self.save_model)

    @step
    def save_model(self):
        data_path = '{}/data'.format(self.train_dir)
        if os.path.isdir(data_path) is False:
            os.mkdir(data_path)

        file_name = '{}-{}-{}'.format(self.model_name, self.model_version, time.time())
        with open('{}/{}.pbz2'.format(data_path, file_name), 'wb') as handle:
            joblib.dump(self.clf, handle)
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == '__main__':
    SimpleTextClassificationFlow()
