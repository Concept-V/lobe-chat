import { BackendInstallModule } from '@/components/modules/BackendInstallModule';
import { MemoryModule } from '@/components/modules/MemoryModule';
import { SystemIntegrationModule } from '@/components/modules/SystemIntegrationModule';
import { ModuleConfig } from '@/types/module';

export const defaultModules: ModuleConfig[] = [
  {
    id: 'memory-management',
    name: 'Memory Management',
    description: 'Configure and monitor Claude memory usage',
    component: MemoryModule,
    enabled: true,
  },
  {
    id: 'system-integration',
    name: 'System Integration',
    description: 'Monitor system resources and service status',
    component: SystemIntegrationModule,
    enabled: true,
  },
  {
    id: 'backend-install',
    name: 'Backend Installation',
    description: 'Install and configure backend systems',
    component: BackendInstallModule,
    enabled: true,
  },
];