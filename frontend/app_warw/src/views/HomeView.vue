<script setup>
import { RouterLink } from 'vue-router';
import posterArmas from '@/assets/multimedia/poster-armas.jpg';
import posterAviones from '@/assets/multimedia/poster-aviones.jpg';
import posterHelicopteros from '@/assets/multimedia/poster-helicopteros.jpg';
</script>

<template>
  <div class="portal-grid">

    <RouterLink to="/armas" class="category-card">
      <img :src="posterArmas" alt="Armas" class="card-image"/>
      <div class="card-overlay"></div>
      <h2 class="card-title">ARMAS</h2>
    </RouterLink>

    <RouterLink to="/aviones" class="category-card">
      <img :src="posterAviones" alt="Aviones" class="card-image"/>
      <div class="card-overlay"></div>
      <h2 class="card-title">AVIONES</h2>
    </RouterLink>

    <RouterLink to="/helicopteros" class="category-card">
      <img :src="posterHelicopteros" alt="Helicópteros" class="card-image"/>
      <div class="card-overlay"></div>
      <h2 class="card-title">HELICOPTEROS</h2>
    </RouterLink>

  </div>
</template>

<style scoped>
.portal-grid {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-grow: 1;
  gap: 2rem;
  padding: 2rem;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.category-card {
  flex: 1;
  height: 70vh;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: all 0.4s ease;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  transition: background 0.4s ease;
}

.card-title {
  position: absolute;
  bottom: 2rem;
  color: white;
  font-size: 2.5rem;
  text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
  transition: transform 0.4s ease;
}

.category-card:hover {
  border-color: var(--color-accent);
}

.category-card:hover .card-image {
  transform: scale(1.05);
}

.category-card:hover .card-title {
  transform: translateY(-10px);
}
</style>