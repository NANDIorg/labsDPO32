import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

export const productsApi = {
  getAll(params = {}) {
    return api.get('/products/', { params })
  },
  getOne(id) {
    return api.get(`/products/${id}`)
  },
  create(data) {
    return api.post('/products/', data)
  },
  update(id, data) {
    return api.put(`/products/${id}`, data)
  },
  delete(id) {
    return api.delete(`/products/${id}`)
  }
}

export const categoriesApi = {
  getAll() {
    return api.get('/categories/')
  },
  getOne(id) {
    return api.get(`/categories/${id}`)
  },
  create(data) {
    return api.post('/categories/', data)
  },
  update(id, data) {
    return api.put(`/categories/${id}`, data)
  },
  delete(id) {
    return api.delete(`/categories/${id}`)
  }
}

export default api
