import React from 'react';
import { Card, CardContent, Typography, Box, CircularProgress } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import PauseCircleIcon from '@mui/icons-material/PauseCircle';

interface SystemStatusCardProps {
  systemId: string;
  status: 'not-installed' | 'installing' | 'installed' | 'error';
  enabled: boolean;
}

export const SystemStatusCard: React.FC<SystemStatusCardProps> = ({
  systemId,
  status,
  enabled,
}) => {
  const getStatusIcon = () => {
    if (!enabled) return <PauseCircleIcon color="disabled" />;
    
    switch (status) {
      case 'installed':
        return <CheckCircleIcon color="success" />;
      case 'installing':
        return <CircularProgress size={24} />;
      case 'error':
        return <ErrorIcon color="error" />;
      default:
        return <PauseCircleIcon color="disabled" />;
    }
  };

  const getStatusColor = () => {
    if (!enabled) return 'text.disabled';
    
    switch (status) {
      case 'installed':
        return 'success.main';
      case 'installing':
        return 'info.main';
      case 'error':
        return 'error.main';
      default:
        return 'text.disabled';
    }
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {getStatusIcon()}
          <Typography variant="h6" sx={{ textTransform: 'capitalize' }}>
            {systemId.replace(/-/g, ' ')}
          </Typography>
        </Box>
        <Typography 
          variant="body2" 
          sx={{ 
            mt: 1,
            color: getStatusColor(),
            textTransform: 'capitalize'
          }}
        >
          {enabled ? status : 'Disabled'}
        </Typography>
      </CardContent>
    </Card>
  );
};