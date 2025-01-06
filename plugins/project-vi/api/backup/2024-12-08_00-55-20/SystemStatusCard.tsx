import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  LinearProgress,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Settings as SettingsIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { SystemStatus } from '../../types/system';

interface SystemStatusCardProps {
  id: string;
  system: SystemStatus;
  onClick: () => void;
}

export const SystemStatusCard: React.FC<SystemStatusCardProps> = ({
  id,
  system,
  onClick,
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'success';
      case 'stopped':
        return 'error';
      case 'starting':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getHealthIndicator = (health: number) => {
    if (health >= 90) return { color: 'success', label: 'Healthy' };
    if (health >= 70) return { color: 'warning', label: 'Warning' };
    return { color: 'error', label: 'Critical' };
  };

  const healthInfo = getHealthIndicator(system.health);

  return (
    <Card
      sx={{
        minWidth: 300,
        position: 'relative',
        '&:hover': {
          boxShadow: 6,
        },
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" component="div">
            {system.name}
          </Typography>
          <Chip
            label={system.status}
            color={getStatusColor(system.status) as any}
            size="small"
          />
        </Box>

        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Health
            </Typography>
            <Chip
              label={healthInfo.label}
              color={healthInfo.color as any}
              size="small"
            />
          </Box>
          <LinearProgress
            variant="determinate"
            value={system.health}
            color={healthInfo.color as any}
          />
        </Box>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
          {system.metrics.map((metric) => (
            <Box
              key={metric.name}
              sx={{ display: 'flex', justifyContent: 'space-between' }}
            >
              <Typography variant="body2" color="text.secondary">
                {metric.name}
              </Typography>
              <Typography variant="body2">
                {metric.value} {metric.unit}
              </Typography>
            </Box>
          ))}
        </Box>
      </CardContent>

      <CardActions sx={{ justifyContent: 'space-between' }}>
        <Box>
          <Tooltip title="Refresh Status">
            <IconButton size="small" onClick={(e) => {
              e.stopPropagation();
              // Refresh logic
            }}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="System Information">
            <IconButton size="small" onClick={(e) => {
              e.stopPropagation();
              // Show info dialog
            }}>
              <InfoIcon />
            </IconButton>
          </Tooltip>
        </Box>
        <Button
          size="small"
          startIcon={<SettingsIcon />}
          onClick={onClick}
        >
          Configure
        </Button>
      </CardActions>
    </Card>
  );
};