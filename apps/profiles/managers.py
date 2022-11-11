from django.db import models
from django.db.models import Q


class ProfileManager(models.Manager):
    def get_all_profiles(self, me):
        """        
        me : utilisateur connecté

        Returns:
            cette méthode renvoie tout les profiles sauf moi (moi c'est-à-dire utilisateur connecté)
        """
        from apps.profiles.models import Profile
        
        profiles = Profile.objects.select_related('user').filter(user__is_verified_email=True)
        # profiles = Profile.objects.select_related('user').filter(user__is_verified_email=True).exclude(user=me)
        return profiles
    
    # def get_all_profiles_to_invites(self, sender):
    #     """
    #     Args:
    #         sender : utilisateur qui envoie l'invitation

    #     Returns:
    #         cette méthode renvoie tout les profiles pas de relation avec moi (moi c'est-à-dire utilisateur connecté)
    #     """
    #     from apps.friends.models import Relationship
    #     from apps.profiles.models import Profile
        
    #     profiles = Profile.objects.select_related('user').prefetch_related('sender').filter(user__is_email_verified=True).exclude(user=sender)
    #     profile = Profile.objects.get(user=sender)
    #     qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        
    #     accepted = set([])
    #     for q in qs:
    #         if q.status == 'accepted':
    #             accepted.add(q.receiver)
    #             accepted.add(q.sender)
        
    #     available = [profile for profile in profiles if profile not in accepted]
        
    #     return available