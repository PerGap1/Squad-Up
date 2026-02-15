from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as lazy

from games.models import Game
from core.models import DefaultFields, DefaultFieldsUserRelated


class AbstractGroup(models.Model, DefaultFields):
    class Meta:
        abstract = True

    class Privacy(models.TextChoices):
        PUBLIC = 'PB', lazy('Public')
        LINKED = 'LK', lazy('Linked')
        PRIVATE = 'PR', lazy('Private')

    name = models.CharField(max_length=50)
    privacy = models.CharField(max_length=2, choices=Privacy, default=Privacy.PUBLIC)
    tag = models.CharField(max_length=7, unique=True, editable=False, default=create_tag())     # Ainda não consigo acessar coisas dentro da classe...
    image = models.ImageField()
    members = models.ManyToManyField(get_user_model())

    games = models.ManyToManyField(Game)
    host = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # chat...? Talvez importar um app chat, talvez criar nós mesmos e fazer um relacionamento 1 pra 1
    # schedule: fazer um app pra isso

    def create_tag(self): pass


class Ban(models.Model, DefaultFieldsUserRelated):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_1", "user_2"], name="unique_constraint_friendship"
            )
        ]

    # Acho que por ser AbstractGroup, pode dar erro
    group = models.ForeignKey(AbstractGroup, related_name='ban_group', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='ban_user', on_delete=models.CASCADE)


class Squad(AbstractGroup): pass        # Talvez permitir que um grupo tenha subgrupos, tipo discord


class Event(AbstractGroup):
    group = models.ForeignKey(Squad, blank=True, on_delete=models.CASCADE)  # Para que um grupo possa criar eventos de jogos