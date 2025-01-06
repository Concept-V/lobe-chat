import React from 'react';
import ReactDOM from 'react-dom/client';
import { ConfigurationBuilder } from './components/core/ConfigurationBuilder';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ConfigurationBuilder />
  </React.StrictMode>
);