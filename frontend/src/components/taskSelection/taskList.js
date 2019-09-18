import React, { useLayoutEffect, useState } from 'react';
import { FormattedMessage, FormattedRelative } from 'react-intl';

import messages from './messages';
import { useFetch } from '../../hooks/UseFetch';
import { compareTaskId, compareHistoryId } from '../../utils/sorting';

function getLastTaskActivity(task, activities) {
  return activities.filter(
    activity => activity.taskId === task.properties.taskId
  ).filter(
    activity => activity.action === task.properties.taskStatus || activity.actionText === task.properties.taskStatus
  ).sort(compareHistoryId)[0];
}

export function TaskList({tasks, projectId}: Object) {
  const [error, loading, touchedTasks] = useFetch(`projects/${projectId}/activities/`);
  const activeStatus = ['MAPPED', 'VALIDATED', 'LOCKED_FOR_MAPPING', 'LOCKED_FOR_VALIDATION', 'INVALIDATED', 'BADIMAGERY'];
  console.log(tasks && tasks.features && tasks.features.filter(task => activeStatus.includes(task.properties.taskStatus)));
  return <div className="cf">
    {tasks && tasks.features && tasks.features
      .filter(task => activeStatus.includes(task.properties.taskStatus))
      .map(task => getLastTaskActivity(task, touchedTasks.activity))
      .filter(taskActivity => taskActivity !== undefined)
      .sort(compareTaskId)
      .map((taskActivity, n) =>
        <div key={n} className="db pv3 ba b--tan mt2 cf">
          <div className="w-60 fl dib">
            <span className="pl3 b">#{taskActivity.taskId}</span>
            <span className="ph2 blue-grey">&#183;</span>
            <span className="blue-grey">
            <FormattedMessage {...messages.taskLastUpdate} values={{user: <span className="b blue-grey">{taskActivity.actionBy}</span>}} />
            { ' ' }
            <FormattedRelative value={taskActivity.actionDate} />
            </span>
          </div>
          <div className="w-30 fl blue-grey dib">
            <span>
              <span className="ph2 blue-grey f3 fw5">&#183;</span>
                <FormattedMessage
                  {...messages[`taskStatus_${taskActivity.action === 'STATE_CHANGE' ? taskActivity.actionText : taskActivity.action}`]}
                />
            </span>
          </div>
          <div className="w-10 fl dib">

          </div>
        </div>
    )}

  </div>;
}
