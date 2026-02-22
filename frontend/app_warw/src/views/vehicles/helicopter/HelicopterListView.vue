<script setup>
import { onMounted } from 'vue';
import { useVehicleStore } from '@/stores/vehicles';
import { RouterLink } from 'vue-router';

const vehicleStore = useVehicleStore();

onMounted(() => {
  vehicleStore.fetchHelicopters();
});

const getVehicleImage = (vehicle) => {
  if (!vehicle.multimedia || vehicle.multimedia.length === 0) return null;
  const image = vehicle.multimedia.find(m => m.tipo === 'Imagen de Galería');
  return image ? image.archivo : null;
}
</script>

<template>
  <div class="container">
    <header class="page-header">
      <h1>Galería de Helicópteros</h1>
      <p>Explora todos los modelos de helicópteros disponibles.</p>
    </header>

    <div v-if="vehicleStore.loading" class="loading-state">Cargando escuadrón...</div>
    <div v-if="vehicleStore.error" class="error-state">{{ vehicleStore.error }}</div>

    <div v-if="!vehicleStore.loading && vehicleStore.helicopters.length" class="helicopter-grid">
      <RouterLink 
        v-for="helicopter in vehicleStore.helicopters" 
        :key="helicopter.id" 
        :to="`/vehiculo/${helicopter.id}`"
        class="helicopter-card"
      >
        <div class="helicopter-card-image-wrapper">
          <img v-if="getVehicleImage(helicopter)" :src="getVehicleImage(helicopter)" :alt="helicopter.nombre" class="helicopter-card-image" loading="lazy">
          <div v-else class="helicopter-card-image-placeholder">Sin Imagen</div>
        </div>
        <div class="helicopter-card-content">
          <h3>{{ helicopter.nombre }}</h3>
          <p>{{ helicopter.tipo }}</p>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.container {
  padding: 0 1rem;
}
.page-header { text-align: center; margin-bottom: 3rem; }
.page-header h1 { font-size: 2.5rem; }
.page-header p { font-size: 1.125rem; color: var(--color-text-muted); }
.helicopter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
.helicopter-card {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  display: block;
  color: var(--color-text);
  background-color: var(--color-surface);
  text-decoration: none;

  transition: 
    transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), 
    box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1),
    border-color 0.3s ease;
}
.helicopter-card:hover {
  transform: scale(1.02);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 1);
  border-color: var(--color-accent);
}
.helicopter-card-image-wrapper {
  width: 100%;
  height: 200px;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}
.helicopter-card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.helicopter-card-image-placeholder {
  color: var(--color-text-muted);
}
.helicopter-card-content {
  padding: 1rem;
}
.helicopter-card-content h3 {
  margin-bottom: 0.25rem;
  text-decoration: none;
  color: var(--color-text);
  transition: color 0.3s ease;
}
.helicopter-card:hover .weapon-card-content h3 {
  color: var(--color-accent);
}
.helicopter-card-content p {
  color: var(--color-text-muted);
}
.loading-state, .error-state {
  text-align: center;
  padding: 3rem;
  font-size: 1.25rem;
  color: var(--color-text-muted);
}
.loading-state, .error-state { 
  text-align: center;
  padding: 3rem;
  font-size: 1.25rem;
  color: var(--color-text-muted); }
</style>
