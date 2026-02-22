// frontend/app_warw/src/stores/armament.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '@/services/apiClient';

export const useArmamentStore = defineStore('armament', () => {
  // --- State ---
  const weapons = ref([]);
  const currentWeapon = ref(null);
  const loading = ref(false);
  const error = ref(null);

  // --- Actions ---
  async function fetchWeapons() {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/armas/');
      weapons.value = response.data;
    } catch (e) {
      error.value = 'No se pudieron cargar las armas.';
      console.error(e);
    } finally {
      loading.value = false;
    }
  }

  async function fetchWeaponById(id) {
    loading.value = true;
    error.value = null;
    currentWeapon.value = null; // Resetea antes de buscar
    try {
      const response = await apiClient.get(`/armas/${id}/`);
      currentWeapon.value = response.data;
    } catch (e) {
      error.value = 'No se pudo encontrar el arma solicitada.';
      console.error(e);
    } finally {
      loading.value = false;
    }
  }

  return { weapons, currentWeapon, loading, error, fetchWeapons, fetchWeaponById };
});
