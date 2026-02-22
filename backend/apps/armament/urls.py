# backend/apps/armament/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaisViewSet, ConflictoViewSet, FuerzaArmadaViewSet, DerriboViewSet,
    ArmaViewSet, AvionViewSet, HelicopteroViewSet, VehiculoDetailViewSet
)

router = DefaultRouter()

router.register(r'paises', PaisViewSet, basename='pais')
router.register(r'conflictos', ConflictoViewSet, basename='conflicto')
router.register(r'fuerzas-armadas', FuerzaArmadaViewSet, basename='fuerza-armada')
router.register(r'derribos', DerriboViewSet, basename='derribo')
router.register(r'armas', ArmaViewSet, basename='arma')
router.register(r'aviones', AvionViewSet, basename='avion')
router.register(r'helicopteros', HelicopteroViewSet, basename='helicoptero')
router.register(r'vehiculos', VehiculoDetailViewSet, basename='vehiculo-detail')
urlpatterns = [
    path('', include(router.urls)),
]