from rest_framework import serializers
from .models import (
    Pais, Conflicto, FuerzaArmada, Arma, Vehiculo, RecursoMultimedia, Derribo, VehiculoFichaTecnica, VehiculoArmamento,
    VehiculoCaracteristica
)

# --- Serializadores de Soporte y Simples ---

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ['id', 'nombre', 'bandera']

class ConflictoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conflicto
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'descripcion']

class FuerzaArmadaSerializer(serializers.ModelSerializer):
    # Mostramos el nombre del país en lugar de su ID para mayor claridad.
    icono_default = serializers.ReadOnlyField()
    pais = serializers.StringRelatedField() 
    
    class Meta:
        model = FuerzaArmada
        fields = ['id', 'nombre', 'rama', 'logo', 'icono_default', 'pais']

class RecursoMultimediaSerializer(serializers.ModelSerializer):
    # Muestra el nombre legible del tipo de recurso (ej. "Sonido de Disparo")
    tipo = serializers.CharField(source='get_tipo_display') 

    class Meta:
        model = RecursoMultimedia
        fields = ['id', 'nombre', 'tipo', 'archivo']


# --- Serializadores de Lista (Para vistas generales y rápidas) ---

class ArmaSerializer(serializers.ModelSerializer):
    """
    Versión ligera para listas. Muestra nombres en lugar de objetos completos.
    """
    pais_origen = serializers.StringRelatedField()
    tipo = serializers.CharField(source='get_tipo_display')
    multimedia = RecursoMultimediaSerializer(many=True, read_only=True)

    class Meta:
        model = Arma
        fields = ['id', 'nombre', 'tipo', 'pais_origen', 'multimedia']

class VehiculoSerializer(serializers.ModelSerializer):
    """
    Versión ligera para listas.
    """
    pais_origen = serializers.StringRelatedField()
    tipo = serializers.CharField(source='get_tipo_display')
    multimedia = RecursoMultimediaSerializer(many=True, read_only=True)

    class Meta:
        model = Vehiculo
        fields = ['id', 'nombre', 'tipo', 'pais_origen', 'multimedia']


class ArmaDetailSerializer(serializers.ModelSerializer):
    """
    Versión completa para la vista de detalle de un arma. Anida otros serializadores.
    """
    pais_origen = PaisSerializer(read_only=True)
    tipo = serializers.CharField(source='get_tipo_display')
    operadores = FuerzaArmadaSerializer(many=True, read_only=True)
    conflictos_uso = ConflictoSerializer(many=True, read_only=True)
    multimedia = RecursoMultimediaSerializer(many=True, read_only=True)

    class Meta:
        model = Arma
        # Incluimos todos los campos del modelo y los campos anidados que definimos arriba.
        # --- ASEGÚRATE DE QUE 'tipo' ESTÉ EN ESTA LISTA ---
        fields = [
            'id', 'nombre', 'tipo', 'pais_origen', 'funcionamiento', 'mecanismos', 
            'operadores', 'conflictos_uso', 'multimedia'
        ]


class VehiculoFichaTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiculoFichaTecnica
        fields = "__all__"


class VehiculoCaracteristicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiculoCaracteristica
        fields = "__all__"


class VehiculoArmamentoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)

    class Meta:
        model = VehiculoArmamento
        fields = ["id", "tipo", "tipo_display", "nombre"]


class VehiculoDetailSerializer(serializers.ModelSerializer):
    """
    Versión completa para la vista de detalle de un vehículo.
    """

    pais_origen = PaisSerializer(read_only=True)
    operadores = FuerzaArmadaSerializer(many=True, read_only=True)
    conflictos_uso = ConflictoSerializer(many=True, read_only=True)
    multimedia = RecursoMultimediaSerializer(many=True, read_only=True)

    # 🔥 NUEVO
    ficha = VehiculoFichaTecnicaSerializer(read_only=True)
    caracteristicas = VehiculoCaracteristicaSerializer(many=True, read_only=True)
    armamento = VehiculoArmamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Vehiculo
        fields = [
            'id',
            'nombre',
            'tipo',
            'pais_origen',
            'operadores',
            'conflictos_uso',
            'multimedia',
            'ficha',
            'caracteristicas',
            'armamento',
        ]

class DerriboSerializer(serializers.ModelSerializer):
    """
    Serializador para los eventos de derribo. Muestra toda la información de forma clara.
    """
    # Usamos StringRelatedField para mostrar los nombres de los involucrados.
    vehiculo_victorioso = serializers.StringRelatedField()
    arma_victoriosa = serializers.StringRelatedField()
    vehiculo_derribado = serializers.StringRelatedField()
    conflicto = serializers.StringRelatedField()

    class Meta:
        model = Derribo
        fields = '__all__'
