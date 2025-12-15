<template>
  <div class="categories-view">
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2>Категории</h2>
        <button class="btn btn-primary" @click="openModal()">Добавить категорию</button>
      </div>

      <div v-if="loading" class="empty-state">Загрузка...</div>
      <div v-else-if="categories.length === 0" class="empty-state">
        Категории не найдены
      </div>
      <table v-else>
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Описание</th>
            <th>Дата создания</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.id">
            <td>{{ category.id }}</td>
            <td>{{ category.name }}</td>
            <td>{{ category.description || '-' }}</td>
            <td>{{ formatDate(category.created_at) }}</td>
            <td class="actions">
              <button class="btn btn-secondary" @click="openModal(category)">Изменить</button>
              <button class="btn btn-danger" @click="deleteCategory(category.id)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingCategory ? 'Редактировать категорию' : 'Добавить категорию' }}</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <form @submit.prevent="saveCategory">
          <div class="form-group">
            <label>Название *</label>
            <input v-model="form.name" type="text" required />
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="form.description" rows="3"></textarea>
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
import { categoriesApi } from '../api'

export default {
  name: 'CategoriesView',
  data() {
    return {
      categories: [],
      loading: false,
      showModal: false,
      editingCategory: null,
      form: {
        name: '',
        description: ''
      }
    }
  },
  async mounted() {
    await this.fetchCategories()
  },
  methods: {
    async fetchCategories() {
      this.loading = true
      try {
        const response = await categoriesApi.getAll()
        this.categories = response.data
      } catch (error) {
        alert('Ошибка загрузки категорий')
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleDateString('ru-RU')
    },
    openModal(category = null) {
      this.editingCategory = category
      if (category) {
        this.form = {
          name: category.name,
          description: category.description || ''
        }
      } else {
        this.form = {
          name: '',
          description: ''
        }
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.editingCategory = null
    },
    async saveCategory() {
      try {
        if (this.editingCategory) {
          await categoriesApi.update(this.editingCategory.id, this.form)
        } else {
          await categoriesApi.create(this.form)
        }
        this.closeModal()
        await this.fetchCategories()
      } catch (error) {
        alert('Ошибка сохранения категории')
      }
    },
    async deleteCategory(id) {
      if (!confirm('Удалить эту категорию?')) return
      try {
        await categoriesApi.delete(id)
        await this.fetchCategories()
      } catch (error) {
        alert('Ошибка удаления категории')
      }
    }
  }
}
</script>
