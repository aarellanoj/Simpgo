from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Ticket(models.Model):
    """Comments"""

    TICKET_STATUS = (
        (1,'Abierto'),
        (2,'En Proceso'),
        (3,'Cerrado'),
        (4,'Re-Abierto'),
        (5,'Esperando por Información'),
    )

    TICKET_PRIORITY = (
        (1,'Alta'),
        (2,'Media'),
        (3,'Baja'),
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
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Creador del Ticket",
    )

    status = models.IntegerField(
        "Estatus del Ticket",
        choices=TICKET_STATUS,
    )

    priority = models.IntegerField(
        "Prioridad del Ticket",
        choices=TICKET_PRIORITY,
    )

    def __str__(self):
        return self.title

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
        return self.name

class Ticket_Actions(models.Model):
    """Comments"""

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
    )

    claimed = models.BooleanField(
        "¿Reclamado?",
        null=True,
        default=False,
    )

    assigned = models.BooleanField(
        "¿Asignado?",
        null=True,
        default=False,
    )

    closed = models.BooleanField(
        "¿Cerrado?",
        null=True,
        default=False,
    )

    re_opened = models.BooleanField(
        "¿Re-Abierto?",
        null=True,
        default=False,
    )

    class Meta:
        verbose_name = "Ticket Action"
        verbose_name_plural = "Ticket Actions"

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
    job_title = models.CharField(
        "Cargo",
        max_length=100,
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

    avatar = models.CharField(
        "Imagen del Perfil",
        max_length=250,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.get_full_name()



















