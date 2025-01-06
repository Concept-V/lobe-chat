import create from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { configService } from '../services/configService';
import { installationService } from '../services/installationService';

const useStore = create(
  devtools(
    persist(
      (set, get) => ({
        // Installation State
        installationConfig: null,
        installationStep: 'welcome',
        dependencies: [],
        
        // Power-up Configurations
        powerUps: {},
        selectedPowerUps: [],
        
        // UI State
        activeSection: 'home',
        activePowerUp: null,
        
        // Actions
        setInstallationConfig: (config) => set({ installationConfig: config }),
        setInstallationStep: (step) => set({ installationStep: step }),
        
        addPowerUp: (id, config) => set((state) => ({
          powerUps: { ...state.powerUps, [id]: config }
        })),
        
        togglePowerUp: (id) => set((state) => ({
          selectedPowerUps: state.selectedPowerUps.includes(id)
            ? state.selectedPowerUps.filter(p => p !== id)
            : [...state.selectedPowerUps, id]
        })),
        
        setActiveSection: (section) => set({ activeSection: section }),
        setActivePowerUp: (powerUp) => set({ activePowerUp: powerUp }),
        
        // Complex Actions
        startInstallation: async () => {
          const state = get();
          const script = installationService.generateInstallationScript({
            selectedServers: state.selectedPowerUps,
            config: state.powerUps
          });
          
          if (state.computerUseEnabled) {
            return installationService.generateComputerUseInstructions({
              selectedServers: state.selectedPowerUps,
              config: state.powerUps
            });
          }
          
          return script;
        },
        
        saveConfiguration: async () => {
          const state = get();
          return configService.saveConfig({
            powerUps: state.powerUps,
            selectedPowerUps: state.selectedPowerUps,
            installationConfig: state.installationConfig
          }, 'claude_config');
        },
        
        loadConfiguration: async () => {
          const config = await configService.loadConfig('claude_config');
          if (config) {
            set({
              powerUps: config.powerUps || {},
              selectedPowerUps: config.selectedPowerUps || [],
              installationConfig: config.installationConfig
            });
          }
        },
        
        // Export/Import
        exportConfiguration: () => {
          const state = get();
          return {
            powerUps: state.powerUps,
            selectedPowerUps: state.selectedPowerUps,
            installationConfig: state.installationConfig
          };
        },
        
        importConfiguration: (config) => {
          set({
            powerUps: config.powerUps || {},
            selectedPowerUps: config.selectedPowerUps || [],
            installationConfig: config.installationConfig
          });
        }
      }),
      {
        name: 'claude-config-storage',
        getStorage: () => localStorage
      }
    )
  )
);

export default useStore;