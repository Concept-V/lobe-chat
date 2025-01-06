import React from 'react';
import { 
  Settings, 
  Brain,
  Book,
  Sun,
  Moon,
  Wrench,
  Terminal,
  Database,
  Globe,
  Zap,
  Shield,
  Code,
  Workflow,
  Network,
  Box
} from 'lucide-react';

import { categories } from './data';
import { useTheme, useLogging } from '../../shared/contexts';
import PowerUpConfig from '../PowerUpConfig';
import ExportConfig from '../ExportConfig';
import InstallationWizard from '../InstallationWizard';
import { Button, Card } from '../../shared/components';

const CommandCentre = () => {
  const { styles, isDarkMode, toggleDarkMode } = useTheme();
  const { log } = useLogging();

  const sections = [
    {
      id: 'core',
      title: 'Core Systems',
      icon: Brain,
      items: [
        { id: 'memory', name: 'Memory System', icon: Brain },
        { id: 'filesystem', name: 'File System', icon: Box },
        { id: 'computer', name: 'Computer Control', icon: Terminal }
      ]
    },
    {
      id: 'integrations',
      title: 'Integrations',
      icon: Network,
      items: [
        { id: 'github', name: 'GitHub', icon: Globe },
        { id: 'slack', name: 'Slack', icon: Globe },
        { id: 'databases', name: 'Databases', icon: Database }
      ]
    },
    {
      id: 'tools',
      title: 'Development Tools',
      icon: Wrench,
      items: [
        { id: 'monitoring', name: 'Monitoring', icon: Zap },
        { id: 'security', name: 'Security', icon: Shield },
        { id: 'automation', name: 'Automation', icon: Workflow }
      ]
    },
    {
      id: 'settings',
      title: 'System Settings',
      icon: Settings,
      items: [
        { id: 'performance', name: 'Performance', icon: Zap },
        { id: 'backup', name: 'Backup & Restore', icon: Box },
        { id: 'advanced', name: 'Advanced', icon: Code }
      ]
    }
  ];

  return (
    <div className={`min-h-screen ${isDarkMode ? 'dark bg-dark' : 'bg-concept-yellow-light'}`}>
      <div className="p-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <header className={`${styles.card} p-6 mb-8`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <img 
                  src={process.env.PUBLIC_URL + '/Icon_ConceptV_VCircle_White.png'} 
                  alt="Vi"
                  className="w-12 h-12" 
                />
                <div>
                  <h1 className={`text-3xl font-bold ${styles.heading}`}>Vi Command Centre</h1>
                  <p className={styles.subheading}>System Configuration and Control</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <Button 
                  variant="icon"
                  onClick={toggleDarkMode}
                  icon={isDarkMode ? Sun : Moon}
                  tooltip={isDarkMode ? "Light Mode" : "Dark Mode"}
                />
                <Button 
                  variant="primary"
                  icon={Settings}
                >
                  Settings
                </Button>
              </div>
            </div>
          </header>

          {/* Quick Actions */}
          <section className="mb-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card className="p-6 text-center">
                <Terminal className={`${styles.icon} w-8 h-8 mx-auto mb-4`} />
                <h3 className={styles.heading}>Quick Setup</h3>
                <p className={`${styles.text} mb-4`}>First time setup and configuration</p>
                <Button variant="secondary" fullWidth>Start Setup</Button>
              </Card>
              
              <Card className="p-6 text-center">
                <Code className={`${styles.icon} w-8 h-8 mx-auto mb-4`} />
                <h3 className={styles.heading}>Developer Mode</h3>
                <p className={`${styles.text} mb-4`}>Advanced tools and configurations</p>
                <Button variant="secondary" fullWidth>Enable</Button>
              </Card>

              <Card className="p-6 text-center">
                <Shield className={`${styles.icon} w-8 h-8 mx-auto mb-4`} />
                <h3 className={styles.heading}>Security Check</h3>
                <p className={`${styles.text} mb-4`}>Review system security status</p>
                <Button variant="secondary" fullWidth>Review</Button>
              </Card>

              <Card className="p-6 text-center">
                <Zap className={`${styles.icon} w-8 h-8 mx-auto mb-4`} />
                <h3 className={styles.heading}>Performance</h3>
                <p className={`${styles.text} mb-4`}>System performance metrics</p>
                <Button variant="secondary" fullWidth>Monitor</Button>
              </Card>
            </div>
          </section>

          {/* Main Sections */}
          {sections.map(section => (
            <section key={section.id} className="mb-8">
              <div className="flex items-center space-x-3 mb-4">
                <section.icon className={`${styles.icon} w-6 h-6`} />
                <h2 className={`text-xl font-semibold ${styles.heading}`}>{section.title}</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {section.items.map(item => (
                  <Card 
                    key={item.id}
                    className="p-6 hover:border-concept-yellow cursor-pointer"
                    onClick={() => log('info', `Selected ${item.name}`)}
                  >
                    <div className="flex items-center space-x-4">
                      <item.icon className={`${styles.icon} w-8 h-8`} />
                      <div>
                        <h3 className={styles.heading}>{item.name}</h3>
                        <p className={styles.text}>Configure and manage {item.name.toLowerCase()}</p>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </section>
          ))}

          {/* Footer */}
          <footer className={`${styles.card} p-6 mt-8`}>
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <Book className={styles.iconSecondary} />
                <a href="/docs" className={styles.buttonSecondary}>Documentation</a>
              </div>
              <div className="flex items-center space-x-4">
                <span className={styles.text}>Version 1.0.0</span>
                <Button variant="primary" icon={Globe}>Updates</Button>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </div>
  );
};

export default CommandCentre;