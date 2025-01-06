import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  Box,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  FormControlLabel,
  Button,
  Alert,
} from '@mui/material';

interface MemorySettings {
  type: 'local' | 'indexed-db' | 'postgres';
  contextWindow: number;
  compression: boolean;
  persistence: boolean;
  shortTerm: {
    size: number;
    cleanup: 'aggressive' | 'balanced' | 'conservative';
  };
  longTerm: {
    storageLimit: number;
    backupEnabled: boolean;
  };
}

export const MemoryConfig: React.FC = () => {
  const [settings, setSettings] = useState<MemorySettings>({
    type: 'indexed-db',
    contextWindow: 8192,
    compression: true,
    persistence: true,
    shortTerm: {
      size: 1000,
      cleanup: 'balanced',
    },
    longTerm: {
      storageLimit: 10000,
      backupEnabled: true,
    }
  });

  // Load settings from file
  useEffect(() => {
    const loadSettings = async () => {
      try {
        const response = await fetch('/api/read-file?path=config/memory_settings.json');
        if (response.ok) {
          const savedSettings = await response.json();
          setSettings(savedSettings);
        }
      } catch (error) {
        console.error('Failed to load memory settings:', error);
      }
    };
    loadSettings();
  }, []);

  // Save settings to file
  const saveSettings = async () => {
    try {
      await fetch('/api/write-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          path: 'config/memory_settings.json',
          content: JSON.stringify(settings, null, 2)
        })
      });
    } catch (error) {
      console.error('Failed to save memory settings:', error);
    }
  };

  const handleChange = (path: string, value: any) => {
    const pathArray = path.split('.');
    setSettings(prev => {
      const newSettings = { ...prev };
      let current = newSettings;
      for (let i = 0; i < pathArray.length - 1; i++) {
        current = current[pathArray[i]];
      }
      current[pathArray[pathArray.length - 1]] = value;
      return newSettings;
    });
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Memory Configuration
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Basic Settings
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <FormControl fullWidth>
            <InputLabel>Storage Type</InputLabel>
            <Select
              value={settings.type}
              label="Storage Type"
              onChange={(e) => handleChange('type', e.target.value)}
            >
              <MenuItem value="local">Local Storage</MenuItem>
              <MenuItem value="indexed-db">IndexedDB</MenuItem>
              <MenuItem value="postgres">PostgreSQL</MenuItem>
            </Select>
          </FormControl>

          <TextField
            label="Context Window Size"
            type="number"
            value={settings.contextWindow}
            onChange={(e) => handleChange('contextWindow', Number(e.target.value))}
            helperText="Size in tokens (1024-32768)"
          />

          <FormControlLabel
            control={
              <Switch
                checked={settings.compression}
                onChange={(e) => handleChange('compression', e.target.checked)}
              />
            }
            label="Enable Compression"
          />

          <FormControlLabel
            control={
              <Switch
                checked={settings.persistence}
                onChange={(e) => handleChange('persistence', e.target.checked)}
              />
            }
            label="Enable Persistence"
          />
        </Box>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Short-term Memory
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Memory Size"
            type="number"
            value={settings.shortTerm.size}
            onChange={(e) => handleChange('shortTerm.size', Number(e.target.value))}
            helperText="Size in MB"
          />

          <FormControl fullWidth>
            <InputLabel>Cleanup Strategy</InputLabel>
            <Select
              value={settings.shortTerm.cleanup}
              label="Cleanup Strategy"
              onChange={(e) => handleChange('shortTerm.cleanup', e.target.value)}
            >
              <MenuItem value="aggressive">Aggressive</MenuItem>
              <MenuItem value="balanced">Balanced</MenuItem>
              <MenuItem value="conservative">Conservative</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Long-term Memory
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Storage Limit"
            type="number"
            value={settings.longTerm.storageLimit}
            onChange={(e) => handleChange('longTerm.storageLimit', Number(e.target.value))}
            helperText="Size in MB"
          />

          <FormControlLabel
            control={
              <Switch
                checked={settings.longTerm.backupEnabled}
                onChange={(e) => handleChange('longTerm.backupEnabled', e.target.checked)}
              />
            }
            label="Enable Backups"
          />
        </Box>
      </Paper>

      <Button
        variant="contained"
        onClick={saveSettings}
        sx={{ mt: 2 }}
      >
        Save Memory Settings
      </Button>
    </Box>
  );
};