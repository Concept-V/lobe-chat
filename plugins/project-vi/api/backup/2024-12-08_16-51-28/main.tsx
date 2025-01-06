import React from 'react';
import ReactDOM from 'react-dom/client';
import { ThemeProvider, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import { Layout } from './components/Layout';
import { MemoryConfig } from './components/sections/MemoryConfig';
import { ExportConfig } from './components/sections/ExportConfig';
import './index.css';

// Dark theme
const theme = createTheme({
  palette: {
    mode: 'dark',
  },
});

// Route configuration
const routes = {
  memory: MemoryConfig,
  export: ExportConfig,
};

const App = () => {
  const [currentRoute, setCurrentRoute] = React.useState('memory');
  const CurrentComponent = routes[currentRoute];

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Layout onRouteChange={setCurrentRoute}>
        <CurrentComponent />
      </Layout>
    </ThemeProvider>
  );
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);