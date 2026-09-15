import http from './http'


export function getDashboard() {
  return http.get('/dashboard')
}
