from django.db import models
from django.contrib.auth import get_user_model
from core.models import DefaultFields

# Dá pra pensar em extender django.db.models pra acrescentar creator, modified e created em todos os models, como no bubble
class Message(DefaultFields):
    '''
    content = models.TextField()
    edited = models.BooleanField()                      # É possível não utilizar esse campo, ou usar @property
    message_type = models.TextChoices()                 # Conversa, alerta, block, sair do grupo...
    receiver = models.ManyToOneRel(get_user_model())    # No caso de mensagem em um grupo (não sei se mensagens de grupo estarão no chat mesmo...)
    
    replied_message = models.ManyToOneRel()             # Uma vez que a mensagem não será apagada, só inativada, pode ser feito desse jeito
                                                        # Não consegui colocar Message dentro de ManyToOne, mas essa é a ideia
    '''
    pass
