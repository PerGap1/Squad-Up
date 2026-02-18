from django.db import models
from core.models import DefaultFields

from squadup.settings import AUTH_USER_MODEL


class Game(DefaultFields): 

    name = models.CharField(max_length=50)
    artwork = models.ImageField()           # Mudar o nome?
    description = models.TextField()
    # developer = ?
    # genres = models.TextChoices()         # Dá para buscar com api da steam
    released = models.DateField()
    # platforms = models.TextChoices()    # Acho que dá para cancelar, nem a Steam mostra muito sobre plataformas

    creator = models.ForeignKey(AUTH_USER_MODEL, null=True, related_name='game_creator', on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['name', 'released', 'creator']

    @classmethod
    def create(cls, **kwargs):
        not_given = []
        for field in cls.REQUIRED_FIELDS:
            if not kwargs.get(field):
                not_given.append(field)

        if not_given:
            raise ValueError(f"Some required field(s) were not passed: {', '.join(not_given)}")
        
        return cls.objects.create(**kwargs)
    
    def delete(self):
        if not self.active:
            raise ValueError(f"Cannot delete game {self.name}: already deleted")
        self.active = False

    def get_users(self):
        return self.user_set.all()
    
    def get_squads(self):
        return self.squad_set.all()
    
    def get_events(self):
        return self.event_set.all()

    def __str__(self):
        return self.name