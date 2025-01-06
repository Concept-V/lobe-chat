import React from 'react';
import { Brain, Layers, AlertCircle } from 'lucide-react';

const ContextConfig = ({ config, onChange }) => {
  const handleSliderChange = (e) => {
    onChange('contextDepth', parseInt(e.target.value));
  };

  const getContextDescription = (depth) => {
    if (depth <= 3) return 'Basic context maintenance for simple conversations';
    if (depth <= 6) return 'Balanced memory for professional interactions';
    return 'Deep context awareness for complex, long-term collaborations';
  };

  const contextCategories = [
    {
      id: 'personal',
      name: 'Personal Context',
      description: 'Names, preferences, and interaction styles',
      enabled: true,
      required: true
    },
    {
      id: 'conversational',
      name: 'Conversation History',
      description: 'Previous discussions and decisions',
      enabled: config.contextCategories.includes('conversational')
    },
    {
      id: 'technical',
      name: 'Technical Knowledge',
      description: 'Code, documentation, and technical concepts',
      enabled: config.contextCategories.includes('technical')
    },
    {
      id: 'project',
      name: 'Project Context',
      description: 'Project goals, requirements, and progress',
      enabled: config.contextCategories.includes('project')
    }
  ];

  return (
    <div className="space-y-8">
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Context Depth</h3>
        <div className="space-y-4">
          <div className="flex items-center space-x-4">
            <Brain className="w-5 h-5 text-purple-600" />
            <input
              type="range"
              min="1"
              max="10"
              value={config.contextDepth}
              onChange={handleSliderChange}
              className="w-full h-2 bg-purple-200 rounded-lg appearance-none cursor-pointer"
            />
            <span className="text-sm font-medium text-purple-600">
              {config.contextDepth}/10
            </span>
          </div>
          <p className="text-sm text-gray-600">{getContextDescription(config.contextDepth)}</p>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Memory Categories</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {contextCategories.map((category) => (
            <div
              key={category.id}
              className={`border rounded-lg p-4 ${
                category.enabled ? 'border-purple-200 bg-purple-50' : 'border-gray-200'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Layers className="w-5 h-5 text-purple-600" />
                  <div>
                    <h4 className="font-medium text-gray-900">{category.name}</h4>
                    <p className="text-sm text-gray-600">{category.description}</p>
                  </div>
                </div>
                {!category.required && (
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={category.enabled}
                      onChange={() => {
                        const newCategories = category.enabled
                          ? config.contextCategories.filter(id => id !== category.id)
                          : [...config.contextCategories, category.id];
                        onChange('contextCategories', newCategories);
                      }}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
                  </label>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {config.contextDepth > 7 && (
        <div className="flex items-start space-x-3 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-sm font-medium text-yellow-800">High Context Depth Selected</h4>
            <p className="mt-1 text-sm text-yellow-700">
              With this setting, Claude will maintain detailed memory of conversations and context. 
              This may impact response speed and increase token usage. Consider if this depth is necessary for your use case.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContextConfig;