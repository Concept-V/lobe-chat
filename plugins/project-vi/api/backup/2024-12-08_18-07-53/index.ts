import express from 'express';
import cors from 'cors';
import { promises as fs } from 'fs';
import path from 'path';
import { createLogger, format, transports } from 'winston';

// Initialize logger
const logger = createLogger({
  format: format.combine(
    format.timestamp(),
    format.json()
  ),
  transports: [
    new transports.Console(),
    new transports.File({ filename: 'logs/error.log', level: 'error' }),
    new transports.File({ filename: 'logs/combined.log' })
  ]
});

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Config directory path
const CONFIG_DIR = path.join(__dirname, '../../config');

// Ensure config directory exists
async function ensureConfigDir() {
  try {
    await fs.mkdir(CONFIG_DIR, { recursive: true });
  } catch (error) {
    logger.error('Failed to create config directory:', error);
  }
}

ensureConfigDir();

interface FileOperation {
  path: string;
  content?: string;
}

// File operations endpoints
app.get('/api/read-file', async (req, res) => {
  try {
    const filePath = path.join(CONFIG_DIR, req.query.path as string);
    const content = await fs.readFile(filePath, 'utf8');
    res.json(JSON.parse(content));
  } catch (error) {
    logger.error('Failed to read file:', error);
    res.status(404).json({ error: 'File not found or invalid' });
  }
});

app.post('/api/write-file', async (req, res) => {
  try {
    const { path: filePath, content } = req.body as FileOperation;
    const fullPath = path.join(CONFIG_DIR, filePath);
    
    // Ensure parent directory exists
    await fs.mkdir(path.dirname(fullPath), { recursive: true });
    
    // Write file
    if (typeof content === 'string') {
      await fs.writeFile(fullPath, content);
    } else if (content) {
      await fs.writeFile(fullPath, JSON.stringify(content, null, 2));
    }
    
    res.json({ success: true });
  } catch (error) {
    logger.error('Failed to write file:', error);
    res.status(500).json({ error: 'Failed to write file' });
  }
});

// Export configuration endpoint
app.post('/api/export-config', async (req, res) => {
  try {
    const config: Record<string, unknown> = {
      version: '1.0',
      timestamp: new Date().toISOString(),
      settings: {}
    };

    // Read all configuration files
    const files = await fs.readdir(CONFIG_DIR);
    for (const file of files) {
      if (file.endsWith('.json')) {
        const content = await fs.readFile(path.join(CONFIG_DIR, file), 'utf8');
        config.settings[path.basename(file, '.json')] = JSON.parse(content);
      }
    }

    // Write complete configuration
    const exportPath = path.join(CONFIG_DIR, 'claude-config-export.json');
    await fs.writeFile(exportPath, JSON.stringify(config, null, 2));

    res.json({ success: true, path: exportPath });
  } catch (error) {
    logger.error('Failed to export configuration:', error);
    res.status(500).json({ error: 'Failed to export configuration' });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

const port = process.env.PORT || 5000;
app.listen(port, () => {
  logger.info(`API server running on port ${port}`);
});