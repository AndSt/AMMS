from metaflow import FlowSpec, step

import os
import numpy as np
import joblib
import time

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier


class SimpleTextClassificationFlow(FlowSpec):

    @step
    def start(self):
        self.model_name = 'simple_text'
        self.model_version = '1_0_5'

        self.train_dir = os.environ['TRAIN_DIR']
        self.model_save_dir = '/shared_volume'
        print('Store dir: {}'.format(self.model_save_dir))
        self.next(self.load_data)

    @step
    def load_data(self):
        self.twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
        self.twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
        self.next(self.create_model)

    @step
    def create_model(self):
        self.clf = Pipeline([
            ('vect', CountVectorizer(max_features=5, max_df=5)),
            ('tfidf', TfidfTransformer()),
            ('clf-svm', DecisionTreeClassifier(max_features=1, max_depth=1, max_leaf_nodes=2, random_state=42))
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
        if not os.path.isdir(self.model_save_dir):
            os.mkdir(self.model_save_dir)

        file_name = '{}-{}-{}.pbz2'.format(self.model_name, self.model_version, time.time())
        print('Save at: {}/{}'.format(self.model_save_dir, file_name))
        with open('{}/{}'.format(self.model_save_dir, file_name), 'wb') as handle:
            joblib.dump(self.clf, handle)
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == '__main__':
    SimpleTextClassificationFlow()
