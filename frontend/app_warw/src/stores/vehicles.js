import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '@/services/apiClient';

export const useVehicleStore = defineStore('vehicles', () => {
  const planes = ref([]);
  const helicopters = ref([]);
  const currentVehicle = ref(null);
  const loading = ref(false);
  const error = ref(null);

  async function fetchPlanes() {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/aviones/');
      planes.value = response.data;
    } catch (e) {
      error.value = 'No se pudieron cargar los aviones.';
      console.error(e);
    } finally {
      loading.value = false;
    }
  }

  async function fetchHelicopters() {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/helicopteros/');
      helicopters.value = response.data;
    } catch (e) {
      error.value = 'No se pudieron cargar los helicópteros.';
      console.error(e);
    } finally {
      loading.value = false;
    }
  }

  async function fetchVehicleById(id) {
    loading.value = true;
    error.value = null;
    currentVehicle.value = null;
    try {
      const response = await apiClient.get(`/vehiculos/${id}/`); 
      currentVehicle.value = response.data;
    } catch (e) {
      error.value = 'No se pudo encontrar el vehículo solicitado.';
      console.error(e);
    } finally {
      loading.value = false;
    }
  }

  return { planes, helicopters, currentVehicle, loading, error, fetchPlanes, fetchHelicopters, fetchVehicleById };
});
