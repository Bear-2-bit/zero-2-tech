import http from './http'


export function getTasks() {
  return http.get('/tasks')
}


export function getTask(id) {
  return http.get(`/tasks/${id}`)
}


export function createTask(data) {
  return http.post('/tasks', data)
}


export function updateTask(id, data) {
  return http.put(`/tasks/${id}`, data)
}


export function deleteTask(id) {
  return http.delete(`/tasks/${id}`)
}
