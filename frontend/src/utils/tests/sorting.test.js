import { compareTaskId, compareHistoryId } from '../sorting';

it('test sorting with compareHistoryId', () => {
  let arr = [{historyId: 45}, {historyId: 34}, {historyId: 40}, {historyId: 200}, {historyId: 4}];
  expect(
    arr.sort(compareHistoryId)
  ).toEqual(
    [ { "historyId": 4 }, { "historyId": 34 }, { "historyId": 40 }, { "historyId": 45 }, { "historyId": 200 } ]
  );
});

it('test sorting with compareTaskId', () => {
  let arr = [{taskId: 45}, {taskId: 34}, {taskId: 40}, {taskId: 200}, {taskId: 4}];
  expect(
    arr.sort(compareTaskId)
  ).toEqual(
    [ { "taskId": 4 }, { "taskId": 34 }, { "taskId": 40 }, { "taskId": 45 }, { "taskId": 200 } ]
  );
});
