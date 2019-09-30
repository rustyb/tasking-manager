import React from 'react';
import { FormattedMessage } from 'react-intl';

import messages from './messages';

export function Imagery({ value = '' }: Object) {
  let content = <span>{value}</span>;
  if (value) {
    if (value.startsWith('tms[')) {
      content = <FormattedMessage {...messages.customTMSLayer} />;
    }
    if (value.startsWith('wms[')) {
      content = <FormattedMessage {...messages.customWMSLayer} />;
    }
    if (value.startsWith('wmts[')) {
      content = <FormattedMessage {...messages.customWMTSLayer} />;
    }
  } else {
    content = <FormattedMessage {...messages.noImageryDefined} />;
  }
  return <p className={`f5 fw6 pt1 ma0 ${value ? 'blue-dark' : 'blue-light'}`}>{content}</p>;
}
