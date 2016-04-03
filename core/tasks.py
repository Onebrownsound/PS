from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import Capsule
from data_mining.data_mining import api
from sklearn.externals import joblib
from tweepy.error import TweepError
from post_classifier.post_classifier import CLASSIFICATION_TRANSLATOR

logger = get_task_logger(__name__)

'''Tasks, for More Detailed behavior see the Helper Functions Below'''


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_find_dead_users",
    ignore_result=False
)
def task_find_dead_users():
    """
    Kicks off job of finding dead users
    """

    find_dead_users()

    logger.info("Searched and marked dead users")


"""Abstracted Helper Functions"""


def find_dead_users():
    """
    Entry point to time base job which prunes for capsules which are death activated and have not been flagged as active
    yet. Mutates (changes <Capsule>.is_active->True) and saves capsules that break a scoring threshold).Unsure how celery
    distributes this task to workers.
    Args:
        None
    Output:
        None
    """
    classifier = joblib.load('./post_classifier/classifier.pkl')
    candidate_capsules = Capsule.objects.filter(activation_type='D', is_active=False)
    if not candidate_capsules:
        return
    for candidate in candidate_capsules:
        try:
            if candidate.author_twitter[0] != '@':
                username = '@' + candidate.author_twitter  # searching for @author_twitter will show incoming tweets to author
            else:
                username = candidate.author_twitter  # Incase a user was naughty and included @ despite the directions
            recently_received_tweets = api.search(q=username, count=20)
            recently_received_tweets = [tweet.text for tweet in recently_received_tweets]  # <3 generators extract text
            if score_threshold(recently_received_tweets, classifier, CLASSIFICATION_TRANSLATOR['death']):
                candidate.is_active = True
                candidate.save()
        except TweepError as e:
            print(e.reason)
        except Exception as e:
            print(e.args)


def score_threshold(data, clf, success_classification, threshold=0.45):
    '''
    This is the scoring function. It essentially takes in a portion of tweets for a user and feeds them into a trained
    machine learning algorithm (SGD Classifier). The classifier classifies each posts and assigns the set of tweets a score
    based off of how many match the desired success_classification.

    Args:
        data:list of strings (of tweets)
        clf:a loaded classifier (sklearn)
        success_classification: int (which maps to a string ex: 1:'Death'
        threshold : float should be >0 and < 1.
    Output:
        Boolean

    '''
    number_of_tweets = len(data)
    score = 0
    predicted_results = clf.predict(data)
    for predicted_classification in predicted_results:
        if predicted_classification == success_classification:
            score += 1
    if float(score / number_of_tweets) >= threshold:
        return True
    return False
