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

    def save(self, **kwargs):
        not_given = []
        for field in self.REQUIRED_FIELDS:
            if not hasattr(self, field) or not getattr(self, field):
                not_given.append(field)

        if not_given:
            raise ValueError(f"Some required field(s) were not passed: {', '.join(not_given)}")
        
        return super().save(**kwargs)
    
    def delete(self):           # Talvez depreciar
        if not self.active:
            raise ValueError(f"Cannot delete game {self.name}: already deleted")
        self.active = False

    def __str__(self):
        return self.name