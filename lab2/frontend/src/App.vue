<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <h1>Справочник товаров</h1>
        <nav class="nav">
          <router-link to="/">Товары</router-link>
          <router-link to="/categories">Категории</router-link>
        </nav>
      </div>
    </header>
    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
