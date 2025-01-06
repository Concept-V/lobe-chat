import { BackendConfig } from '../types/config';
import * as yaml from 'js-yaml';
import path from 'path';

export class InstallationService {
  private async readExistingConfig(): Promise<any> {
    try {
      const response = await fetch('/api/read-file?path=docker-compose.yml');
      const content = await response.text();
      return yaml.load(content);
    } catch (error) {
      throw new Error(`Failed to read existing docker-compose.yml: ${error}`);
    }
  }

  private async updateDockerCompose(config: BackendConfig): Promise<void> {
    try {
      // Read existing configuration
      const existingConfig = await this.readExistingConfig();

      // Preserve existing services and settings
      const updatedConfig = {
        version: existingConfig.version,
        services: {
          ...existingConfig.services,
          // Add or update service configurations based on enabled systems
          ...(config.memory.enabled && this.getMemoryServices(config.memory)),
          ...(config.automation.enabled && this.getAutomationServices(config.automation)),
        },
        volumes: {
          ...existingConfig.volumes,
          ...(config.memory.longTermStorage === 'postgres' && { postgres_data: {} }),
        },
      };

      // Update environment variables for existing services
      if (updatedConfig.services.api) {
        updatedConfig.services.api.environment = {
          ...updatedConfig.services.api.environment,
          MEMORY_ENABLED: config.memory.enabled,
          MEMORY_STORAGE: config.memory.longTermStorage,
          AUTOMATION_ENABLED: config.automation.enabled,
          MAX_CONCURRENT_TASKS: config.automation.maxConcurrent,
        };
      }

      // Convert to YAML and write back
      const yamlContent = yaml.dump(updatedConfig, {
        indent: 2,
        lineWidth: -1,
      });

      await this.writeFile('docker-compose.yml', yamlContent);
    } catch (error) {
      throw new Error(`Failed to update docker-compose.yml: ${error}`);
    }
  }

  private getMemoryServices(memoryConfig: any): Record<string, any> {
    if (memoryConfig.longTermStorage === 'postgres') {
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

  private getAutomationServices(automationConfig: any): Record<string, any> {
    if (automationConfig.enabled) {
      return {
        automation_worker: {
          build: {
            context: './src/workers',
            dockerfile: 'Dockerfile',
          },
          environment: {
            MAX_CONCURRENT: automationConfig.maxConcurrent,
          },
          depends_on: ['redis'],
        },
      };
    }
    return {};
  }

  private async writeFile(filePath: string, content: string): Promise<void> {
    try {
      // Convert to Windows path format
      const windowsPath = filePath.replace(/\//g, '\\');
      
      const response = await fetch('/api/write-file', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          path: windowsPath, 
          content 
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to write file');
      }
    } catch (error) {
      throw new Error(`Failed to write file: ${error}`);
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
MAX_CONCURRENT_TASKS=${config.automation.maxConcurrent}

# Learning System
LEARNING_ENABLED=${config.learning.enabled}
STORAGE_LIMIT=${config.learning.storageLimit}
`;

    await this.writeFile('.env', envContent);
  }

  async install(config: BackendConfig): Promise<void> {
    try {
      // Update docker-compose.yml
      await this.updateDockerCompose(config);

      // Update environment configuration
      await this.updateEnvFile(config);

      // Create necessary directories with Windows paths
      const directories = [
        'src\\workers',
        'config\\nginx',
        'config\\prometheus',
        'logs',
      ];

      for (const dir of directories) {
        await fetch('/api/create-directory', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ path: dir }),
        });
      }

    } catch (error) {
      throw new Error(`Installation failed: ${error}`);
    }
  }

  async verifyInstallation(): Promise<boolean> {
    try {
      // Verify file existence and content
      const filesToCheck = [
        'docker-compose.yml',
        '.env',
      ];

      for (const file of filesToCheck) {
        const response = await fetch(`/api/read-file?path=${file}`);
        if (!response.ok) {
          return false;
        }
      }

      return true;
    } catch (error) {
      throw new Error(`Verification failed: ${error}`);
    }
  }
}