from django.db import models
from django.core.validators import FileExtensionValidator

class Pais(models.Model):
    """Representa un país productor o usuario de armamento."""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del País")
    bandera = models.ImageField(upload_to='banderas/', blank=True, null=True, verbose_name="Bandera")

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Conflicto(models.Model):
    """Representa un conflicto histórico, como una guerra o una batalla."""
    nombre = models.CharField(max_length=200, unique=True, verbose_name="Nombre del Conflicto")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(blank=True, null=True, verbose_name="Fecha de Fin")
    descripcion = models.TextField(verbose_name="Descripción")

    class Meta:
        verbose_name = "Conflicto"
        verbose_name_plural = "Conflictos"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return self.nombre

class FuerzaArmada(models.Model):
    """Representa una rama militar específica de un país."""
    class Rama(models.TextChoices):
        EJERCITO = 'EJE', 'Ejército'
        ARMADA = 'ARM', 'Armada'
        FUERZA_AEREA = 'FAE', 'Fuerza Aérea'
        MARINES = 'MAR', 'Infantería de Marina'
        OTRA = 'OTR', 'Otra'

    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="fuerzas_armadas")
    nombre = models.CharField(max_length=150, verbose_name="Nombre Oficial")
    rama = models.CharField(max_length=3, choices=Rama.choices)
    logo = models.ImageField(
        upload_to='logos_fuerzas_armadas/', 
        blank=True, 
        null=True,
        verbose_name="Logo/Insignia",
        help_text="Logo o insignia de la fuerza armada"
    )

    class Meta:
        verbose_name = "Fuerza Armada"
        verbose_name_plural = "Fuerzas Armadas"
        unique_together = ('pais', 'nombre')
        ordering = ['pais__nombre', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.pais.nombre})"
    
    @property
    def icono_default(self):
        """Retorna un emoji por defecto según la rama."""
        iconos = {
            self.Rama.EJERCITO: '🪖',
            self.Rama.ARMADA: '⚓',
            self.Rama.FUERZA_AEREA: '✈️',
            self.Rama.MARINES: '🎖️',
            self.Rama.OTRA: '🛡️',
        }
        return iconos.get(self.rama, '🌍')


