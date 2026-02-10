from django.db import models
from django.contrib.auth.models import AbstractUser
from games.models import Game
from core.models import DefaultFields

from django.utils.translation import gettext_lazy as lazy
from django_countries.fields import CountryField

class User(DefaultFields, AbstractUser): 

    class Plan(models.TextChoices):
        FREE = 'FR', lazy('Free')
        PRO = 'PR', lazy('Pro')

    class Status(models.TextChoices):
        ACTIVE = 'AT', lazy('Active')
        SUSPENDED = 'SP', lazy('Suspended')
        BANNED = 'BN', lazy('Banned')

    # USERNAME_FIELD = email                            # Em teoria é assim que se coloca o email como o identificador...
                                                        # Porém não estou conseguindo acessar os atributos de dentro da classe
    
    country = CountryField()
    dark_mode = models.BooleanField(default=True)
    profile_picture = models.ImageField()

    # Campos que costumavam estar em player
    ban_request = models.BooleanField(default=False)
    discord = models.CharField(max_length=30)
    plan = models.CharField(max_length=2, choices=Plan, default=Plan.FREE)
    status = models.CharField(max_length=2, choices=Status, default=Status.ACTIVE)
    # notifications = ?
    # schedule = ?
    # first_time = models.BooleanField(default=True)    Esse campo não será necessário, só lembrar de direcionar users recém registrados para uma tela de engajamento

    game_preferences = models.ManyToManyField(Game)     # Pesquisar diferença entre rel e field

    # Atributos em relacionamento n pra n recursivo
    blocked_players = models.ManyToManyField('self', through='Block', symmetrical=True)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=True)
    # silenced = ?      # players, groups e events

# Tabela usada para reutilizar código, para todas as tabelas que determinem relacionamentos n pra n entre Users
class AbstractRelationshipUsers(DefaultFields):
    '''
    A classe Meta a seguir, usada pelo Django para definir algumas configurações, é usada para
    evitar múltiplos relacionamentos entre as mesmas instâncias.
    Possível troca de nome necessária
    '''
    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["user_1", "user_2"], name="unique_user_to_user"
            )
        ]

    user_1 = models.ForeignKey(User, on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE)

# Tabela intermediária de User em um relacionamento n pra n recursivo
class Friendship(AbstractRelationshipUsers):
    '''
    Quais campos (metadados) podem ser úteis nessa tabela?
    Lembrar que os campos default já estão sendo herdados
    
    O campo active, nesse caso, considerando que o relacionamento é único entre instâncias,
    provavelmente vai ser usado para determinar se a amizade está ativa depois que foi criada.
    O mesmo é válido para as outras tabelas
    '''
    pass

# Seguindo a ideia que eu pesquisei para a tabela de amizades, parece justo também fazer outras tabelas para os outros campos
class Block(AbstractRelationshipUsers):
    '''
    No momento me parece que praticamente todos os atributos que são necessários para uma tabela intermediária
    já foram herdados de AbstractRelationshipUsers...
    Talvez dê só para adicionar '...' no final das classes, para sinalizar que está completa
    '''
    pass

# Falta Silenced, porém provavelmente haverá três classes silenced, uma pra cada tipo de objeto.
# Ou duas, considerando que Events e Squads herdam de uma classe abstrata