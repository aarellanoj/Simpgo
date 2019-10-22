from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

#Functions
def to_who():
    staff = Profile.objects.filter(rank=2,department=taldepartamento)
    band = True
    winner = dict()

    for worker in staff:
        #Filtramos por Trabajador, por el Tipo de Prioridad y El Estatus
        worker_tickets = Ticket.objects.filter(assigned_to=worker.id,
                                               priority=self.priority,
                                               status__in=[1,2])
        how_many = len(worker_tickets)

        if band:
            winner['worker'] = worker
            winner['how_many'] = how_many
            band = False 
        elif how_many > winner['how_many']:
            winner['worker'] = worker
            winner['how_many'] = how_many

    return winner['worker']

# Create your models here.

class Management(models.Model):
    """Comments"""

    name = models.CharField(
        "Nombre de la Direccion",
        max_length=100,
    )

    def __str__(self):
        return self.name

class Department(models.Model):
    """Comments"""

    name = models.CharField(
        "Nombre del Departamento",
        max_length=100,
    )

    management = models.ForeignKey(
        Management,
        on_delete=models.CASCADE,
        verbose_name="Dirección a la que Pertenece",
    )

    def __str__(self):
        return self.name + " -> " + self.management.name 

class Rank(models.Model):
    """Comments"""

    title = models.CharField(
        "Rango en el Sistema",
        max_length=100,
    )

    def __str__(self):
        return self.title


class Job_Titles(models.Model):
    """Comments"""

    IMPORTANCE = (
        (3,'Alto'),
        (2,'Medio'),
        (1,'Bajo'),
    )

    job_title = models.CharField(
        "Cargo",
        max_length=100,
    )

    importance = models.IntegerField(
        "Importancia",
        choices=IMPORTANCE,
    )

    class Meta:
        verbose_name = "Job Title"
        verbose_name_plural = "Job Titles"

    def __str__(self):
        return self.job_title


DEFAULT_RANK_ID = 1
class Profile(models.Model):
    """Comments"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name="Departamento al que Pertenece",
    )

    job_title = models.ForeignKey(
        Job_Titles,
        on_delete=models.CASCADE,
        verbose_name="Cargo dentro de la Organización",
    )

    rank = models.ForeignKey(
        Rank,
        on_delete=models.CASCADE,
        default=DEFAULT_RANK_ID,
        verbose_name="Rango en el Sistema",
    )

    avatar = models.ImageField(
        "Imagen del Perfil",
        max_length=250,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.get_full_name()

class Description(models.Model):
    """Comments"""

    IMPORTANCE = (
        (3,'Alta'),
        (2,'Media'),
        (1,'Baja'),
    )

    description = models.CharField(
        "Descripción",
        max_length=250,
    )

    importance = models.IntegerField(
        "Importancia",
        choices=IMPORTANCE,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name="Departamento al que Pertenece",
    )

    def __str__(self):
        return self.description

DEFAULT_STATUS = 1
DEFAULT_PRIORITY = 0
class Ticket(models.Model):
    """Comments"""

    TICKET_STATUS = (
        (1,'Abierto'),
        (2,'En Proceso'),
        (3,'Cerrado'),
        (4,'Rechazado'),
    )

    TICKET_PRIORITY = (
        (0,'Sin Asignar'),
        (1,'Baja'),
        (2,'Media'),
        (3,'Alta'),
    )

    title = models.CharField(
        "Titulo del Ticket",
        max_length=100,
    )

    content = models.TextField(
        "Contenido del Ticket",
        max_length=1000,
    )

    created = models.DateTimeField(
        "Momento en el que fue Creado",
        auto_now_add=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Creador del Ticket",
    )

    status = models.IntegerField(
        "Estatus del Ticket",
        choices=TICKET_STATUS,
        default=DEFAULT_STATUS,
    )

    priority = models.IntegerField(
        "Prioridad del Ticket",
        choices=TICKET_PRIORITY,
        default=DEFAULT_PRIORITY,
    )

    description = models.ForeignKey(
        Description,
        on_delete=models.CASCADE,
        verbose_name="Descripción del Ticket",
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    image_file = models.ImageField(
        "Imagen",
        max_length=250,
        null=True,
        blank=True,
    )

    deleted = models.BooleanField(
        "Eliminar Ticket",
        default=False,
    )

    def _change_status_to(self,new_status,*args, **kwargs):
        self.status = new_status
        return super(Ticket, self).save(*args,**kwargs)

    def _remove(self,*args, **kwargs):
        self.deleted = True
        self.status = 3
        return super(Ticket, self).save(*args,**kwargs)

    def _assign_priority(self,*args,**kwargs):
        prio_job = self.created_by.profile.job_title.importance
        prio_des = self.description.importance
        imp = prio_job + prio_des

        if imp > 4:
            self.priority = 3
        elif imp > 2:
            self.priority = 2
        else:
            self.priority = 1

        return super(Ticket, self).save(*args,**kwargs)

    def _assign_ticket(self,*args,**kwargs):
        staff = Profile.objects.filter(rank=2,department=self.description.department)
        band = True
        winner = dict()

        for worker in staff:
            #Filtramos por Trabajador, por el Tipo de Prioridad y El Estatus
            worker_tickets = Ticket.objects.filter(assigned_to=worker.user.id,
                                                   priority=self.priority,
                                                   status__in=[1,2],
                                                   deleted=0)
            how_many = len(worker_tickets)

            if band:
                winner['worker'] = worker
                winner['how_many'] = how_many
                band = False 
            elif how_many < winner['how_many']:
                winner['worker'] = worker
                winner['how_many'] = how_many

        self.assigned_to = winner['worker'].user
        return super(Ticket, self).save(*args,**kwargs)

    def __str__(self):
        return self.title

class Subscribe(models.Model):
    """Comments"""

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        verbose_name="Ticket",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Subscriptor",
    )

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return self.user.get_full_name() + " - " + self.ticket.title

class Response(models.Model):
    """Comments"""

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        verbose_name="Ticket Asociado",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Usuario que Responde",
    )

    response = models.TextField(
        "Contenido de la Respuesta",
        max_length=1000,
    )

    image_file = models.ImageField(
        "Imagen",
        max_length=250,
        null=True,
        blank=True,
    )

class Ticket_Actions(models.Model):
    """Comments"""

    TICKET_ACTIONS = (
        (1,'Abierto'),
        (2,'En Proceso'),
        (3,'Cerrado'),
        (4,'Rechazado')
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        verbose_name="Ticket",
    )

    action_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Usuario que realiza la Acción",
    )

    date = models.DateTimeField(
        "Fecha de la Acción",
        auto_now_add=True,
    )

    action = models.IntegerField(
        "Acción del Ticket",
        choices=TICKET_ACTIONS,
    )

    class Meta:
        verbose_name = "Ticket Action"
        verbose_name_plural = "Ticket Actions"