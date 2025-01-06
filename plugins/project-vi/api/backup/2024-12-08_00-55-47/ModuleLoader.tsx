import React, { Suspense } from 'react';
import { Box, CircularProgress } from '@mui/material';
import { useModuleStore } from '../../stores/moduleStore';

export const ModuleLoader: React.FC = () => {
  const { activeModules } = useModuleStore();

  return (
    <Box sx={{ display: 'flex', flexGrow: 1, flexWrap: 'wrap', gap: 2, p: 2 }}>
      {activeModules.map((module) => (
        <Suspense
          key={module.id}
          fallback={
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 200 }}>
              <CircularProgress />
            </Box>
          }
        >
          <module.component />
        </Suspense>
      ))}
    </Box>
  );
};