<template>
  <div class="products-view">
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2>Товары</h2>
        <button class="btn btn-primary" @click="openModal()">Добавить товар</button>
      </div>

      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск по названию..."
          @input="fetchProducts"
        />
        <select v-model="selectedCategory" @change="fetchProducts">
          <option :value="null">Все категории</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>

      <div v-if="loading" class="empty-state">Загрузка...</div>
      <div v-else-if="products.length === 0" class="empty-state">
        Товары не найдены
      </div>
      <table v-else>
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Описание</th>
            <th>Цена</th>
            <th>Количество</th>
            <th>Категория</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.description || '-' }}</td>
            <td>{{ product.price.toFixed(2) }} руб.</td>
            <td>{{ product.quantity }}</td>
            <td>
              <span class="badge" v-if="product.category">{{ product.category.name }}</span>
              <span v-else>-</span>
            </td>
            <td class="actions">
              <button class="btn btn-secondary" @click="openModal(product)">Изменить</button>
              <button class="btn btn-danger" @click="deleteProduct(product.id)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingProduct ? 'Редактировать товар' : 'Добавить товар' }}</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <form @submit.prevent="saveProduct">
          <div class="form-group">
            <label>Название *</label>
            <input v-model="form.name" type="text" required />
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="form.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>Цена *</label>
            <input v-model.number="form.price" type="number" step="0.01" min="0" required />
          </div>
          <div class="form-group">
            <label>Количество</label>
            <input v-model.number="form.quantity" type="number" min="0" />
          </div>
          <div class="form-group">
            <label>Категория</label>
            <select v-model="form.category_id">
              <option :value="null">Без категории</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>
          <div style="display: flex; gap: 10px; justify-content: flex-end;">
            <button type="button" class="btn btn-secondary" @click="closeModal">Отмена</button>
            <button type="submit" class="btn btn-success">Сохранить</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { productsApi, categoriesApi } from '../api'

export default {
  name: 'ProductsView',
  data() {
    return {
      products: [],
      categories: [],
      loading: false,
      showModal: false,
      editingProduct: null,
      searchQuery: '',
      selectedCategory: null,
      form: {
        name: '',
        description: '',
        price: 0,
        quantity: 0,
        category_id: null
      }
    }
  },
  async mounted() {
    await this.fetchCategories()
    await this.fetchProducts()
  },
  methods: {
    async fetchProducts() {
      this.loading = true
      try {
        const params = {}
        if (this.searchQuery) params.search = this.searchQuery
        if (this.selectedCategory) params.category_id = this.selectedCategory
        const response = await productsApi.getAll(params)
        this.products = response.data
      } catch (error) {
        alert('Ошибка загрузки товаров')
      } finally {
        this.loading = false
      }
    },
    async fetchCategories() {
      try {
        const response = await categoriesApi.getAll()
        this.categories = response.data
      } catch (error) {
        console.error('Ошибка загрузки категорий')
      }
    },
    openModal(product = null) {
      this.editingProduct = product
      if (product) {
        this.form = {
          name: product.name,
          description: product.description || '',
          price: product.price,
          quantity: product.quantity,
          category_id: product.category_id
        }
      } else {
        this.form = {
          name: '',
          description: '',
          price: 0,
          quantity: 0,
          category_id: null
        }
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.editingProduct = null
    },
    async saveProduct() {
      try {
        if (this.editingProduct) {
          await productsApi.update(this.editingProduct.id, this.form)
        } else {
          await productsApi.create(this.form)
        }
        this.closeModal()
        await this.fetchProducts()
      } catch (error) {
        alert('Ошибка сохранения товара')
      }
    },
    async deleteProduct(id) {
      if (!confirm('Удалить этот товар?')) return
      try {
        await productsApi.delete(id)
        await this.fetchProducts()
      } catch (error) {
        alert('Ошибка удаления товара')
      }
    }
  }
}
</script>
