import { defineMessages } from 'react-intl';

/**
 * Internationalized messages for use on header.
 */
export default defineMessages({
  createBy: {
    id: 'project.createdBy',
    defaultMessage: 'Created by {user}',
  },
  typesOfMapping: {
    id: 'project.typesOfMapping',
    defaultMessage: 'Types of Mapping',
  },
  editor: {
    id: 'project.editor',
    defaultMessage: 'Editor',
  },
  selectEditor: {
    id: 'project.editor.select',
    defaultMessage: 'Select editor',
  },
  tasks: {
    id: 'project.tasks',
    defaultMessage: 'Tasks',
  },
  instructions: {
    id: 'project.instructions',
    defaultMessage: 'Instructions',
  },
  imagery: {
    id: 'project.imagery',
    defaultMessage: 'Imagery',
  },
  customTMSLayer: {
    id: 'project.imagery.tms',
    defaultMessage: 'Custom TMS Layer',
  },
  customWMSLayer: {
    id: 'project.imagery.wms',
    defaultMessage: 'Custom WMS Layer',
  },
  customWMTSLayer: {
    id: 'project.imagery.wmts',
    defaultMessage: 'Custom WMTS Layer',
  },
  mapRandomTask: {
    id: 'project.selectTask.footer.button.mapRandomTask',
    defaultMessage: 'Map random task',
  },
  validateRandomTask: {
    id: 'project.selectTask.footer.button.validateRandomTask',
    defaultMessage: 'Validate random task',
  },
  taskLastUpdate: {
    id: 'project.tasks.list.lastUpdate',
    defaultMessage: 'Last updated by {user}',
  },
  taskStatus_READY: {
    id: 'project.tasks.status.ready',
    defaultMessage: 'Ready to map',
  },
  taskStatus_MAPPED: {
    id: 'project.tasks.status.mapped',
    defaultMessage: 'Mapped',
  },
  taskStatus_LOCKED_FOR_MAPPING: {
    id: 'project.tasks.status.lockedForMapping',
    defaultMessage: 'Locked for mapping',
  },
  taskStatus_LOCKED_FOR_VALIDATION: {
    id: 'project.tasks.status.lockedForValidation',
    defaultMessage: 'Locked for validation',
  },
  taskStatus_VALIDATED: {
    id: 'project.tasks.status.validated',
    defaultMessage: 'Validated',
  },
  taskStatus_INVALIDATED: {
    id: 'project.tasks.status.invalidated',
    defaultMessage: 'Invalidated',
  },
  taskStatus_BADIMAGERY: {
    id: 'project.tasks.status.badImagery',
    defaultMessage: 'Bad imagery',
  },
  taskStatus_SPLIT: {
    id: 'project.tasks.status.split',
    defaultMessage: 'Splitted',
  },
});
