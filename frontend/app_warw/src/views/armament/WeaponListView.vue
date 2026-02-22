<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useArmamentStore } from '@/stores/armament';

const armamentStore = useArmamentStore();
const isDialogOpen = ref(false);
const activeTab = ref('specs');
const currentWeapon = ref(null);

onMounted(() => {
  armamentStore.fetchWeapons();

  const handleEsc = (e) => {
    if (e.key === "Escape" && isDialogOpen.value) closeWeaponDialog();
  };

  window.addEventListener("keydown", handleEsc);
  onUnmounted(() => window.removeEventListener("keydown", handleEsc));
});

const openWeaponDialog = async (weapon) => {
  currentWeapon.value = weapon;
  activeTab.value = 'specs';
  isDialogOpen.value = true;
  // Si necesitas cargar más detalles:
  // await armamentStore.fetchWeaponById(weapon.id);
};

const closeWeaponDialog = () => {
  isDialogOpen.value = false;
  currentWeapon.value = null;
};

const getWeaponImage = (weapon) => {
  if (!weapon.multimedia || weapon.multimedia.length === 0) return null;
  const image = weapon.multimedia.find(m => m.tipo === 'Imagen de Galería');
  return image ? image.archivo : null;
};

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

const getIconoPorRama = (rama) => {
  const iconos = {
    'EJE': '🪖',
    'ARM': '⚓',
    'FAE': '✈️',
    'MAR': '🎖️',
    'OTR': '🛡️'
  };
  return iconos[rama] || '🌍';
};
</script>

<template>
  <div class="container">
    <header class="page-header">
      <h1>Galería de Armamento</h1>
      <p>Explora todos los modelos de armas disponibles.</p>
    </header>

    <div v-if="armamentStore.loading" class="loading-state">Cargando arsenal...</div>
    <div v-if="armamentStore.error" class="error-state">{{ armamentStore.error }}</div>
    
    <div v-if="!armamentStore.loading && armamentStore.weapons.length" class="weapon-grid">
      <div 
        v-for="weapon in armamentStore.weapons" 
        :key="weapon.id" 
        @click="openWeaponDialog(weapon)"
        class="weapon-card"
      >
        <div class="weapon-card-image-wrapper">
          <img v-if="getWeaponImage(weapon)" :src="getWeaponImage(weapon)" :alt="weapon.nombre" class="weapon-card-image" loading="lazy">
          <div v-else class="weapon-card-image-placeholder">Sin Imagen</div>
        </div>
        <div class="weapon-card-content">
          <h3>{{ weapon.nombre }}</h3>
          <p>{{ weapon.tipo }}</p>
        </div>
      </div>
    </div>

    <!-- MODAL CON IMAGEN (IGUAL AL DE AVIONES) -->
    <div v-if="isDialogOpen" class="dialog-overlay" @click="closeWeaponDialog">
      <div class="dialog-content-split" @click.stop>
        <button class="close-btn" @click="closeWeaponDialog">✕</button>

        <div v-if="!currentWeapon" class="dialog-loading">Cargando detalles...</div>

        <div v-else class="dialog-split-container">
          
          <!-- IMAGEN IZQUIERDA -->
          <div class="dialog-left-image">
            <img 
              v-if="getWeaponImage(currentWeapon)" 
              :src="getWeaponImage(currentWeapon)" 
              :alt="currentWeapon.nombre"
              class="weapon-full-image"
            >
            <div v-else class="no-image-placeholder">
              <span class="weapon-icon-large">🔫</span>
              <p>Sin imagen disponible</p>
            </div>
          </div>

          <!-- CONTENIDO DERECHO -->
          <div class="dialog-right-content">
            <article class="weapon-detail">
              
              <header class="detail-header">
                <div class="header-content">
                  <div class="header-top">
                    <span class="badge">{{ currentWeapon.tipo }}</span>
                    <img 
                      v-if="currentWeapon.pais_origen?.bandera" 
                      :src="currentWeapon.pais_origen.bandera" 
                      :alt="currentWeapon.pais_origen.nombre" 
                      class="flag-icon"
                    >
                  </div>
                  <h1>{{ currentWeapon.nombre }}</h1>
                  <div class="subtitle">
                    <span>🌍 {{ currentWeapon.pais_origen?.nombre || 'Origen desconocido' }}</span>
                  </div>
                </div>
              </header>

              <!-- TABS -->
              <div class="tabs">
                <div class="tabs-list">
                  <button @click="activeTab = 'specs'" :class="['tab-button', { active: activeTab === 'specs' }]">
                    ⚙️ Especificaciones
                  </button>
                  <button v-if="currentWeapon.operadores?.length" @click="activeTab = 'operators'" :class="['tab-button', { active: activeTab === 'operators' }]">
                    🌍 Operadores
                  </button>
                  <button v-if="currentWeapon.conflictos_uso?.length" @click="activeTab = 'combat'" :class="['tab-button', { active: activeTab === 'combat' }]">
                    ⚔️ Conflictos
                  </button>
                </div>

                <!-- ESPECIFICACIONES -->
                <div v-if="activeTab === 'specs'" class="tab-content">
                  <section class="section">
                    <h3 class="section-title">📋 Descripción Técnica</h3>
                    <div class="specs-content">
                      <div class="spec-block" v-if="currentWeapon.funcionamiento">
                        <span class="spec-label">Funcionamiento</span>
                        <p class="spec-text">{{ currentWeapon.funcionamiento }}</p>
                      </div>
                      <div class="spec-block" v-if="currentWeapon.mecanismos">
                        <span class="spec-label">Mecanismos</span>
                        <p class="spec-text">{{ currentWeapon.mecanismos }}</p>
                      </div>
                    </div>
                  </section>
                </div>

                <!-- OPERADORES -->
                <div v-if="activeTab === 'operators'" class="tab-content">
                  <section class="section">
                    <h3 class="section-title">🌍 Operadores</h3>
                    <ul class="operators-list">
                      <li v-for="op in currentWeapon.operadores" :key="op.id" class="operator-item">
                        <div class="operator-info">
                          <img v-if="op.logo" :src="op.logo" :alt="op.nombre" class="operator-logo">
                          <span v-else class="operator-icon">{{ getIconoPorRama(op.rama) }}</span>
                          
                          <div>
                            <p class="operator-name">{{ op.nombre }}</p>
                            <p class="operator-detail" v-if="op.pais">{{ op.pais }}</p>
                            <p class="operator-detail" v-if="op.rama">Rama: {{ getRamaName(op.rama) }}</p>
                          </div>
                        </div>
                      </li>
                    </ul>
                  </section>
                </div>

                <!-- CONFLICTOS -->
                <div v-if="activeTab === 'combat'" class="tab-content">
                  <section class="section">
                    <h3 class="section-title">⚔️ Conflictos</h3>
                    <ul class="conflicts-list">
                      <li v-for="c in currentWeapon.conflictos_uso" :key="c.id" class="conflict-item">
                        <h4 class="conflict-name">{{ c.nombre }}</h4>
                        <span class="conflict-date">
                          {{ new Date(c.fecha_inicio).toLocaleDateString('es-ES') }} - 
                          {{ c.fecha_fin ? new Date(c.fecha_fin).toLocaleDateString('es-ES') : 'Actualidad' }}
                        </span>
                        <p class="conflict-description" v-if="c.descripcion">{{ c.descripcion }}</p>
                      </li>
                    </ul>
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

