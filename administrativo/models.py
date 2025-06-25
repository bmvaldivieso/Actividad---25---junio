from django.db import models

# Create your models here.

class Estudiante(models.Model):
    opciones_tipo_estudiante = (
        ('becado', 'Estudiante Becado'),
        ('no-becado', 'Estudiante No Becado'),
        )

    nombre = models.CharField("Nombre de estudiante", max_length=30)
    apellido = models.CharField(max_length=30)
    cedula = models.CharField(max_length=30, unique=True)
    edad = models.IntegerField("edad de estudiante") # Verbose field names
    tipo_estudiante = models.CharField(max_length=30, \
            choices=opciones_tipo_estudiante)
    modulos = models.ManyToManyField('Modulo', through='Matricula')


    def __str__(self):
        return "%s - %s - %s - edad: %d - tipo: %s" % (self.nombre,
                self.apellido,
                self.cedula,
                self.edad,
                self.tipo_estudiante)

    def obtener_matriculas(self):
        return self.lasmatriculas.all()

    def resumen_matriculas(self):
        """
        Devuelve un resumen con los módulos en los que el estudiante está inscrito,
        incluyendo los nombres de los módulos y el costo total.
        """
        modulos = []  # Lista para guardar (nombre del módulo, costo)
        total = 0     # Acumulador del costo total

        # Recorre todas las matrículas del estudiante, incluyendo los datos del módulo relacionado
        for matricula in self.lasmatriculas.select_related('modulo'):
            modulos.append((matricula.modulo.nombre, matricula.modulo.costo))
            total += matricula.modulo.costo

        # Devuelve un diccionario con toda la información resumida
        return {
            'estudiante': self,
            'modulos': modulos,
            'total': total
        }   
        
class Modulo(models.Model):
    """
    """
    opciones_modulo = (
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),
        ('4', 'Cuarto'),
        ('5', 'Quinto'),
        ('6', 'Sexto'),
        )

    nombre = models.CharField(max_length=30, \
            choices=opciones_modulo)
    estudiantes = models.ManyToManyField(Estudiante, through='Matricula')
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "Módulo: %s" % (self.nombre)


class Matricula(models.Model):
    """
    """
    estudiante = models.ForeignKey(Estudiante, related_name='lasmatriculas',
            on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, related_name='lasmatriculas',
            on_delete=models.CASCADE)
    comentario = models.CharField(max_length=200)

    def __str__(self):
        return "Matricula: Estudiante(%s) - Modulo(%s)" % \
                (self.estudiante, self.modulo.nombre)
