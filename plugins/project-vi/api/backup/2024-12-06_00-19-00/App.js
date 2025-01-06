import React from 'react';
import './styles/tailwind.css';
import ConfigWizard from './components/ConfigWizard';
import { 
  ThemeProvider, 
  ConfigProvider, 
  ValidationProvider, 
  LoggingProvider 
} from './shared/contexts';

function App() {
  return (
    <ThemeProvider>
      <ConfigProvider>
        <ValidationProvider>
          <LoggingProvider>
            <div className="App">
              <ConfigWizard />
            </div>
          </LoggingProvider>
        </ValidationProvider>
      </ConfigProvider>
    </ThemeProvider>
  );
}

export default App;