from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import Capsule
from data_mining.data_mining import api
from sklearn.externals import joblib

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
    classifier = joblib.load('./post_classifier/classifier.pkl')
    candidate_capsules = Capsule.objects.filter(activation_type='D', is_active=False)
    if not candidate_capsules:
        return
    for candidate in candidate_capsules:
        try:
            username = '@' + candidate.author_twitter  # searching for @author_twitter will show incoming tweets to author
            recently_received_tweets = api.search(q=username, count=20)
            recently_received_tweets = [tweet.text for tweet in recently_received_tweets]  # <3 generators extract text
            if score_threshold(recently_received_tweets, classifier, 1):
                candidate.is_active = True
                candidate.save()
        except Exception as e:
            pass


def score_threshold(data, clf, success_classification, threshold=0.45):
    number_of_tweets = len(data)
    score = 0
    predicted_results = clf.predict(data)
    for predicted_classification in predicted_results:
        if predicted_classification == success_classification:
            score += 1
    if float(score / number_of_tweets) >= threshold:
        return True
    return False
