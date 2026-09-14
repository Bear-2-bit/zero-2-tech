import http from './http'


export function getTaskSteps(taskId) {
  return http.get(
    `/tasks/${taskId}/steps`
  )
}


export function saveTaskSteps(
  taskId,
  steps
) {
  return http.post(
    `/tasks/${taskId}/steps`,
    {
      steps,
    }
  )
}


export function updateTaskStep(
  taskId,
  stepId,
  data
) {
  return http.put(
    `/tasks/${taskId}/steps/${stepId}`,
    data
  )
}


export function deleteTaskStep(
  taskId,
  stepId
) {
  return http.delete(
    `/tasks/${taskId}/steps/${stepId}`
  )
}
