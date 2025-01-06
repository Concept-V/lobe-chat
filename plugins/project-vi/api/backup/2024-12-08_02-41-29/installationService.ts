import { BackendConfig } from '../types/config';
import * as yaml from 'js-yaml';
import path from 'path';
import { RollbackService } from './rollbackService';

export class InstallationService {
  private rollbackService: RollbackService;

  constructor() {
    this.rollbackService = new RollbackService();
  }

  // ... (previous methods remain the same)

  async install(config: BackendConfig): Promise<void> {
    try {
      // Create backup before installation
      await this.rollbackService.createBackup(
        config,
        'Auto-backup before system changes'
      );

      // Proceed with installation
      await this.updateDockerCompose(config);
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

  // ... (rest of the methods remain the same)
}