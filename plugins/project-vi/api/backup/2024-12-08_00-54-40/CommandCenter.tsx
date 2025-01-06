import React from 'react';
import { Box, ThemeProvider } from '@mui/material';
import { theme } from '../../theme';
import { ModuleLoader } from './ModuleLoader';

export const CommandCenter: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: 'flex', height: '100vh' }}>
        <ModuleLoader />
      </Box>
    </ThemeProvider>
  );
};