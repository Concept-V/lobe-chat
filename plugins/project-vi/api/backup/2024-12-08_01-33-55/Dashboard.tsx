import React from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  useTheme,
} from '@mui/material';
import {
  Memory as MemoryIcon,
  Settings as SettingsIcon,
  Code as CodeIcon,
  AutoFixHigh as AutomationIcon,
  Psychology as LearningIcon,
  Menu as MenuIcon,
} from '@mui/icons-material';
import { useSystemStatus } from '../../hooks/useSystemStatus';
import { SystemStatusCard } from './SystemStatusCard';
import { ConfigPanel } from './ConfigPanel';

export const Dashboard: React.FC = () => {
  const theme = useTheme();
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const [activeSystem, setActiveSystem] = React.useState<string | null>(null);
  const { systems, loading, error } = useSystemStatus();

  const systemIcons = {
    memory: MemoryIcon,
    installation: SettingsIcon,
    sdk: CodeIcon,
    automation: AutomationIcon,
    learning: LearningIcon,
  };

  const handleSystemClick = (systemId: string) => {
    setActiveSystem(systemId);
    setDrawerOpen(false);
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      {/* Navigation Drawer */}
      <Drawer
        variant="permanent"
        sx={{
          width: 240,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 240,
            boxSizing: 'border-box',
            backgroundColor: theme.palette.background.paper,
          },
        }}
      >
        <Box sx={{ p: 2, display: 'flex', alignItems: 'center' }}>
          <IconButton edge="start" onClick={() => setDrawerOpen(!drawerOpen)}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" sx={{ ml: 2 }}>
            Command Center
          </Typography>
        </Box>
        <List>
          {Object.entries(systems).map(([id, system]) => {
            const Icon = systemIcons[id as keyof typeof systemIcons];
            return (
              <ListItem
                button
                key={id}
                onClick={() => handleSystemClick(id)}
                selected={activeSystem === id}
              >
                <ListItemIcon>
                  <Icon color={system.status === 'running' ? 'success' : 'error'} />
                </ListItemIcon>
                <ListItemText
                  primary={system.name}
                  secondary={system.status}
                />
              </ListItem>
            );
          })}
        </List>
      </Drawer>

      {/* Main Content */}
      <Box sx={{ flexGrow: 1, p: 3 }}>
        <Grid container spacing={3}>
          {/* System Status Cards */}
          {Object.entries(systems).map(([id, system]) => (
            <Grid item xs={12} md={6} lg={4} key={id}>
              <SystemStatusCard
                id={id}
                system={system}
                onClick={() => handleSystemClick(id)}
              />
            </Grid>
          ))}
        </Grid>

        {/* Active System Configuration */}
        {activeSystem && (
          <Paper sx={{ mt: 3, p: 2 }}>
            <ConfigPanel
              systemId={activeSystem}
              config={systems[activeSystem].config}
            />
          </Paper>
        )}
      </Box>
    </Box>
  );
};