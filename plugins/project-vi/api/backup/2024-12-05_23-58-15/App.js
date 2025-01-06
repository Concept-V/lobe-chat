import React from 'react';
import './styles/tailwind.css';
import ConfigWizard from './components/ConfigWizard';
import { ThemeProvider } from './theme/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      <div className="App">
        <ConfigWizard />
      </div>
    </ThemeProvider>
  );
}

export default App;