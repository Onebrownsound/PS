from django.test import TestCase
from .tasks import score_threshold, find_dead_candidates, generic_find_delivery_candidates
from sklearn.externals import joblib
from post_classifier.post_classifier import randomly_sample_data, evaluate_classifier, CLASSIFICATION_TO_ML_TARGET_NUMBER
from post_classifier.datacombiner import DataCombiner
from .models import Capsule, FUTURE_DELIVERY_CHOICES
from django.contrib.auth.models import User
import random


# Create your tests here.

class UtilsTestCase(TestCase):
    """
    Here we load the ML classifier and feed it some fake twitter/social media feeds into score_threshold. The default
    intended behavior is that > 45% that gets classifier as our desired result AKA we are looking for death tweets, to
    classify a user as dead. If >45% or what ever threshold we input gets classified as what we are searching for we
    should return True else False.

    We also set up dummy DB data, to see if the scheduled background celery workers found in tasks.py are functioning.
    """

    def setUp(self):
        # Here we make a dummy User and dummy capsules for subsequent tests. Remember these only exist in test dummy db.
        dummy_data = {'title': 'dummy title', 'message': 'test message'}
        User.objects.create_user(username='dom', email='dom@g.com', password='dom')
        Capsule.objects.create(activation_type='D', is_active=False, is_deliverable=False, author_twitter='_PSDev',
                               owner=User.objects.get(username='dom'), **dummy_data)

    def test_scoring_functionality(self):
        classifier = joblib.load('./post_classifier/classifier.pkl')
        failing_data = ['I hope da patriots win', 'this game is dumb', 'holy cow  did you guys see kylie jenner?',
                        'I cannot wait to be king!!']
        passing_data = ['I am so sorry for your loss', 'cann somebody pass me the milk',
                        'rip to bobby my deepest condolences for his family', '#rip to the best friend I ever had',
                        'the world lost someone amazing today RIP pdiddy']
        self.assertEqual(score_threshold(failing_data, classifier, CLASSIFICATION_TO_ML_TARGET_NUMBER['death']), False)
        self.assertEqual(score_threshold(passing_data, classifier, CLASSIFICATION_TO_ML_TARGET_NUMBER['death']), True)

    def test_tasks(self):
        delivery_abbreviation_to_verbose = {'D': 'death', 'M': 'marriage', 'CB': 'baby'}
        delivery_abbreviation_to_faketweets = {
            'D': ['rip I am so sorry for your loss', 'my deepest condolences should be extended to your family',
                  'i hate the islanders', 'I love and will miss jon #rip',
                  'my condolences to mary and her family rip jon'],
            'M': ['grats to eileen and mark i hope they cherish each other on their special day',
                  'congratulations to mary and joe on their special day', 'i like turtles',
                  'congratulations on getting married'],
            'CB': ['congratulations on baby its a boy!', 'congrats on the new baby',
                   'to infinity and beyond', 'congratulations on baby its a boy!', 'congratulations on baby its a boy!']
        }

        # This test actual utilizes the twitter api call in the pipline
        find_dead_candidates()
        self.assertEqual(Capsule.objects.get(pk=1).is_active, True)

        # Below tests the generic_find_delivery function. We randomly select a delivery choice and the appropriate
        # respective paramters.
        for index in range(100000):
            random_delivery_condition = random.choice(FUTURE_DELIVERY_CHOICES)[0]
            if random_delivery_condition == 'SD':  # Skip dates sincel logic is not implemented TODO implement date logic
                break
            dummy_capsule = Capsule(is_active=True, is_deliverable=False, delivery_condition=random_delivery_condition,
                                    owner=User.objects.get(username='dom'))
            generic_find_delivery_candidates(use_twitter=False,
                                             test_data=delivery_abbreviation_to_faketweets[random_delivery_condition],
                                             test_capsule=dummy_capsule,
                                             desired_classification=delivery_abbreviation_to_verbose[
                                                 random_delivery_condition])
            self.assertEqual(dummy_capsule.is_deliverable, True)


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
