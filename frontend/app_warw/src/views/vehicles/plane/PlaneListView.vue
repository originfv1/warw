<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useVehicleStore } from '@/stores/vehicles';

// Importar imágenes del modal (alta calidad)
import a10Img from '@/assets/aviones-modal/a-10-modal.png';
import b52Img from '@/assets/aviones-modal/b52-modal.png';
import eurofighterImg from '@/assets/aviones-modal/eurofighter-modal.png';
import f14Img from '@/assets/aviones-modal/f-14-modal.png';
import f15Img from '@/assets/aviones-modal/f-15-modal.png';
import f16Img from '@/assets/aviones-modal/f-16-modal.png';
import f18Img from '@/assets/aviones-modal/f-18-modal.png';
import f22Img from '@/assets/aviones-modal/f-22-modal.png';
import f35Img from '@/assets/aviones-modal/f-35-modal.png';
import mig29Img from '@/assets/aviones-modal/mig-29-modal.png';
import su27Img from '@/assets/aviones-modal/su-27-modal.png';
import su35Img from '@/assets/aviones-modal/su-35-modal.png';

const vehicleStore = useVehicleStore();
const isDialogOpen = ref(false);
const activeTab = ref('specs');

onMounted(() => {
  vehicleStore.fetchPlanes();

  const handleEsc = (e) => {
    if (e.key === "Escape" && isDialogOpen.value) closeVehicleDialog();
  };

  window.addEventListener("keydown", handleEsc);
  onUnmounted(() => window.removeEventListener("keydown", handleEsc));
});

const openVehicleDialog = async (plane) => {
  isDialogOpen.value = true;
  activeTab.value = 'specs';
  await vehicleStore.fetchVehicleById(plane.id);
};

const closeVehicleDialog = () => {
  isDialogOpen.value = false;
  vehicleStore.currentVehicle = null;
};

const vehicle = computed(() => vehicleStore.currentVehicle);
const ficha = computed(() => vehicle.value?.ficha || {});
const armamentoBackend = computed(() => vehicle.value?.armamento || []);
const caracteristicas = computed(() => vehicle.value?.caracteristicas || []);

/* === MAPEO DE IMÁGENES DEL MODAL === */
const modalVehicleImages = {
  2: f16Img,
  3: null,
  4: b52Img,
  7: null,
  9: eurofighterImg,
  14: f18Img,
  16: f15Img,
  17: f22Img,
  19: a10Img,
  21: f35Img,
  22: mig29Img,
  25: null,
  29: su27Img,
  30: su35Img,
  31: f14Img,
};

/* === IMAGEN PARA TARJETAS (de la BD) === */
const getVehicleImage = (vehicle) => {
  if (!vehicle.multimedia || vehicle.multimedia.length === 0) return null;
  const image = vehicle.multimedia.find(m => m.tipo === 'Imagen de Galería');
  return image ? image.archivo : null;
};

/* === IMAGEN PARA MODAL (assets locales) === */
const getModalVehicleImage = (vehicle) => {
  return modalVehicleImages[vehicle.id] || null;
};

/* === DIMENSIONES === */
const dimensions = computed(() => [
  { label: "Longitud", value: ficha.value.longitud ? `${ficha.value.longitud} m` : "—" },
  { label: "Altura", value: ficha.value.altura ? `${ficha.value.altura} m` : "—" },
  { label: "Envergadura", value: ficha.value.envergadura ? `${ficha.value.envergadura} m` : "—" },
  { label: "Superficie Alar", value: ficha.value.superficie_alar ? `${ficha.value.superficie_alar} m²` : "—" },
  { label: "Peso Vacío", value: ficha.value.peso_vacio ? `${ficha.value.peso_vacio.toLocaleString()} kg` : "—" },
  { label: "Peso Máximo", value: ficha.value.peso_maximo ? `${ficha.value.peso_maximo.toLocaleString()} kg` : "—" },
  { label: "Tripulación", value: ficha.value.tripulacion ? `${ficha.value.tripulacion} persona(s)` : "—" }
]);

/* === CARACTERÍSTICAS === */
const features = computed(() => {
  return caracteristicas.value.map(c => ({
    label: c.categoria,
    value: c.descripcion
  }));
});

