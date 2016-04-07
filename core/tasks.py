from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import Capsule
from data_mining.data_mining import api
from sklearn.externals import joblib
from tweepy.error import TweepError
from post_classifier.post_classifier import CLASSIFICATION_TO_ML_TARGET_NUMBER
from django.core.mail import EmailMessage
from PS_Prototype.settings import EMAIL_HOST_USER
from datetime import datetime

'''Tasks, for More Detailed behavior see the Helper Functions Below'''
logger = get_task_logger(__name__)




@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_find_dead_users",
    ignore_result=False
)
def task_find_dead_users():
    """Kicks off job for finding in-active capsules with a dead owner."""
    find_dead_candidates()
    logger.info("Searched and marked dead users")





@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="task_mark_marriage_capsules_deliverable",
    ignore_result=False
)
def task_mark_marriage_capsules_deliverable():
    """Kicks off job for finding activate marriage capsules that are not marked for delivery"""
    generic_find_delivery_candidates(delivery_type='M', desired_classification='marriage')
    logger.info("Searched and activated marriage capsules.")




@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="task_mark_child_birth_capsules_deliverable",
    ignore_result=False
)
def task_mark_child_birth_capsules_deliverable():
    """Kicks off job for finding activate child birth capsules that are not marked for delivery"""
    generic_find_delivery_candidates(delivery_type='CB', desired_classification='baby')
    logger.info("Searched and activated baby capsules.")





@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="task_mark_death_capsules_deliverable",
    ignore_result=False
)
def task_mark_death_capsules_deliverable():
    """Kicks off job for finding activate death capsules that are not marked for delivery"""
    generic_find_delivery_candidates(delivery_type='D', desired_classification='death')
    logger.info("Searched and activated death capsules.")


@periodic_task(
    run_every=(crontab(minute='*/10')),
    name="task_mark_date_capsules_deliverable",
    ignore_result=False
)
def task_mark_date_capsules_deliverable():
    """Kicks off job for finding activate specific date capsules that are not marked for delivery"""
    find_deliverable_by_date_candidates()
    logger.info("Searched and activated specific date capsules.")


@periodic_task(
    run_every=(crontab(minute='*/3')),
    name="task_mail_man",
    ignore_result=False
)
def task_mail_man():
    """Kicks off job for mailing"""
    mail_man()
    logger.info("Active and Deliverable Capsules Found, Capsules Dispersed, MailMan Let Loose")


"""Abstracted Helper Functions"""


def find_dead_candidates():
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
            if score_threshold(recently_received_tweets, classifier, CLASSIFICATION_TO_ML_TARGET_NUMBER['death']):
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


def generic_find_delivery_candidates(delivery_type=None, desired_classification=None, use_twitter=True, test_data=None,
                                     test_capsule=None):
    classifier = joblib.load('./post_classifier/classifier.pkl')
    # Get all capsules which are of a certain delivery_type and have not been marked for delivery.
    # AKA delivery candidates

    if test_capsule is not None:
        candidate_capsules = [test_capsule]
    else:
        candidate_capsules = Capsule.objects.filter(delivery_condition=delivery_type, is_deliverable=False,
                                                    is_active=True)
    if not candidate_capsules:
        return
    for candidate in candidate_capsules:
        try:
            if use_twitter:  # Optional flag to override using twitter api for testing purposes
                if candidate.target_twitter[0] != '@':
                    username = '@' + candidate.target_twitter
                else:
                    username = candidate.target_twitter  # In case a user was naughty and included @ despite the directions
                recently_received_tweets = api.search(q=username, count=20)
                recently_received_tweets = [tweet.text for tweet in recently_received_tweets]
            else:
                recently_received_tweets = test_data
            if score_threshold(recently_received_tweets, classifier,
                               CLASSIFICATION_TO_ML_TARGET_NUMBER[desired_classification]):
                candidate.is_deliverable = True
                candidate.save()
        except TweepError as e:
            print(e.reason)
        except Exception as e:
            print(e.args)


def find_deliverable_by_date_candidates():
    candidate_capsules = Capsule.objects.filter(delivery_condition='SD', is_deliverable=False,
                                                is_active=True)  # 'SD' is for specific date

    today_date = datetime.now()  # Create datetime object then extract date component
    today_date = datetime.date(today_date)
    for candidate in candidate_capsules:

        if candidate.delivery_date <= today_date:
            print('found a winner')
            candidate.is_deliverable = True
            candidate.save()



def mail_man():
    """This is the grand daddy cherry on top that is the last step in the Capsule pipeline. Here we scan for Active &&
    Deliverable Capsules and Dispatch them."""
    candidate_capsules = Capsule.objects.filter(is_active=True, is_deliverable=True, retired=False)

    if not candidate_capsules:
        return
    for candidate in candidate_capsules:
        try:
            email = EmailMessage()
            email.from_email = EMAIL_HOST_USER
            email.subject = 'Import Message From P.S.'

            email.body = 'Greetings {},\n\t We at PS extends our deepest condolences to you and your family. Attached to this email is a capsule,a snapshot our client wanted you to have.\n' \
                         'Take solace in knowing the owner of your capsule, forged it with you in their mind. \nOur Deepest Sympathies,\nP.S. Team'.format(
                candidate.target_firstname)
            email.to = [candidate.target_email]
            email.attach_file(candidate.file.path)
            email.send()
            # candidate.retired=True #TODO Remove for live/demos.
        except Exception as e:
            print(e)
