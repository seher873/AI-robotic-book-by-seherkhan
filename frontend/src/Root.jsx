import React from 'react';
import AppWrapper from './client/AppWrapper';

// Root component that wraps the entire Docusaurus application
// This ensures that AuthProvider and other global providers are available throughout the app
function Root({ children }) {
  return <AppWrapper>{children}</AppWrapper>;
}

export default Root;