/* === ARMAMENTO === */
const armament = computed(() => {
  const grouped = {};
  armamentoBackend.value.forEach(item => {
    const tipo = item.tipo_display || item.tipo;
    if (!grouped[tipo]) grouped[tipo] = { type: tipo, systems: [] };
    if (!grouped[tipo].systems.includes(item.nombre)) {
      grouped[tipo].systems.push(item.nombre);
    }
  });
  return Object.values(grouped);
});

const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });
};

/* === Helper para mostrar nombre de rama === */
const getRamaName = (ramaCode) => {
  const ramas = {
    'EJE': 'Ejército',
    'ARM': 'Armada',
    'FAE': 'Fuerza Aérea',
    'MAR': 'Infantería de Marina',
    'OTR': 'Otra'
  };
  return ramas[ramaCode] || ramaCode;
};
</script>

<template>
  <div class="container">
    <header class="page-header">
      <h1>Galería de Aviones</h1>
      <p>Explora todos los modelos de aeronaves disponibles.</p>
    </header>

    <div v-if="vehicleStore.loading" class="loading-state">Cargando flota...</div>
    <div v-if="vehicleStore.error" class="error-state">{{ vehicleStore.error }}</div>
    
    <div v-if="!vehicleStore.loading && vehicleStore.planes.length" class="plane-grid">
      <div v-for="plane in vehicleStore.planes" :key="plane.id" @click="openVehicleDialog(plane)" class="plane-card">
        <div class="plane-card-image-wrapper">
          <img v-if="getVehicleImage(plane)" :src="getVehicleImage(plane)" :alt="plane.nombre" class="plane-card-image" loading="lazy">
          <div v-else class="plane-card-image-placeholder">Sin Imagen</div>
        </div>
        <div class="plane-card-content">
          <h3>{{ plane.nombre }}</h3>
          <p>{{ plane.tipo }}</p>
        </div>
      </div>
    </div>

    <!-- DIALOG CON IMAGEN -->
    <div v-if="isDialogOpen" class="dialog-overlay" @click="closeVehicleDialog">
      <div class="dialog-content-split" @click.stop>
        <button class="close-btn" @click="closeVehicleDialog">✕</button>

        <div v-if="vehicleStore.loading" class="dialog-loading">Cargando detalles...</div>
        <div v-else-if="vehicleStore.error" class="dialog-error">{{ vehicleStore.error }}</div>

        <div v-else-if="vehicle" class="dialog-split-container">
          
          <!-- IMAGEN IZQUIERDA -->
          <div class="dialog-left-image">
            <img 
              v-if="getModalVehicleImage(vehicle)" 
              :src="getModalVehicleImage(vehicle)" 
              :alt="vehicle.nombre"
              class="aircraft-full-image"
            >
            <div v-else class="no-image-placeholder">
              <span class="plane-icon-large">✈️</span>
              <p>Sin imagen disponible</p>
            </div>
          </div>

          <!-- CONTENIDO DERECHO -->
          <div class="dialog-right-content">
            <article class="item-detail">
              
              <header class="detail-header">
                <div class="header-content">
                  <div class="header-top">
                    <span class="badge">{{ vehicle.tipo }}</span>
                    <img v-if="vehicle.pais_origen?.bandera" :src="vehicle.pais_origen.bandera" :alt="vehicle.pais_origen.nombre" class="flag-icon">
                  </div>
                  <h1>{{ vehicle.nombre }}</h1>
                  <div class="subtitle">
                    <span>{{ vehicle.tipo }}</span>
                    <span class="separator">|</span>
                    <span v-if="vehicle.pais_origen">{{ vehicle.pais_origen.nombre }}</span>
                  </div>
                  
                  <div class="header-meta" v-if="ficha">
                    <div class="meta-item" v-if="ficha.primer_vuelo">
                      <span class="meta-icon">📅</span>
                      <span>Primer vuelo: {{ ficha.primer_vuelo }}</span>
                    </div>
                    <div class="meta-item" v-if="ficha.entrada_servicio">
                      <span class="meta-icon">🛡️</span>
                      <span>
                        En servicio: {{ ficha.entrada_servicio }}
                        <template v-if="ficha.retiro"> - {{ ficha.retiro }}</template>
                        <template v-else> - Presente</template>
                      </span>
                    </div>
                  </div>
                </div>
              </header>

              <div class="tabs">
                <div class="tabs-list">
                  <button @click="activeTab = 'specs'" :class="['tab-button', { active: activeTab === 'specs' }]">Especificaciones</button>
                  <button v-if="vehicle.operadores?.length" @click="activeTab = 'operators'" :class="['tab-button', { active: activeTab === 'operators' }]">Operadores</button>
                  <button v-if="vehicle.conflictos_uso?.length" @click="activeTab = 'combat'" :class="['tab-button', { active: activeTab === 'combat' }]">Conflictos</button>
                  <button @click="activeTab = 'armament'" :class="['tab-button', { active: activeTab === 'armament' }]">Armamento</button>
                </div>

                <div v-if="activeTab === 'specs'" class="tab-content">
                  <div class="info-grid">
                    <section class="section">
                      <h3 class="section-title">Dimensiones y Pesos</h3>
                      <dl class="dimensions-list">
                        <div v-for="dim in dimensions" :key="dim.label" class="dimension-item">
                          <dt class="dimension-label">{{ dim.label }}</dt>
                          <dd class="dimension-value">{{ dim.value }}</dd>
                        </div>
                      </dl>
                    </section>

                    <section class="section">
                      <h3 class="section-title">Características Técnicas</h3>
                      <div class="features-list">
                        <div v-for="feat in features" :key="feat.label + feat.value" class="feature-item">
                          <span class="feature-badge">{{ feat.label }}</span>
                          <span class="feature-value">{{ feat.value }}</span>
                        </div>
                      </div>
                    </section>
                  </div>
                </div>

                <!-- OPERATORS TAB - CON LOGO DE FUERZA ARMADA -->
                <div v-if="activeTab === 'operators'" class="tab-content">
                  <section class="section">
                    <h3 class="section-title">Operadores</h3>
                    <ul class="operators-list">
                      <li v-for="op in vehicle.operadores" :key="op.id" class="operator-item">
                        <div class="operator-info">
                          <!-- Logo si existe -->
                          <img 
                            v-if="op.logo" 
                            :src="op.logo" 
                            :alt="op.nombre"
                            class="operator-logo"
                            :title="op.nombre"
                          >
                          <!-- Icono por defecto si no hay logo -->
                          <span 
                            v-else 
                            class="operator-icon"
                            :title="`${op.nombre} - ${getRamaName(op.rama)}`"
                          >
                            {{ op.icono_default || '🌍' }}
                          </span>
                          
                          <div>
                            <p class="operator-name">{{ op.nombre }}</p>
                            <p class="operator-detail" v-if="op.pais">{{ op.pais }}</p>
                            <p class="operator-detail" v-if="op.rama">
                              Rama: {{ getRamaName(op.rama) }}
                            </p>
                          </div>
                        </div>
                      </li>
                    </ul>
                  </section>
                </div>

                <div v-if="activeTab === 'combat'" class="tab-content">
                  <section class="section">
                    <h3 class="section-title">Conflictos</h3>
                    <ul class="conflicts-list">
                      <li v-for="c in vehicle.conflictos_uso" :key="c.id" class="conflict-item">
                        <h4 class="conflict-name">{{ c.nombre }}</h4>
                        <span class="conflict-date">{{ formatDate(c.fecha_inicio) }} - {{ c.fecha_fin ? formatDate(c.fecha_fin) : 'Actualidad' }}</span>
                        <p class="conflict-description" v-if="c.descripcion">{{ c.descripcion }}</p>
                      </li>
                    </ul>
                  </section>
                </div>

                <div v-if="activeTab === 'armament'" class="tab-content">
                  <section class="section">
                    <h3 class="section-title">Armamento</h3>
                    <div class="armament-grid">
                      <div v-for="category in armament" :key="category.type" class="armament-category">
                        <h4 class="category-title">{{ category.type }}</h4>
                        <div class="systems-list">
                          <span v-for="sys in category.systems" :key="sys" class="system-badge">{{ sys }}</span>
                        </div>
                      </div>
                    </div>
                  </section>
                </div>

              </div>
            </article>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ===== BASE ===== */