/* ===== WEAPON GRID ===== */
.weapon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
.weapon-card {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  display: block;
  color: var(--color-text);
  background-color: var(--color-surface);
  cursor: pointer;
  transition: 
    transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), 
    box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1),
    border-color 0.3s ease;
}
.weapon-card:hover {
  transform: scale(1.02);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 1);
  border-color: var(--color-accent);
}
.weapon-card-image-wrapper {
  width: 100%;
  height: 200px;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}
.weapon-card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.weapon-card-image-placeholder {
  color: var(--color-text-muted);
}
.weapon-card-content {
  padding: 1rem;
}
.weapon-card-content h3 {
  margin-bottom: 0.25rem;
  color: var(--color-text);
  transition: color 0.3s ease;
}
.weapon-card:hover .weapon-card-content h3 {
  color: var(--color-accent);
}
.weapon-card-content p {
  color: var(--color-text-muted);
}
.loading-state, .error-state {
  text-align: center;
  padding: 3rem;
  font-size: 1.25rem;
  color: var(--color-text-muted);
}

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

/* IMAGEN DEL ARMA */
.weapon-full-image {
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

.weapon-icon-large {
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

/* DETALLE */
.weapon-detail { font-family: 'Segoe UI', system-ui, sans-serif; }
.detail-header { margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 2px solid #e2e8f0; }
.header-top { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.flag-icon { width: 28px; height: 18px; border-radius: 3px; }
.badge { padding: 5px 14px; background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 0.8rem; font-weight: 600; }
.detail-header h1 { font-size: 2.2rem; margin: 0 0 0.5rem 0; color: #2c3e50; font-weight: 700; }
.subtitle { color: #7f8c8d; font-size: 1.05rem; }

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

/* Specs */
.specs-content { display: grid; gap: 1rem; }
.spec-block {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}
.spec-label {
  display: block;
  font-weight: 600;
  color: #475569;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}
.spec-text {
  color: #1e293b;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
}

/* Operators */
.operators-list { list-style: none; padding: 0; margin: 0; display: grid; gap: 12px; }
.operator-item { display: flex; align-items: center; padding: 14px; background: #f8fafc; border-radius: 8px; transition: all 0.2s; }
.operator-item:hover { background: #f1f5f9; transform: translateX(5px); }
.operator-info { display: flex; align-items: center; gap: 12px; }

.operator-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
  border-radius: 4px;
  background: white;
  padding: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

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

/* Scrollbar */
.dialog-right-content::-webkit-scrollbar { width: 8px; }
.dialog-right-content::-webkit-scrollbar-track { background: #f1f5f9; }
.dialog-right-content::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
.dialog-right-content::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* Animations */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideIn { from { transform: translateY(-30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

/* Responsive */
@media (max-width: 1200px) {
  .dialog-content-split { max-width: 1200px; }
}

@media (max-width: 968px) {
  .dialog-split-container { flex-direction: column; }
  .dialog-left-image, .dialog-right-content { width: 100%; height: 50%; }
  .dialog-content-split { height: 95vh; }
  .weapon-full-image { max-height: 70%; }
  .detail-header h1 { font-size: 1.75rem; }
}
</style>