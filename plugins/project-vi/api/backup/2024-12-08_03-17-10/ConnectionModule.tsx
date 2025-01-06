import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  Alert,
  Grid,
  Card,
  CardContent,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControlLabel,
  Switch,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Check as CheckIcon,
} from '@mui/icons-material';

interface Connection {
  id: string;
  name: string;
  type: 'memory' | 'system' | 'automation';
  endpoint: string;
  apiKey?: string;
  enabled: boolean;
  config: Record<string, any>;
}

export const ConnectionModule: React.FC = () => {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [editingConnection, setEditingConnection] = useState<Connection | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [testStatus, setTestStatus] = useState<Record<string, boolean>>({});
  const [error, setError] = useState<string | null>(null);

  // Load saved connections from local storage
  useEffect(() => {
    const savedConnections = localStorage.getItem('claude-connections');
    if (savedConnections) {
      setConnections(JSON.parse(savedConnections));
    }
  }, []);

  // Save connections to local storage when updated
  useEffect(() => {
    localStorage.setItem('claude-connections', JSON.stringify(connections));
  }, [connections]);

  const handleAddConnection = () => {
    setEditingConnection({
      id: Date.now().toString(),
      name: '',
      type: 'memory',
      endpoint: '',
      enabled: true,
      config: {},
    });
    setDialogOpen(true);
  };

  const handleEditConnection = (connection: Connection) => {
    setEditingConnection(connection);
    setDialogOpen(true);
  };

  const handleSaveConnection = () => {
    if (!editingConnection) return;

    setConnections(prev => {
      const newConnections = editingConnection.id
        ? prev.map(c => c.id === editingConnection.id ? editingConnection : c)
        : [...prev, editingConnection];
      return newConnections;
    });

    setDialogOpen(false);
    setEditingConnection(null);
  };

  const handleDeleteConnection = (id: string) => {
    setConnections(prev => prev.filter(c => c.id !== id));
  };

  const handleTestConnection = async (connection: Connection) => {
    try {
      // Test the connection based on type
      const response = await fetch(connection.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(connection.apiKey && { 'Authorization': `Bearer ${connection.apiKey}` }),
        },
        body: JSON.stringify({ type: 'test' }),
      });

      if (!response.ok) throw new Error('Connection failed');

      setTestStatus(prev => ({
        ...prev,
        [connection.id]: true,
      }));

      setTimeout(() => {
        setTestStatus(prev => ({
          ...prev,
          [connection.id]: false,
        }));
      }, 3000);

    } catch (err) {
      setError(`Failed to test connection: ${err}`);
    }
  };

  const renderConnectionCard = (connection: Connection) => (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">{connection.name}</Typography>
          <Box>
            {testStatus[connection.id] && (
              <CheckIcon color="success" sx={{ mr: 1 }} />
            )}
            <IconButton 
              onClick={() => handleTestConnection(connection)}
              size="small"
              sx={{ mr: 1 }}
            >
              <CheckIcon />
            </IconButton>
            <IconButton 
              onClick={() => handleEditConnection(connection)}
              size="small"
              sx={{ mr: 1 }}
            >
              <EditIcon />
            </IconButton>
            <IconButton 
              onClick={() => handleDeleteConnection(connection.id)}
              size="small"
              color="error"
            >
              <DeleteIcon />
            </IconButton>
          </Box>
        </Box>

        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="text.secondary">Type</Typography>
            <Typography>{connection.type}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="text.secondary">Endpoint</Typography>
            <Typography>{connection.endpoint}</Typography>
          </Grid>
        </Grid>

        <FormControlLabel
          control={
            <Switch
              checked={connection.enabled}
              onChange={(e) => {
                setConnections(prev => prev.map(c => 
                  c.id === connection.id 
                    ? { ...c, enabled: e.target.checked }
                    : c
                ));
              }}
            />
          }
          label="Enabled"
        />
      </CardContent>
    </Card>
  );

  return (
    <Paper sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5">Connection Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAddConnection}
        >
          Add Connection
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {connections.map(renderConnectionCard)}

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingConnection?.id ? 'Edit Connection' : 'New Connection'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Name"
              fullWidth
              value={editingConnection?.name || ''}
              onChange={(e) => setEditingConnection(prev => 
                prev ? { ...prev, name: e.target.value } : null
              )}
            />
            <TextField
              label="Endpoint"
              fullWidth
              value={editingConnection?.endpoint || ''}
              onChange={(e) => setEditingConnection(prev => 
                prev ? { ...prev, endpoint: e.target.value } : null
              )}
            />
            <TextField
              label="API Key (optional)"
              fullWidth
              type="password"
              value={editingConnection?.apiKey || ''}
              onChange={(e) => setEditingConnection(prev => 
                prev ? { ...prev, apiKey: e.target.value } : null
              )}
            />
            {/* Add more configuration fields based on connection type */}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveConnection} variant="contained">Save</Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );
};