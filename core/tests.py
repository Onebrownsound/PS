from django.test import TestCase
from .tasks import score_threshold
from sklearn.externals import joblib
from post_classifier.post_classifier import randomly_sample_data, evaluate_classifier
from post_classifier.datacombiner import DataCombiner


# Create your tests here.

class UtilsTestCase(TestCase):
    """
    Here we load the ML classifier and feed it some fake twitter/social media feeds into score_threshold. The default
    intended behavior is that > 45% that gets classifier as our desired result AKA we are looking for death tweets, to
    classify a user as dead. If >45% or what ever threshold we input gets classified as what we are searching for we
    should return True else False.
    """

    def test_scoring_functionality(self):
        classifier = joblib.load('./post_classifier/classifier.pkl')
        failing_data = ['I hope da patriots win', 'this game is dumb', 'holy cow  did you guys see kylie jenner?',
                        'I cannot wait to be king!!']
        passing_data = ['I am so sorry for your loss', 'cann somebody pass me the milk',
                        'rip to bobby my deepest condolences for his family', '#rip to the best friend I ever had',
                        'the world lost someone amazing today RIP pdiddy']
        self.assertEqual(score_threshold(failing_data, classifier, 1), False)
        self.assertEqual(score_threshold(passing_data, classifier, 1), True)


class ClassifierTestCase(TestCase):
    '''
    Here we sample ~100000 tweets and load the ML classifier that has already been trained.
    We want to feed these sampled tweets into the classifier and ensure we have a >99% success in classifying correctly.
    '''

    def test_classifier_functionality(self):
        tweets = DataCombiner(
            filenames=['./post_classifier/marriage_tweets.txt', './post_classifier/death_tweets.txt',
                       './post_classifier/baby_tweets.txt', './post_classifier/garbage_tweets.txt'],
            classifications=['Marriage', 'Death', 'Baby', 'Garbage'])
        classifier = joblib.load('./post_classifier/classifier.pkl')
        sampled_tweets = randomly_sample_data(tweets, 100000)
        self.assertGreater(evaluate_classifier(classifier, sampled_tweets), 0.99)
