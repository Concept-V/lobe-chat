import { BackendInstallModule } from '@/components/modules/BackendInstallModule';
import { ModuleConfig } from '@/types/module';

export const defaultModules: ModuleConfig[] = [
  {
    id: 'backend-install',
    name: 'Backend Installation',
    description: 'Install and configure backend systems',
    component: BackendInstallModule,
    enabled: true,
  },
];