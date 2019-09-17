import React from 'react';

import { useFetch } from '../hooks/UseFetch';
import { TaskSelection } from '../components/taskSelection';


const Error = ({ error }) => <span>Error:{error.message}</span>;

export function SelectTaskToMap({ id }: Object) {
  const [error, loading, data] = useFetch(`projects/${id}/queries/summary/`);
  if (error) return <Error error={error} />;
  return (
    <div className="cf">
      <TaskSelection type={'mapping'} project={data} loading={loading} />
    </div>
  );
}

export function SelectTaskToValidate({ id }: Object) {
  const [error, loading, data] = useFetch(`projects/${id}/queries/summary/`);
  if (error) return <Error error={error} />;
  return (
    <div className="cf">
      <TaskSelection type={'validation'} project={data} loading={loading} />
    </div>
  );
}
