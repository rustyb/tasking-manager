
export function compareHistoryId(a, b){
  if (a.historyId > b.historyId) return 1;
  if (b.historyId > a.historyId) return -1;
  return 0;
}

export function compareTaskId(a, b){
  if (a.taskId > b.taskId) return 1;
  if (b.taskId > a.taskId) return -1;
  return 0;
}