class Arma(models.Model):
    """Modelo central para todo tipo de armamento de infantería."""
    
    class TipoArma(models.TextChoices):
        RIFLE_ASALTO = 'RA', 'Rifle de Asalto'
        PISTOLA = 'PI', 'Pistola'
        FRANCOTIRADOR = 'FR', 'Rifle de Francotirador'
        ESCOPETA = 'ES', 'Escopeta'
        SUBFUSIL = 'SF', 'Subfusil'
        OTRO = 'OT', 'Otro'

    nombre = models.CharField(max_length=150, unique=True)
    
    tipo = models.CharField(
        max_length=2, 
        choices=TipoArma.choices, 
        default=TipoArma.OTRO,
        help_text="El tipo de arma (ej. Rifle de Asalto)."
    )
    
    pais_origen = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name="armas_disenadas")
    funcionamiento = models.TextField(help_text="Descripción técnica de cómo opera el arma.")
    mecanismos = models.TextField(help_text="Detalles sobre los mecanismos internos (ej. cerrojo rotativo, retroceso de masas).")
    operadores = models.ManyToManyField(FuerzaArmada, blank=True, related_name="arsenal", verbose_name="Fuerzas Armadas que la utilizan")
    conflictos_uso = models.ManyToManyField(Conflicto, blank=True, related_name="armas_utilizadas", verbose_name="Conflictos en donde se utilizó")

    class Meta:
        verbose_name = "Arma"
        verbose_name_plural = "Armas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    """Modelo base para todos los vehículos militares (aviones, cazas, helicópteros, etc.)."""
    class TipoVehiculo(models.TextChoices):
        CAZA = 'CAZ', 'Avión de Caza'
        BOMBARDERO = 'BOM', 'Bombardero'
        HELICOPTERO_ATAQUE = 'HEL', 'Helicóptero de Ataque'
        TRANSPORTE = 'TRA', 'Avión de Transporte'
        TANQUE = 'TAN', 'Tanque'

    nombre = models.CharField(max_length=150, unique=True)
    tipo = models.CharField(max_length=3, choices=TipoVehiculo.choices)
    pais_origen = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name="vehiculos_disenados")
    operadores = models.ManyToManyField(FuerzaArmada, blank=True, related_name="inventario_vehiculos")
    conflictos_uso = models.ManyToManyField(Conflicto, blank=True, related_name="vehiculos_utilizados")

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class RecursoMultimedia(models.Model):
    """Un modelo para gestionar todos los archivos: sonidos, videos de animación, imágenes."""
    class TipoRecurso(models.TextChoices):
        SONIDO_DISPARO = 'SD', 'Sonido de Disparo'
        SONIDO_RECARGA = 'SR', 'Sonido de Recarga'
        ANIMACION_3D = 'A3D', 'Animación 3D'
        IMAGEN_GALERIA = 'IMG', 'Imagen de Galería'

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=3, choices=TipoRecurso.choices)
    archivo = models.FileField(upload_to='recursos_multimedia/', validators=[
        FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'mp4', 'webm', 'jpg', 'png', 'glb'])
    ])
    arma_asociada = models.ForeignKey(Arma, on_delete=models.CASCADE, blank=True, null=True, related_name="multimedia")
    vehiculo_asociado = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, blank=True, null=True, related_name="multimedia")

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nombre}"

class Derribo(models.Model):
    """Registra un evento de derribo, ya sea aire-aire o tierra-aire."""

    vehiculo_victorioso = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True, related_name="derribos_logrados")
    arma_victoriosa = models.ForeignKey(Arma, on_delete=models.SET_NULL, null=True, blank=True, related_name="derribos_logrados")
    vehiculo_derribado = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name="derribos_sufridos")
    conflicto = models.ForeignKey(Conflicto, on_delete=models.CASCADE, related_name="derribos")
    fecha = models.DateField()
    descripcion = models.TextField(help_text="Detalles y relato del derribo.")
    
    class Meta:
        verbose_name = "Derribo"
        verbose_name_plural = "Derribos"
        ordering = ['-fecha']
    
    def __str__(self):
        victorioso = self.vehiculo_victorioso or self.arma_victoriosa
        return f"Derribo en {self.conflicto.nombre}: {victorioso} vs {self.vehiculo_derribado}"

class VehiculoFichaTecnica(models.Model):
    vehiculo = models.OneToOneField(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name="ficha"
    )

    primer_vuelo = models.DateField(null=True, blank=True)
    entrada_servicio = models.CharField(max_length=100, blank=True)

    descripcion = models.TextField(blank=True)

    # Dimensiones
    longitud = models.CharField(max_length=50, blank=True)
    altura = models.CharField(max_length=50, blank=True)
    envergadura = models.CharField(max_length=50, blank=True)
    superficie_alar = models.CharField(max_length=50, blank=True)

    # Pesos
    peso_vacio = models.CharField(max_length=50, blank=True)
    peso_maximo = models.CharField(max_length=50, blank=True)

    # Performance
    velocidad_maxima = models.CharField(max_length=50, blank=True)
    alcance = models.CharField(max_length=50, blank=True)
    techo_servicio = models.CharField(max_length=50, blank=True)

    # Propulsión
    motor = models.CharField(max_length=150, blank=True)

    # Otros
    tripulacion = models.CharField(max_length=100, blank=True)
    costo_unitario = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Ficha técnica de {self.vehiculo.nombre}"

class VehiculoCaracteristica(models.Model):
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name="caracteristicas"
    )

    categoria = models.CharField(max_length=100)  # "Radar", "Aviónica", etc.
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.categoria} - {self.vehiculo.nombre}"

class VehiculoArmamento(models.Model):

    class Tipo(models.TextChoices):
        AIRE_AIRE = "AA", "Aire-Aire"
        AIRE_TIERRA = "AT", "Aire-Tierra"
        ANTIRADAR = "AR", "Antiradar"
        CANON = "CA", "Cañón"
        OTRO = "OT", "Otro"

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name="armamento"
    )

    tipo = models.CharField(max_length=2, choices=Tipo.choices)
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
