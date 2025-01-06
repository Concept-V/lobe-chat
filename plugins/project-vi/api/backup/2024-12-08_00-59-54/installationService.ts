import { BackendConfig } from '../types/config';

export class InstallationService {
  private generateDockerCompose(config: BackendConfig): string {
    return `version: '3.8'

services:
  # Core Services
  frontend:
    build:
      context: ./src/frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    volumes:
      - ./src/frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=production
    depends_on:
      - api

  api:
    build:
      context: ./src/api
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./src/api:/app
      - /app/node_modules
    environment:
      - NODE_ENV=production
      ${config.memory.enabled ? '- MEMORY_STORAGE=' + config.memory.longTermStorage : ''}
      ${config.installation.enabled ? '- AUTO_UPDATE=' + config.installation.autoUpdate : ''}
    depends_on:
      - redis
      ${config.memory.longTermStorage === 'postgres' ? '- postgres' : ''}

  # Memory System
  ${config.memory.enabled ? this.generateMemoryServices(config.memory) : ''}

  # Cache and Message Queue
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Monitoring
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus:/etc/prometheus
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    volumes:
      - ./config/grafana:/etc/grafana
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus

volumes:
  redis_data:
  ${config.memory.longTermStorage === 'postgres' ? 'postgres_data:\\n' : ''}
  prometheus_data:
  grafana_data:`;
  }

  private generateMemoryServices(memoryConfig: any): string {
    if (memoryConfig.longTermStorage === 'postgres') {
      return `
  postgres:
    image: postgres:latest
    environment:
      - POSTGRES_USER=claude
      - POSTGRES_PASSWORD=claude_password
      - POSTGRES_DB=claude_memory
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data`;
    }
    return '';
  }

  private generateNginxConfig(): string {
    return `
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }

    upstream api {
        server api:5000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /api {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}`;
  }

  private generatePromConfig(): string {
    return `
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'api'
    static_configs:
      - targets: ['api:5000']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']`;
  }

  private async writeFile(path: string, content: string): Promise<void> {
    try {
      const response = await fetch('/api/write-file', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ path, content }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to write file');
      }
    } catch (error) {
      throw new Error(`Failed to write file: ${error}`);
    }
  }

  async install(config: BackendConfig): Promise<void> {
    try {
      // Generate docker-compose.yml
      const dockerCompose = this.generateDockerCompose(config);
      await this.writeFile('docker-compose.yml', dockerCompose);

      // Generate nginx.conf
      const nginxConfig = this.generateNginxConfig();
      await this.writeFile('config/nginx/nginx.conf', nginxConfig);

      // Generate prometheus.yml
      const promConfig = this.generatePromConfig();
      await this.writeFile('config/prometheus/prometheus.yml', promConfig);

      // Generate environment files
      await this.writeFile('.env', this.generateEnvFile(config));

      // Generate initialization scripts
      await this.writeFile('scripts/init.sh', this.generateInitScript());

    } catch (error) {
      throw new Error(`Installation failed: ${error}`);
    }
  }

  private generateEnvFile(config: BackendConfig): string {
    return `
# Core Settings
NODE_ENV=production
API_PORT=5000
FRONTEND_PORT=3000

# Memory System
MEMORY_STORAGE=${config.memory.longTermStorage}
SHORT_TERM_SIZE=${config.memory.shortTermSize}

# Installation System
AUTO_UPDATE=${config.installation.autoUpdate}
CHECK_INTERVAL=${config.installation.checkInterval}

# Automation System
MAX_CONCURRENT=${config.automation.maxConcurrent}

# Learning System
STORAGE_LIMIT=${config.learning.storageLimit}

# Security
JWT_SECRET=your-secret-key
`;
  }

  private generateInitScript(): string {
    return `#!/bin/bash
set -e

# Create necessary directories
mkdir -p config/nginx
mkdir -p config/prometheus
mkdir -p config/grafana
mkdir -p logs

# Set permissions
chmod -R 755 config
chmod -R 755 logs

# Start services
docker-compose up -d

echo "Installation completed successfully!"
`;
  }

  async verifyInstallation(): Promise<boolean> {
    try {
      // Check if docker containers are running
      const response = await fetch('/api/check-containers');
      const { status } = await response.json();
      return status === 'running';
    } catch (error) {
      throw new Error(`Verification failed: ${error}`);
    }
  }
}