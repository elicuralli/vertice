from tortoise import fields
from tortoise.models import Model

class Peticion(Model):
    id = fields.IntField(pk=True)
    id_docente = fields.ForeignKeyField("models.Usuario", related_name='peticiones_docente')
    descripcion = fields.CharField(max_length=500)
    estado = fields.CharField(max_length=150)
    id_estudiante = fields.ForeignKeyField("models.Usuario", related_name='peticiones_estudiante')
    id_materia = fields.ForeignKeyField("models.Materia", related_name='peticiones')
    campo = fields.CharField(max_length=10)
    valor = fields.DecimalField(max_digits=4,decimal_places=2, null=True)
    activo = fields.BooleanField(default=True)  # Para borrado lógico

    class Meta:
        table = "peticiones"
        table_description = "Peticiones"