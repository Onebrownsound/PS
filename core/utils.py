from .models import Capsule,FUTURE_DELIVERY_DICT
import random



def reset_capsules_randomly():
    """Just a utility function that can be called from console to randomly reset capsules activation and delivery status.
    Greatly beneficially for demoing live to display background workers functioning."""
    capsules = Capsule.objects.all()
    for capsule in capsules:
        random_roll = random.random()
        if random_roll > 0.50:
            capsule.is_deliverable = False
            capsule.is_active = True
        else:
            capsule.is_deliverable = False
            capsule.is_active = False
        capsule.save()


def reset_all_capsules():
    capsules = Capsule.objects.all()
    for capsule in capsules:
        capsule.is_active = False
        capsule.is_deliverable = False
        capsule.retired = False
        capsule.save()

def translate_delivery_condition(ax):
    """
    Takes in a list of Capsule Model objects. Translates short delivery condition abbreviation to the verbose definition
    AKA 'M' -> 'Marriage". Import to note this does not save to the db. Make sure this never happens

    Args:
        ax:list of Capsule Model objects
    Output:
        ax: list of Capsule Model objects with delivery_condition expressed verbosely.
    """
    for data in ax:
        data.delivery_condition = FUTURE_DELIVERY_DICT[data.delivery_condition]
    return ax
