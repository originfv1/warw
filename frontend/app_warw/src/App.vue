<script setup>
import { RouterView, RouterLink } from 'vue-router';
import logo from '@/assets/multimedia/logo.png';
</script>

<template>
  <div id="app-layout">
    <header class="main-header">
      <div class="container header-container">
        
        <div class="header-left">
          <RouterLink to="/" class="site-brand">
            <img :src="logo" alt="Logo de WARW" />
          </RouterLink>

          <nav class="menu" role="navigation">

            <RouterLink to="/">
              <a>Inicio</a>
            </RouterLink>

            <RouterLink to="/armas">
              <a>Armas</a>
            </RouterLink>
            
            <RouterLink to="/aviones">
              <a>Aviones</a>
            </RouterLink>

            <RouterLink to="/helicopteros">
              <a>Helicópteros</a>
            </RouterLink>
          </nav>
        </div>

        <form class="search-form">
          <input type="search" placeholder="Buscar en la enciclopedia...">
          <button type="submit">
          </button>
        </form>
      </div>
    </header>

    <main>
      <RouterView />
    </main>

    <footer class="main-footer">
      <div class="container">
        <p>&copy; 2025 WARW Project. Todos los derechos reservados.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>

#app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
main {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
.main-header { border-bottom: 1px solid var(--color-border); background-color: var(--color-surface); position: sticky; top: 0; z-index: 1000; }
.header-container { display: flex; align-items: center; justify-content: space-between; height: 70px; padding-top: 0; padding-bottom: 0; }
.header-left {
  display: flex;
  align-items: center;
  gap: 3rem;
}
.site-brand { display: block; }
.site-brand img { height: 70px; width: auto; display: block; }
.search-form { position: relative; }
.search-form input { background-color: var(--color-background); border: 1px solid var(--color-border); border-radius: 20px; padding: 0.5rem 1rem 0.5rem 2.5rem; color: var(--color-text); width: 250px; transition: all 0.2s ease; }
.search-form input:focus { border-color: var(--color-accent); outline: none; }
.search-form button { position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--color-text-muted); cursor: pointer; }
.main-footer { border-top: 1px solid var(--color-border); padding: 1.5rem 0; text-align: center; font-size: 0.9rem; color: var(--color-text-muted); }

.menu {
  display: flex;
  gap: 10px;
  align-items: center;
}

.menu a {
  text-decoration: none;
  color: inherit;
}

</style>