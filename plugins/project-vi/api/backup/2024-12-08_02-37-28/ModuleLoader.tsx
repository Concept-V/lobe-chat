import React, { Suspense } from 'react';
import { Box, CircularProgress, Paper, Typography } from '@mui/material';
import { useModuleStore } from '../../stores/moduleStore';

export const ModuleLoader: React.FC = () => {
  const { activeModules } = useModuleStore();

  if (activeModules.length === 0) {
    return (
      <Paper sx={{ p: 2 }}>
        <Typography>No active modules</Typography>
      </Paper>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      {activeModules.map((module) => (
        <Paper key={module.id} sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>{module.name}</Typography>
          <Suspense
            fallback={
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
                <CircularProgress />
              </Box>
            }
          >
            <module.component config={module.config} />
          </Suspense>
        </Paper>
      ))}
    </Box>
  );
};