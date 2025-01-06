export const installationPresets = {
  // Quick-start profiles
  profiles: {
    basic: {
      id: 'basic',
      name: 'Basic Setup',
      description: 'Perfect for getting started with Claude',
      icon: 'Brain',
      servers: ['memory', 'filesystem'],
      features: {
        darkMode: true,
        autoStart: false,
        logging: 'basic'
      }
    },
    professional: {
      id: 'professional',
      name: 'Professional Setup',
      description: 'Enhanced capabilities for work environments',
      icon: 'Briefcase',
      servers: ['memory', 'filesystem', 'github', 'gdrive'],
      features: {
        darkMode: true,
        autoStart: true,
        logging: 'detailed'
      }
    },
    developer: {
      id: 'developer',
      name: 'Developer Setup',
      description: 'Full development environment integration',
      icon: 'Code',
      servers: ['memory', 'filesystem', 'github', 'postgres'],
      features: {
        darkMode: true,
        autoStart: true,
        logging: 'debug'
      }
    }
  },

  // Pre-configured MCP server bundles
  serverBundles: {
    essential: {
      name: 'Essential Tools',
      servers: [
        {
          name: '@modelcontextprotocol/server-memory',
          config: {
            retentionPeriod: '7d',
            contextDepth: 'medium'
          }
        },
        {
          name: '@modelcontextprotocol/server-filesystem',
          config: {
            allowedPaths: ['Documents', 'Downloads'],
            permissions: ['read', 'write']
          }
        }
      ]
    },
    collaboration: {
      name: 'Team Collaboration',
      servers: [
        {
          name: '@modelcontextprotocol/server-github',
          config: {
            scope: ['repo', 'user'],
            cacheTimeout: 3600
          }
        },
        {
          name: '@modelcontextprotocol/server-gdrive',
          config: {
            scope: ['drive.file', 'drive.readonly'],
            cacheStrategy: 'moderate'
          }
        }
      ]
    },
    development: {
      name: 'Development Tools',
      servers: [
        {
          name: '@modelcontextprotocol/server-postgres',
          config: {
            maxConnections: 5,
            queryTimeout: 30000
          }
        },
        {
          name: '@modelcontextprotocol/server-github',
          config: {
            scope: ['repo', 'workflow'],
            cacheTimeout: 3600
          }
        }
      ]
    }
  },

  // Memory system configurations
  memoryConfigs: {
    basic: {
      retentionPeriod: '24h',
      contextDepth: 'shallow',
      privacyLevel: 'high',
      backupEnabled: true
    },
    standard: {
      retentionPeriod: '7d',
      contextDepth: 'medium',
      privacyLevel: 'standard',
      backupEnabled: true
    },
    advanced: {
      retentionPeriod: '30d',
      contextDepth: 'deep',
      privacyLevel: 'custom',
      backupEnabled: true
    }
  },

  // File system configurations
  filesystemConfigs: {
    basic: {
      allowedPaths: ['Documents', 'Downloads'],
      permissions: ['read', 'write'],
      backupEnabled: true
    },
    professional: {
      allowedPaths: ['Documents', 'Downloads', 'Projects'],
      permissions: ['read', 'write', 'execute'],
      backupEnabled: true,
      watchEnabled: true
    }
  },

  // Default validation rules
  validationRules: {
    checkDiskSpace: true,
    verifyPermissions: true,
    testConnections: true,
    validateConfigs: true
  }
};