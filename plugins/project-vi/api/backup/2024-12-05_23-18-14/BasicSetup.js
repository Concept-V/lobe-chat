import React from 'react';
import { Brain, Clock, Shield } from 'lucide-react';

const BasicSetup = ({ config, onChange }) => {
  const memoryProfiles = [
    {
      id: 'casual',
      name: 'Casual Assistant',
      description: 'Remembers key details about your preferences and recent interactions',
      icon: Brain,
      settings: {
        retentionPeriod: '24h',
        contextDepth: 'medium',
        privacyLevel: 'standard'
      }
    },
    {
      id: 'professional',
      name: 'Professional Collaborator',
      description: 'Maintains detailed context about projects, meetings, and work preferences',
      icon: Clock,
      settings: {
        retentionPeriod: '7d',
        contextDepth: 'deep',
        privacyLevel: 'strict'
      }
    },
    {
      id: 'researcher',
      name: 'Research Partner',
      description: 'Long-term memory for research topics, citations, and complex discussions',
      icon: Shield,
      settings: {
        retentionPeriod: '30d',
        contextDepth: 'maximum',
        privacyLevel: 'custom'
      }
    }
  ];

  return (
    <div className="space-y-6">
      <div className="bg-blue-50 rounded-lg p-4">
        <h3 className="text-lg font-medium text-blue-900">Choose Your Memory Profile</h3>
        <p className="mt-1 text-sm text-blue-700">
          Select a starting point that best matches how you'll work with Claude. You can customize everything later.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {memoryProfiles.map((profile) => {
          const IconComponent = profile.icon;
          return (
            <div
              key={profile.id}
              onClick={() => onChange('memoryProfile', profile.id)}
              className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                config.memoryProfile === profile.id 
                  ? 'border-purple-500 bg-purple-50' 
                  : 'hover:border-purple-300'
              }`}
            >
              <div className="flex items-center space-x-3 mb-3">
                <IconComponent className="w-6 h-6 text-purple-600" />
                <h4 className="font-medium text-gray-900">{profile.name}</h4>
              </div>
              <p className="text-sm text-gray-600">{profile.description}</p>
              
              {config.memoryProfile === profile.id && (
                <div className="mt-3 pt-3 border-t border-purple-200">
                  <ul className="text-xs text-purple-700 space-y-1">
                    <li>• Retention: {profile.settings.retentionPeriod}</li>
                    <li>• Context: {profile.settings.contextDepth}</li>
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