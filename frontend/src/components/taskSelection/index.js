import React, {useState} from 'react';
import { useSelector } from 'react-redux';
import { Link } from '@reach/router';
import { FormattedMessage } from 'react-intl';
import ReactPlaceholder from 'react-placeholder';

import messages from './messages';
import { useFetch } from '../../hooks/UseFetch';
import { PriorityBox } from '../projectcard/projectCard';
import { TasksMap } from './map.js';
import { TaskSelectionFooter } from './footer';
import { TaskList } from './taskList';
import { htmlFromMarkdown } from '../projectDetail/htmlFromMarkdown';


export function HeaderLine({author, projectId, priority}: Object) {
    const userLink = (
      <Link to={`/users/${author}`} className="link blue-dark underline">
        {author}
      </Link>
    );
    return (
      <div className="cf">
        <div className="w-70 dib fl">
          <span className="blue-light">#{projectId}</span>
          <span className="blue-dark">
            {' '}
            | <FormattedMessage {...messages.createBy} values={{ user: userLink }} />
          </span>
        </div>
        <div className="mw4 dib fr">
          <PriorityBox priority={priority} extraClasses={'pv2 ph3'} />
        </div>
      </div>
    );
  }

export function TaskSelection({project, type, loading}: Object) {
  const [activeSection, setActiveSection] = useState('tasks');
  const defaultEditor = useSelector(state => state.preferences.default_editor);
  const [error, tasksLoading, tasks] = useFetch(`projects/${project.projectId}/tasks/`);
  const htmlInstructions =
  project.projectInfo && htmlFromMarkdown(project.projectInfo.instructions);

  return (
    <div>
      <div className="cf pv3">
        <div className="w-100 w-60-ns fl">
          <div className="ph4">
            <ReactPlaceholder
              showLoadingAnimation={true}
              rows={3}
              delay={500}
              ready={typeof(project.projectId) === 'number' && project.projectId > 0}
            >
              <HeaderLine author={project.author} priority={project.projectPriority} projectId={project.projectId} />
              <div className="cf pb3">
                <h3 className="f2 fw6 mt2 mb3 ttu barlow-condensed blue-dark">
                  {project.projectInfo && project.projectInfo.name}
                </h3>
                <span className="blue-light">{project.campaignTag} &#183; Brazil</span>
              </div>
              <div className="cf">
                <div className="cf ttu barlow-condensed f4 pv2">
                  <span
                    className={`mr4 pb2 pointer ${activeSection === 'tasks' && 'bb b--blue-dark'}`}
                    onClick={() => setActiveSection('tasks')}
                  >
                    <FormattedMessage {...messages.tasks} />
                  </span>
                  <span
                    className={`mr4 pb2 pointer ${activeSection === 'instructions' && 'bb b--blue-dark'}`}
                    onClick={() => setActiveSection('instructions')}
                  >
                    <FormattedMessage {...messages.instructions} />
                  </span>
                </div>
                <div className="pt4">
                  {activeSection === 'tasks' ? (
                    <TaskList projectId={project.projectId} tasks={tasks} />
                  ) : (
                    <p dangerouslySetInnerHTML={htmlInstructions} />
                  )}
                </div>
              </div>
            </ReactPlaceholder>
          </div>
        </div>
        <div className="w-100 w-40-ns fl">
          <TasksMap
            mapResults={tasks}
            projectId={project.projectId}
            type={type}
            error={error}
            loading={tasksLoading}
            className="dib w-100 fl"
          />
        </div>
      </div>
      <div className="cf ph4 bt b--grey-light">
        <ReactPlaceholder
          showLoadingAnimation={true}
          rows={3}
          delay={500}
          ready={typeof(project.projectId) === 'number' && project.projectId >0}
        >
          <TaskSelectionFooter
            type={type}
            mappingTypes={project.mappingTypes}
            imagery={project.imagery}
            editors={project.mappingEditors}
            defaultUserEditor={defaultEditor}
          />
        </ReactPlaceholder>
      </div>
    </div>
  );
}
