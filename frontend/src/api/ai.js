import http from './http'


export function decomposeGoal(goal) {
  return http.post('/ai/decompose', {
    goal,
  })
}