.container { padding: 0 1rem; }
.page-header { text-align: center; margin-bottom: 3rem; }
.page-header h1 { font-size: 2.5rem; }
.page-header p { font-size: 1.125rem; color: var(--color-text-muted); }

/* ===== PLANE GRID ===== */
.plane-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
.plane-card { border: 1px solid var(--color-border); border-radius: 8px; overflow: hidden; display: block; color: var(--color-text); background-color: var(--color-surface); text-decoration: none; cursor: pointer; transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), border-color 0.3s ease; }
.plane-card:hover { transform: scale(1.02); box-shadow: 0 12px 24px rgba(0, 0, 0, 1); border-color: var(--color-accent); }
.plane-card-image-wrapper { width: 100%; height: 200px; background-color: #f8f9fa; display: flex; align-items: center; justify-content: center; }
.plane-card-image { width: 100%; height: 100%; object-fit: cover; }
.plane-card-image-placeholder { color: var(--color-text-muted); }
.plane-card-content { padding: 1rem; }
.plane-card-content h3 { margin-bottom: 0.25rem; color: var(--color-text); transition: color 0.3s ease; }
.plane-card:hover .plane-card-content h3 { color: var(--color-accent); }
.plane-card-content p { color: var(--color-text-muted); }
.loading-state, .error-state { text-align: center; padding: 3rem; font-size: 1.25rem; color: var(--color-text-muted); }

/* ===== DIALOG SPLIT ===== */
.dialog-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.dialog-content-split {
  background: white;
  border-radius: 12px;
  width: 95%;
  max-width: 1600px;
  height: 90vh;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease;
}

.close-btn {
  position: absolute;
  top: 20px; right: 20px;
  background: white;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  transition: all 0.2s;
  z-index: 100;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
}

.close-btn:hover {
  color: #ff4444;
  background: #f8f9fa;
  transform: scale(1.1);
}

.dialog-split-container {
  display: flex;
  height: 100%;
  overflow: hidden;
}

/* LADO IZQUIERDO - Imagen */
.dialog-left-image {
  width: 50%;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
}

/* LADO DERECHO - Contenido */
.dialog-right-content {
  width: 50%;
  overflow-y: auto;
  padding: 30px;
  background: white;
}

/* IMAGEN SIN ANIMACIÓN */
.aircraft-full-image {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  filter: drop-shadow(0 25px 50px rgba(0,0,0,0.4));
}

.no-image-placeholder {
  text-align: center;
  color: #94a3b8;
}

.plane-icon-large {
  font-size: 10rem;
  opacity: 0.3;
  display: block;
  margin-bottom: 1.5rem;
  filter: grayscale(100%);
}

.no-image-placeholder p {
  font-size: 1.25rem;
  opacity: 0.7;
}

/* Item detail */
.item-detail { font-family: 'Segoe UI', system-ui, sans-serif; }
.detail-header { margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 2px solid #e2e8f0; }
.header-top { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.plane-icon { font-size: 2.5rem; }
.flag-icon { width: 28px; height: 18px; }
.badge { padding: 5px 14px; background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 0.8rem; font-weight: 600; }
.header-content h1 { font-size: 2.2rem; margin: 0 0 0.5rem 0; color: #2c3e50; font-weight: 700; }
.subtitle { color: #7f8c8d; font-size: 1.05rem; }
.separator { margin: 0 0.5rem; opacity: 0.7; }
.header-meta { display: flex; flex-wrap: wrap; gap: 16px; margin-top: 15px; font-size: 0.9rem; }
.meta-item { display: flex; align-items: center; gap: 8px; }
.meta-icon { font-size: 1rem; }

/* Tabs */
.tabs { margin-top: 2rem; }
.tabs-list { display: flex; gap: 6px; border-bottom: 2px solid #e2e8f0; margin-bottom: 2rem; flex-wrap: wrap; }
.tab-button { padding: 10px 16px; background: none; border: none; border-bottom: 3px solid transparent; cursor: pointer; color: #64748b; font-size: 0.9rem; font-weight: 600; display: flex; align-items: center; gap: 8px; transition: all 0.2s; }
.tab-button:hover { color: #3b82f6; background: #f8fafc; }
.tab-button.active { color: #3b82f6; border-bottom-color: #3b82f6; }
.tab-content { animation: fadeIn 0.3s ease; }

/* Sections */
.section { margin-bottom: 0; }
.section-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 15px; color: #2c3e50; }
.separator-line { height: 2px; background: #e2e8f0; margin: 25px 0; }

/* Info Grid */
.info-grid { display: grid; gap: 2rem; }
.dimensions-list { display: grid; gap: 10px; margin: 0; padding: 0; list-style: none; }
.dimension-item { display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; }
.dimension-item:last-child { border-bottom: none; }
.dimension-label { color: #64748b; font-weight: 500; }
.dimension-value { color: #1e293b; font-weight: 700; }
.features-list { display: grid; gap: 12px; margin: 0; padding: 0; }
.feature-item { display: flex; align-items: center; gap: 10px; padding: 0; }
.feature-badge { padding: 4px 12px; background: #f1f5f9; border-radius: 5px; font-size: 0.75rem; font-weight: 600; color: #475569; white-space: nowrap; }
.feature-value { color: #1e293b; font-size: 0.9rem; font-weight: 500; line-height: 1.4; }

/* ===== OPERADORES CON LOGO ===== */
.operators-list { list-style: none; padding: 0; margin: 0; display: grid; gap: 12px; }
.operator-item { display: flex; align-items: center; justify-content: space-between; padding: 14px; background: #f8fafc; border-radius: 8px; transition: all 0.2s; }
.operator-item:hover { background: #f1f5f9; transform: translateX(5px); }
.operator-info { display: flex; align-items: center; gap: 12px; }

/* Logo de fuerza armada */
.operator-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
  border-radius: 4px;
  background: white;
  padding: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Icono emoji fallback */
.operator-icon {
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  filter: grayscale(100%);
  opacity: 0.8;
}

.operator-name { font-weight: 600; margin: 0; font-size: 0.95rem; }
.operator-detail { font-size: 0.8rem; color: #64748b; margin: 2px 0 0 0; }

/* Conflicts */
.conflicts-list { list-style: none; padding: 0; margin: 0; display: grid; gap: 12px; }
.conflict-item { padding: 18px; border: 2px solid #e2e8f0; border-radius: 8px; transition: all 0.2s; }
.conflict-item:hover { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); border-color: #cbd5e1; }
.conflict-name { font-weight: 700; font-size: 1.05rem; margin: 0 0 8px 0; color: #1e293b; }
.conflict-date { font-size: 0.8rem; color: #64748b; display: block; margin-bottom: 8px; font-weight: 500; }
.conflict-description { color: #334155; font-size: 0.85rem; line-height: 1.6; margin: 0; }

/* Armament */
.armament-grid { display: grid; gap: 16px; }
.armament-category { border: 2px solid #e2e8f0; border-radius: 8px; padding: 18px; background: #f8fafc; transition: all 0.2s; }
.armament-category:hover { border-color: #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.category-title { font-weight: 700; font-size: 1rem; margin: 0 0 12px 0; color: #2c3e50; }
.systems-list { display: flex; flex-wrap: wrap; gap: 8px; }
.system-badge { padding: 5px 12px; background: white; border: 1px solid #e2e8f0; border-radius: 5px; font-size: 0.8rem; font-weight: 500; color: #334155; }

/* Scrollbar personalizada */
.dialog-right-content::-webkit-scrollbar {
  width: 8px;
}

.dialog-right-content::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.dialog-right-content::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.dialog-right-content::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Animations */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideIn { from { transform: translateY(-30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

/* Responsive */
@media (max-width: 1200px) {
  .dialog-content-split {
    max-width: 1200px;
  }
}

@media (max-width: 968px) {
  .dialog-split-container {
    flex-direction: column;
  }
  
  .dialog-left-image,
  .dialog-right-content {
    width: 100%;
    height: 50%;
  }
  
  .dialog-content-split {
    height: 95vh;
  }
  
  .aircraft-full-image {
    max-height: 70%;
  }
  
  .header-content h1 {
    font-size: 1.75rem;
  }
}
</style>
