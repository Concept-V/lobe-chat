import { BackendConfig } from '@/types/config';
import { dump as yamlDump, load as yamlLoad } from 'js-yaml';

export class InstallationService {
  async verifySystemRequirements(): Promise<void> {
    // Check system requirements
    const requirements = [
      this.checkStorage(),
      this.checkMemory(),
      this.checkDocker(),
    ];

    await Promise.all(requirements);
  }

  private async checkStorage(): Promise<void> {
    if ('storage' in navigator && 'estimate' in navigator.storage) {
      const { quota, usage } = await navigator.storage.estimate();
      if (quota && usage && (quota - usage) < 100 * 1024 * 1024) {
        throw new Error('Insufficient storage space');
      }
    }
  }

  private async checkMemory(): Promise<void> {
    // Example memory check
    if (performance?.memory?.usedJSHeapSize > 0.8 * performance.memory.jsHeapSizeLimit) {
      throw new Error('Insufficient memory available');
    }
  }

  private async checkDocker(): Promise<void> {
    try {
      const response = await fetch('/api/check-docker');
      if (!response.ok) {
        throw new Error('Docker not available');
      }
    } catch (error) {
      throw new Error('Failed to verify Docker: ' + error);
    }
  }

  async install(config: BackendConfig): Promise<void> {
    try {
      // Generate and write Docker configuration
      await this.updateDockerCompose(config);
      
      // Update environment configuration
      await this.updateEnvFile(config);

      // Create necessary directories
      const directories = [
        'src/workers',
        'config/nginx',
        'config/prometheus',
        'logs',
      ];

      for (const dir of directories) {
        await fetch('/api/create-directory', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: dir }),
        });
      }
    } catch (error) {
      throw new Error(`Installation failed: ${error}`);
    }
  }

  async verifyInstallation(): Promise<boolean> {
    try {
      const checks = [
        this.checkFileExists('docker-compose.yml'),
        this.checkFileExists('.env'),
        this.checkApiHealth(),
      ];

      await Promise.all(checks);
      return true;
    } catch (error) {
      return false;
    }
  }

  private async checkFileExists(path: string): Promise<void> {
    const response = await fetch(`/api/check-file?path=${path}`);
    if (!response.ok) {
      throw new Error(`File ${path} not found`);
    }
  }

  private async checkApiHealth(): Promise<void> {
    const response = await fetch('/api/health');
    if (!response.ok) {
      throw new Error('API health check failed');
    }
  }

  private async updateDockerCompose(config: BackendConfig): Promise<void> {
    try {
      // Read existing config
      const response = await fetch('/api/read-file?path=docker-compose.yml');
      const content = await response.text();
      const existingConfig = yamlLoad(content);

      // Update configuration
      const updatedConfig = {
        ...existingConfig,
        services: {
          ...existingConfig.services,
          ...(config.memory.enabled && this.getMemoryServices(config)),
        },
      };

      // Write updated config
      await fetch('/api/write-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          path: 'docker-compose.yml',
          content: yamlDump(updatedConfig),
        }),
      });
    } catch (error) {
      throw new Error(`Failed to update docker-compose.yml: ${error}`);
    }
  }

  private async updateEnvFile(config: BackendConfig): Promise<void> {
    const envContent = `
# Environment Configuration
NODE_ENV=development

# Memory System
MEMORY_ENABLED=${config.memory.enabled}
MEMORY_STORAGE=${config.memory.longTermStorage}
SHORT_TERM_SIZE=${config.memory.shortTermSize}

# Automation System
AUTOMATION_ENABLED=${config.automation.enabled}
MAX_CONCURRENT=${config.automation.maxConcurrent}

# Learning System
LEARNING_ENABLED=${config.learning.enabled}
STORAGE_LIMIT=${config.learning.storageLimit}
`;

    try {
      await fetch('/api/write-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          path: '.env',
          content: envContent,
        }),
      });
    } catch (error) {
      throw new Error(`Failed to update .env file: ${error}`);
    }
  }

  private getMemoryServices(config: BackendConfig): Record<string, unknown> {
    if (config.memory.longTermStorage === 'postgres') {
      return {
        postgres: {
          image: 'postgres:latest',
          environment: {
            POSTGRES_USER: 'claude',
            POSTGRES_PASSWORD: 'claude_password',
            POSTGRES_DB: 'claude_memory',
          },
          ports: ['5432:5432'],
          volumes: ['postgres_data:/var/lib/postgresql/data'],
        },
      };
    }
    return {};
  }
}