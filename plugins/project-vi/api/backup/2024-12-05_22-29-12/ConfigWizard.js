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
    <div className="min-h-screen bg-conceptv-bg-light p-8">
      <div className="max-w-6xl mx-auto bg-white rounded-lg shadow-lg">
        {/* Header */}
        <div className="p-6 border-b border-conceptv-brown-light">
          <div className="flex items-center space-x-3">
            <img 
              src={process.env.PUBLIC_URL + '/Icon_ConceptV_VCircle_White.png'} 
              alt="ConceptV"
              className="w-8 h-8" 
            />
            <h1 className="text-2xl font-bold text-conceptv-brown-dark">Claude Power-Up Station</h1>
          </div>
          <p className="mt-2 text-conceptv-gray-dark">Enhance Claude with powerful integrations and capabilities</p>
        </div>

        {/* Navigation */}
        <div className="flex border-b border-conceptv-brown-light">
          {['quick-start', 'power-ups', 'advanced'].map((section) => (
            <button
              key={section}
              onClick={() => setActiveSection(section)}
              className={`px-6 py-3 text-sm font-medium ${
                activeSection === section
                  ? 'border-b-2 border-conceptv-yellow text-conceptv-brown'
                  : 'text-conceptv-gray-dark hover:text-conceptv-brown'
              }`}
            >
              {section.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
            </button>
          ))}
        </div>

        {/* Content Area */}
        <div className="p-6 bg-conceptv-bg-light">
          {activeSection === 'quick-start' && (
            <div className="space-y-6">
              <div className="bg-conceptv-bg-alt p-4 rounded-lg">
                <h3 className="text-lg font-medium text-conceptv-brown">Getting Started</h3>
                <p className="mt-2 text-conceptv-brown-light">Choose your essential power-ups to enhance Claude's capabilities.</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {categories['Essential Tools'].items.map((tool) => {
                  const IconComponent = Brain;
                  return (
                    <div 
                      key={tool.id}
                      onClick={() => handlePowerUpClick(tool)}
                      className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                        selectedPowerups.includes(tool.id) 
                          ? 'border-conceptv-yellow bg-conceptv-bg-light' 
                          : 'hover:border-conceptv-yellow-sepia'
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <IconComponent className="w-5 h-5 text-conceptv-brown" />
                        <div>
                          <div className="flex items-center">
                            <h3 className="font-medium text-conceptv-brown-dark">{tool.name}</h3>
                            {tool.official && (
                              <span className="ml-2 px-2 py-1 text-xs bg-conceptv-yellow-sepia text-white rounded">Official</span>
                            )}
                          </div>
                          <p className="text-sm text-conceptv-gray-dark mt-1">{tool.description}</p>
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
                      <IconComponent className="w-6 h-6 text-conceptv-brown" />
                      <h2 className="text-xl font-semibold text-conceptv-brown-dark">{categoryName}</h2>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {category.items.map((tool) => (
                        <div 
                          key={tool.id}
                          onClick={() => handlePowerUpClick(tool)}
                          className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                            selectedPowerups.includes(tool.id) 
                              ? 'border-conceptv-yellow bg-conceptv-bg-light' 
                              : 'hover:border-conceptv-yellow-sepia'
                          }`}
                        >
                          <div className="flex items-center space-x-3">
                            <IconComponent className="w-5 h-5 text-conceptv-brown" />
                            <div>
                              <div className="flex items-center">
                                <h3 className="font-medium text-conceptv-brown-dark">{tool.name}</h3>
                                {tool.official ? (
                                  <span className="ml-2 px-2 py-1 text-xs bg-conceptv-yellow-sepia text-white rounded">Official</span>
                                ) : (
                                  <span className="ml-2 px-2 py-1 text-xs bg-conceptv-brown-light text-white rounded">Community</span>
                                )}
                              </div>
                              <p className="text-sm text-conceptv-gray-dark mt-1">{tool.description}</p>
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
              <Book className="w-5 h-5 text-conceptv-brown-light" />
              <a href="https://modelcontextprotocol.io/docs" 
                 className="text-sm text-conceptv-brown hover:text-conceptv-brown-dark">
                View Documentation
              </a>
            </div>
            <div className="flex space-x-4">
              <button className="px-4 py-2 text-conceptv-brown hover:text-conceptv-brown-dark">
                Cancel
              </button>
              <button className="px-4 py-2 bg-conceptv-yellow text-conceptv-brown-dark rounded-md hover:bg-conceptv-yellow-dark flex items-center space-x-2">
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