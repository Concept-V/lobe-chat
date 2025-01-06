import React, { useState } from 'react';
import {
  Paper,
  Typography,
  Stepper,
  Step,
  StepLabel,
  Button,
  Box,
  TextField,
  FormControlLabel,
  Switch,
  Alert,
  CircularProgress,
} from '@mui/material';
import { ModuleProps } from '../../types/module';
import { InstallationService } from '../../services/installationService';
import { validateConfig, validateSystemRequirements } from '../../utils/configValidation';
import { useBackendInstallStore } from '../../stores/backendInstallStore';

// ... (previous interfaces remain the same)

export const BackendInstallModule: React.FC<ModuleProps> = ({ config: initialConfig }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [config, setConfig] = useState<BackendConfig>(initialConfig as BackendConfig || defaultConfig);
  const [status, setStatus] = useState<'idle' | 'checking' | 'installing' | 'error' | 'success'>('idle');
  const [error, setError] = useState<string | null>(null);
  const [installationProgress, setInstallationProgress] = useState<string>('');
  
  const installationService = new InstallationService();

  const handleSystemCheck = async () => {
    setStatus('checking');
    try {
      const result = await validateSystemRequirements();
      if (!result.valid) {
        throw new Error(result.errors.join(', '));
      }
      setActiveStep(1);
      setStatus('idle');
    } catch (err) {
      setError('System check failed: ' + (err as Error).message);
      setStatus('error');
    }
  };

  const handleConfigUpdate = (system: keyof BackendConfig, key: string, value: any) => {
    setConfig(prev => ({
      ...prev,
      [system]: {
        ...prev[system],
        [key]: value,
      },
    }));
  };

  const handleInstall = async () => {
    setStatus('installing');
    try {
      // Validate configuration
      const validation = validateConfig(config);
      if (!validation.valid) {
        throw new Error(validation.errors.join(', '));
      }

      // Update progress
      setInstallationProgress('Generating configuration files...');
      
      // Perform installation
      await installationService.install(config);
      
      setInstallationProgress('Verifying installation...');
      
      // Verify installation
      const isValid = await installationService.verifyInstallation();
      if (!isValid) {
        throw new Error('Installation verification failed');
      }

      setActiveStep(3);
      setStatus('success');
    } catch (err) {
      setError('Installation failed: ' + (err as Error).message);
      setStatus('error');
    }
  };

  const renderSystemCheck = () => (
    <Box sx={{ mt: 2 }}>
      <Button
        variant="contained"
        onClick={handleSystemCheck}
        disabled={status === 'checking'}
      >
        {status === 'checking' ? 'Checking...' : 'Start System Check'}
      </Button>
    </Box>
  );

  const renderConfiguration = () => (
    <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
      {Object.entries(config).map(([system, settings]) => (
        <Paper key={system} sx={{ p: 2 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            {system.charAt(0).toUpperCase() + system.slice(1)} System
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.enabled}
                  onChange={(e) => handleConfigUpdate(system as keyof BackendConfig, 'enabled', e.target.checked)}
                />
              }
              label="Enabled"
            />
            {Object.entries(settings).map(([key, value]) => {
              if (key === 'enabled') return null;
              if (typeof value === 'number') {
                return (
                  <TextField
                    key={key}
                    label={key.replace(/([A-Z])/g, ' $1').trim()}
                    type="number"
                    value={value}
                    onChange={(e) => handleConfigUpdate(system as keyof BackendConfig, key, Number(e.target.value))}
                    size="small"
                  />
                );
              }
              if (typeof value === 'string') {
                return (
                  <TextField
                    key={key}
                    label={key.replace(/([A-Z])/g, ' $1').trim()}
                    value={value}
                    onChange={(e) => handleConfigUpdate(system as keyof BackendConfig, key, e.target.value)}
                    size="small"
                  />
                );
              }
              return null;
            })}
          </Box>
        </Paper>
      ))}
      <Button
        variant="contained"
        onClick={() => setActiveStep(2)}
        sx={{ mt: 2 }}
      >
        Save Configuration
      </Button>
    </Box>
  );

  const renderInstallation = () => (
    <Box sx={{ mt: 2 }}>
      {status === 'installing' ? (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
          <CircularProgress />
          <Typography>{installationProgress}</Typography>
        </Box>
      ) : (
        <Button
          variant="contained"
          onClick={handleInstall}
          disabled={status === 'installing'}
        >
          Start Installation
        </Button>
      )}
    </Box>
  );

  const renderVerification = () => (
    <Box sx={{ mt: 2 }}>
      <Alert severity="success">
        Backend systems have been successfully installed and configured!
      </Alert>
      <Typography sx={{ mt: 2 }}>
        Your docker-compose configuration has been generated and the system is ready to use.
        To start the services, run:
      </Typography>
      <Paper sx={{ p: 2, mt: 1, bgcolor: 'grey.900' }}>
        <Typography sx={{ fontFamily: 'monospace' }}>
          docker-compose up -d
        </Typography>
      </Paper>
      <Typography sx={{ mt: 2 }}>
        You can monitor the system status at:
        <ul>
          <li>Frontend: http://localhost:3000</li>
          <li>API: http://localhost:5000</li>
          <li>Monitoring: http://localhost:3001</li>
        </ul>
      </Typography>
    </Box>
  );

  return (
    <Paper sx={{ p: 3, minWidth: 600 }}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Backend Systems Installation
      </Typography>

      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {activeStep === 0 && renderSystemCheck()}
      {activeStep === 1 && renderConfiguration()}
      {activeStep === 2 && renderInstallation()}
      {activeStep === 3 && renderVerification()}
    </Paper>
  );
};

export const moduleConfig = {
  id: 'backend-install',
  name: 'Backend Installation',
  description: 'Install and configure backend systems',
  component: BackendInstallModule,
};