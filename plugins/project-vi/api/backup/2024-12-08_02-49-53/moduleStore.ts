import create from 'zustand';
import { ModuleConfig } from '../types/module';

interface ModuleState {
  activeModules: ModuleConfig[];
  addModule: (module: ModuleConfig) => void;
  removeModule: (moduleId: string) => void;
}

export const useModuleStore = create<ModuleState>((set) => ({
  activeModules: [],
  addModule: (module) =>
    set((state) => ({
      activeModules: [...state.activeModules, module],
    })),
  removeModule: (moduleId) =>
    set((state) => ({
      activeModules: state.activeModules.filter((m) => m.id !== moduleId),
    })),
}));