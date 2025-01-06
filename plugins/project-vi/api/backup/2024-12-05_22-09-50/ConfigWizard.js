import React, { useState } from 'react';
import { 
  Settings, 
  ChevronRight, 
  Plus, 
  Save, 
  Terminal, 
  Database, 
  FileText, 
  Brain,
  Globe, 
  MessageSquare, 
  Shield, 
  Search, 
  Map, 
  Monitor, 
  Cloud, 
  Robot, 
  Book 
} from 'lucide-react';

// Import our categories data
import { categories } from './data';
import PowerUpConfig from '../PowerUpConfig';

const ConfigWizard = () => {
  const [activeSection, setActiveSection] = useState('quick-start');
  const [selectedPowerups, setSelectedPowerups] = useState([]);
  const [activePowerUp, setActivePowerUp] = useState(null);

  const handleToolSelect = (toolId) => {
    setSelectedPowerups(prev => 
      prev.includes(toolId) 
        ? prev.filter(id => id !== toolId)
        : [...prev, toolId]
    );
  };

  const handlePowerUpClick = (tool) => {
    setActivePowerUp(tool);
    setActiveSection('advanced');
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto bg-white rounded-lg shadow-lg">
        {/* Header */}
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <Settings className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">Claude Power-Up Station</h1>
          </div>
          <p className="mt-2 text-gray-600">Enhance Claude with powerful integrations and capabilities</p>
        </div>

        {/* Navigation */}
        <div className="flex border-b border-gray-200">
          {['quick-start', 'power-ups', 'advanced'].map((section) => (
            <button
              key={section}
              onClick={() => setActiveSection(section)}
              className={`px-6 py-3 text-sm font-medium ${
                activeSection === section
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {section.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
            </button>
          ))}
        </div>

        {/* Content Area */}
        <div className="p-6">
          {activeSection === 'quick-start' && (
            <div className="space-y-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h3 className="text-lg font-medium text-blue-900">Getting Started</h3>
                <p className="mt-2 text-blue-700">Choose your essential power-ups to enhance Claude's capabilities.</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {categories['Essential Tools'].items.map((tool) => {
                  const IconComponent = Brain;
                  return (
                    <div 
                      key={tool.id}
                      onClick={() => handlePowerUpClick(tool)}
                      className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                        selectedPowerups.includes(tool.id) ? 'border-blue-500 bg-blue-50' : 'hover:border-blue-500'
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <IconComponent className="w-5 h-5 text-blue-600" />
                        <div>
                          <div className="flex items-center">
                            <h3 className="font-medium text-gray-900">{tool.name}</h3>
                            {tool.official && (
                              <span className="ml-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">Official</span>
                            )}
                          </div>
                          <p className="text-sm text-gray-500 mt-1">{tool.description}</p>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {activeSection === 'power-ups' && (
            <div className="space-y-8">
              {Object.entries(categories).map(([categoryName, category]) => {
                const IconComponent = category.icon;
                return (
                  <div key={categoryName} className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <IconComponent className="w-6 h-6 text-blue-600" />
                      <h2 className="text-xl font-semibold text-gray-900">{categoryName}</h2>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {category.items.map((tool) => (
                        <div 
                          key={tool.id}
                          onClick={() => handlePowerUpClick(tool)}
                          className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                            selectedPowerups.includes(tool.id) ? 'border-blue-500 bg-blue-50' : 'hover:border-blue-500'
                          }`}
                        >
                          <div className="flex items-center space-x-3">
                            <IconComponent className="w-5 h-5 text-blue-600" />
                            <div>
                              <div className="flex items-center">
                                <h3 className="font-medium text-gray-900">{tool.name}</h3>
                                {tool.official ? (
                                  <span className="ml-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">Official</span>
                                ) : (
                                  <span className="ml-2 px-2 py-1 text-xs bg-green-100 text-green-800 rounded">Community</span>
                                )}
                              </div>
                              <p className="text-sm text-gray-500 mt-1">{tool.description}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {activeSection === 'advanced' && activePowerUp && (
            <PowerUpConfig powerUp={activePowerUp} />
          )}

          {/* Footer */}
          <div className="mt-6 flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <Book className="w-5 h-5 text-gray-400" />
              <a href="https://modelcontextprotocol.io/docs" 
                 className="text-sm text-gray-600 hover:text-gray-900">
                View Documentation
              </a>
            </div>
            <div className="flex space-x-4">
              <button className="px-4 py-2 text-gray-700 hover:text-gray-900">
                Cancel
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center space-x-2">
                <Save className="w-4 h-4" />
                <span>Save Configuration</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfigWizard;