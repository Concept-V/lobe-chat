import React from 'react';
import { Brain, Shield, Cog } from 'lucide-react';
import { useTheme } from '../../../theme/ThemeContext';

const BasicSetup = ({ config, onChange }) => {
  const { styles } = useTheme();
  
  const accessProfiles = [
    {
      id: 'restricted',
      name: 'Basic Memory',
      description: 'Simple, conversation-level memory',
      icon: Shield,
      settings: {
        retentionPeriod: '24h',
        contextDepth: 'shallow',
        privacyLevel: 'high'
      }
    },
    {
      id: 'standard',
      name: 'Standard Memory',
      description: 'Balanced memory for general use',
      icon: Brain,
      settings: {
        retentionPeriod: '7d',
        contextDepth: 'medium',
        privacyLevel: 'standard'
      }
    },
    {
      id: 'advanced',
      name: 'Advanced Memory',
      description: 'Deep, long-term memory system',
      icon: Cog,
      settings: {
        retentionPeriod: '30d',
        contextDepth: 'deep',
        privacyLevel: 'custom'
      }
    }
  ];

  return (
    <div className="space-y-6">
      <div className={`${styles.card} bg-concept-brown-dark/10`}>
        <h3 className={styles.heading}>Choose Your Memory Profile</h3>
        <p className={styles.subheading}>
          Select a starting point for Claude's memory system. You can customize everything later.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {accessProfiles.map((profile) => {
          const IconComponent = profile.icon;
          return (
            <div
              key={profile.id}
              onClick={() => onChange('memoryProfile', profile.id)}
              className={`${styles.card} ${
                config.memoryProfile === profile.id 
                  ? styles.cardSelected
                  : styles.cardHover
              }`}
            >
              <div className="flex items-center space-x-3 mb-3">
                <IconComponent className={styles.icon} />
                <h4 className={styles.heading}>{profile.name}</h4>
              </div>
              <p className={styles.text}>{profile.description}</p>
              
              {config.memoryProfile === profile.id && (
                <div className="mt-3 pt-3 border-t border-concept-brown-light/20">
                  <ul className={`space-y-1 ${styles.text}`}>
                    <li>• Retention: {profile.settings.retentionPeriod}</li>
                    <li>• Depth: {profile.settings.contextDepth}</li>
                    <li>• Privacy: {profile.settings.privacyLevel}</li>
                  </ul>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default BasicSetup;