from rest_framework import viewsets, permissions
from .models import Pais, Conflicto, FuerzaArmada, Arma, Vehiculo, Derribo
from .serializers import (
    PaisSerializer, ConflictoSerializer, FuerzaArmadaSerializer, DerriboSerializer,
    ArmaSerializer, ArmaDetailSerializer, 
    VehiculoSerializer, VehiculoDetailSerializer
)

# --- ViewSets para los modelos de soporte ---

class PaisViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver y listar Países. Solo permite la lectura.
    """
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ConflictoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver y listar Conflictos.
    """
    queryset = Conflicto.objects.all()
    serializer_class = ConflictoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FuerzaArmadaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver y listar Fuerzas Armadas.
    """
    # Optimizamos la consulta para traer el nombre del país relacionado.
    queryset = FuerzaArmada.objects.select_related('pais').all()
    serializer_class = FuerzaArmadaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DerriboViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver y listar Derribos.
    """
    queryset = Derribo.objects.all()
    serializer_class = DerriboSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# --- ViewSets para los modelos principales (con lógica de detalle/lista) ---

class ArmaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Armas que utiliza un serializer diferente para la lista y el detalle.
    """
    # Optimizamos la consulta para traer toda la información relacionada de una vez.
    queryset = Arma.objects.prefetch_related(
        'operadores__pais', 'conflictos_uso', 'multimedia'
    ).select_related('pais_origen').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """
        Decide qué serializer usar.
        - Si la acción es 'list' (pedir el listado completo), usa el serializer simple.
        - Si la acción es 'retrieve' (pedir un objeto específico), usa el serializer de detalle.
        """
        if self.action == 'list':
            return ArmaSerializer
        return ArmaDetailSerializer

class AvionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet que muestra SOLO vehículos de tipo Avión (Caza, Bombardero, etc.).
    """
    queryset = (
        Vehiculo.objects.filter(
            tipo__in=[
                Vehiculo.TipoVehiculo.CAZA,
                Vehiculo.TipoVehiculo.BOMBARDERO,
                Vehiculo.TipoVehiculo.TRANSPORTE
            ]
        )
        .select_related('pais_origen', 'ficha')
        .prefetch_related(
            'operadores__pais',
            'conflictos_uso',
            'multimedia',
            'caracteristicas',
            'armamento',
        )
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return VehiculoSerializer
        return VehiculoDetailSerializer

class HelicopteroViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet que muestra SOLO vehículos de tipo Helicóptero.
    """
    queryset = (
        Vehiculo.objects.filter(
            tipo=Vehiculo.TipoVehiculo.HELICOPTERO_ATAQUE
        )
        .select_related('pais_origen', 'ficha')
        .prefetch_related(
            'operadores__pais',
            'conflictos_uso',
            'multimedia',
            'caracteristicas',
            'armamento',
        )
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return VehiculoSerializer
        return VehiculoDetailSerializer
    
class VehiculoDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Devuelve el vehículo con TODA su información técnica.
    """

    serializer_class = VehiculoDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return (
            Vehiculo.objects
            .select_related('pais_origen', 'ficha')
            .prefetch_related(
                'operadores__pais',
                'conflictos_uso',
                'multimedia',
                'caracteristicas',
                'armamento',
            )
        )
