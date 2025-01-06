import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Slider,
  Switch,
  FormControlLabel,
  CircularProgress,
  Alert,
} from '@mui/material';
import { ModuleProps } from '@/types/module';
import { useBackendInstallStore } from '@/stores/backendInstallStore';

interface MemoryStats {
  used: number;
  total: number;
  contextSize: number;
}

export const MemoryModule: React.FC<ModuleProps> = () => {
  const [stats, setStats] = useState<MemoryStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { systems } = useBackendInstallStore();
  const memoryConfig = systems.memory;

  const [settings, setSettings] = useState({
    storageType: 'indexed-db',
    contextWindow: 8192,
    persistenceEnabled: true,
    compressionEnabled: true,
  });

  useEffect(() => {
    fetchMemoryStats();
    const interval = setInterval(fetchMemoryStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchMemoryStats = async () => {
    try {
      setLoading(true);
      // This would be replaced with actual API call
      const response = await fetch('/api/memory/stats');
      const data = await response.json();
      setStats(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch memory statistics');
    } finally {
      setLoading(false);
    }
  };

  const handleSettingChange = (setting: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [setting]: value
    }));
  };

  const renderMemoryUsage = () => {
    if (!stats) return null;
    
    const usagePercent = (stats.used / stats.total) * 100;
    return (
      <Box sx={{ position: 'relative', display: 'inline-flex' }}>
        <CircularProgress
          variant="determinate"
          value={usagePercent}
          size={80}
          thickness={4}
          sx={{ color: usagePercent > 80 ? 'error.main' : 'primary.main' }}
        />
        <Box
          sx={{
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            position: 'absolute',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Typography variant="caption" component="div" color="text.secondary">
            {`${Math.round(usagePercent)}%`}
          </Typography>
        </Box>
      </Box>
    );
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Memory Management
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Memory Usage Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Memory Usage
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
                {loading ? <CircularProgress /> : renderMemoryUsage()}
              </Box>
              {stats && (
                <Typography variant="body2" color="text.secondary">
                  {`${Math.round(stats.used / 1024 / 1024)}MB / ${Math.round(stats.total / 1024 / 1024)}MB`}
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Context Window Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Context Window
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Slider
                  value={settings.contextWindow}
                  onChange={(_, value) => handleSettingChange('contextWindow', value)}
                  min={1024}
                  max={32768}
                  step={1024}
                  marks={[
                    { value: 1024, label: '1K' },
                    { value: 8192, label: '8K' },
                    { value: 32768, label: '32K' },
                  ]}
                  valueLabelDisplay="auto"
                  valueLabelFormat={value => `${value / 1024}K`}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Storage Settings Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Storage Settings
              </Typography>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Storage Type</InputLabel>
                <Select
                  value={settings.storageType}
                  label="Storage Type"
                  onChange={(e) => handleSettingChange('storageType', e.target.value)}
                >
                  <MenuItem value="local">Local Storage</MenuItem>
                  <MenuItem value="indexed-db">IndexedDB</MenuItem>
                  <MenuItem value="postgres">PostgreSQL</MenuItem>
                </Select>
              </FormControl>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.persistenceEnabled}
                    onChange={(e) => handleSettingChange('persistenceEnabled', e.target.checked)}
                  />
                }
                label="Enable Persistence"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.compressionEnabled}
                    onChange={(e) => handleSettingChange('compressionEnabled', e.target.checked)}
                  />
                }
                label="Enable Compression"
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Paper>
  );
};