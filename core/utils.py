from .models import Capsule
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
        capsule.save()
