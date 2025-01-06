import React, { useState } from 'react';
import { 
  Save, 
  Brain,
  Book,
  Sun,
  Moon 
} from 'lucide-react';

import { categories } from './data';
import PowerUpConfig from '../PowerUpConfig';

const ConfigWizard = () => {
  const [activeSection, setActiveSection] = useState('quick-start');
  const [selectedPowerups, setSelectedPowerups] = useState([]);
  const [activePowerUp, setActivePowerUp] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(true);

  const handlePowerUpClick = (tool) => {
    setActivePowerUp(tool);
    setActiveSection('advanced');
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className={`min-h-screen ${isDarkMode ? 'dark bg-dark' : 'bg-concept-yellow-light'}`}>
      <div className="p-8">
        <div className="max-w-6xl mx-auto bg-dark-card rounded-lg shadow-xl">
          {/* Header */}
          <div className="p-6 border-b border-concept-brown-light flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <img 
                src={process.env.PUBLIC_URL + '/Icon_ConceptV_VCircle_White.png'} 
                alt="ConceptV"
                className="w-8 h-8" 
              />
              <div>
                <h1 className="text-2xl font-bold text-concept-yellow-sepia">Claude Power-Up Station</h1>
                <p className="mt-1 text-concept-yellow-light/80">Enhance Claude with powerful integrations and capabilities</p>
              </div>
            </div>
            <button 
              onClick={toggleDarkMode}
              className="p-2 rounded-full hover:bg-concept-brown-dark/20"
            >
              {isDarkMode ? 
                <Sun className="w-5 h-5 text-concept-yellow" /> : 
                <Moon className="w-5 h-5 text-concept-brown-dark" />
              }
            </button>
          </div>

          {/* Navigation */}
          <div className="flex border-b border-concept-brown-dark/20">
            {['quick-start', 'power-ups', 'advanced'].map((section) => (
              <button
                key={section}
                onClick={() => setActiveSection(section)}
                className={`px-6 py-3 text-sm font-medium transition-colors ${
                  activeSection === section
                    ? 'border-b-2 border-concept-yellow text-concept-yellow'
                    : 'text-concept-yellow-light/60 hover:text-concept-yellow-light'
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
                <div className="bg-dark/50 p-4 rounded-lg border border-concept-brown-light/20">
                  <h3 className="text-lg font-medium text-concept-yellow">Getting Started</h3>
                  <p className="mt-2 text-concept-yellow-light/80">Choose your essential power-ups to enhance Claude's capabilities.</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {categories['Essential Tools'].items.map((tool) => (
                    <div 
                      key={tool.id}
                      onClick={() => handlePowerUpClick(tool)}
                      className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                        selectedPowerups.includes(tool.id) 
                          ? 'border-concept-yellow bg-concept-brown-dark/20' 
                          : 'border-concept-brown-light/20 hover:border-concept-yellow hover:bg-concept-brown-dark/10'
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <Brain className="w-5 h-5 text-concept-yellow" />
                        <div>
                          <div className="flex items-center">
                            <h3 className="font-medium text-concept-yellow-light">{tool.name}</h3>
                            {tool.official && (
                              <span className="ml-2 px-2 py-1 text-xs bg-concept-yellow text-concept-brown-dark rounded">Official</span>
                            )}
                          </div>
                          <p className="text-sm text-concept-yellow-light/60 mt-1">{tool.description}</p>
                        </div>
                      </div>
                    </div>
                  ))}
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
                        <IconComponent className="w-6 h-6 text-concept-yellow" />
                        <h2 className="text-xl font-semibold text-concept-yellow-light">{categoryName}</h2>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {category.items.map((tool) => (
                          <div 
                            key={tool.id}
                            onClick={() => handlePowerUpClick(tool)}
                            className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                              selectedPowerups.includes(tool.id) 
                                ? 'border-concept-yellow bg-concept-brown-dark/20' 
                                : 'border-concept-brown-light/20 hover:border-concept-yellow hover:bg-concept-brown-dark/10'
                            }`}
                          >
                            <div className="flex items-center space-x-3">
                              <IconComponent className="w-5 h-5 text-concept-yellow" />
                              <div>
                                <div className="flex items-center">
                                  <h3 className="font-medium text-concept-yellow-light">{tool.name}</h3>
                                  {tool.official ? (
                                    <span className="ml-2 px-2 py-1 text-xs bg-concept-yellow text-concept-brown-dark rounded">Official</span>
                                  ) : (
                                    <span className="ml-2 px-2 py-1 text-xs bg-concept-brown text-concept-yellow-light rounded">Community</span>
                                  )}
                                </div>
                                <p className="text-sm text-concept-yellow-light/60 mt-1">{tool.description}</p>
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
            <div className="mt-6 flex justify-between items-center pt-6 border-t border-concept-brown-dark/20">
              <div className="flex items-center space-x-2">
                <Book className="w-5 h-5 text-concept-yellow-light/60" />
                <a href="https://modelcontextprotocol.io/docs" 
                   className="text-sm text-concept-yellow-light/80 hover:text-concept-yellow">
                  View Documentation
                </a>
              </div>
              <div className="flex space-x-4">
                <button className="px-4 py-2 text-concept-yellow-light/80 hover:text-concept-yellow">
                  Cancel
                </button>
                <button className="px-4 py-2 bg-concept-yellow text-concept-brown-dark rounded-md hover:bg-concept-yellow-dark flex items-center space-x-2">
                  <Save className="w-4 h-4" />
                  <span>Save Configuration</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfigWizard;