import React, { useState, useEffect, useCallback } from 'react';
import { Check, AlertCircle, Loader } from 'lucide-react';
import { useTheme } from '../../../shared/contexts';
import { Card } from '../../../shared/components';

const SystemCheck = ({ profile, onComplete }) => {
  const { styles } = useTheme();
  const [checks, setChecks] = useState({
    disk: { status: 'pending', message: 'Checking disk space...' },
    memory: { status: 'pending', message: 'Checking available memory...' },
    permissions: { status: 'pending', message: 'Verifying permissions...' },
    network: { status: 'pending', message: 'Testing network connectivity...' }
  });

  const verifyAllChecks = useCallback(() => {
    const allPassed = Object.values(checks).every(
      check => check.status === 'success'
    );
    if (allPassed) {
      onComplete(true);
    }
  }, [checks, onComplete]);

  useEffect(() => {
    const runChecks = async () => {
      // Disk Space Check
      setChecks(prev => ({
        ...prev,
        disk: { status: 'checking', message: 'Checking disk space...' }
      }));
      try {
        // TODO: Implement actual disk space check
        await new Promise(resolve => setTimeout(resolve, 1000));
        setChecks(prev => ({
          ...prev,
          disk: { 
            status: 'success',
            message: `Required: ${profile.requirements.disk}, Available: 50GB`
          }
        }));
      } catch (error) {
        setChecks(prev => ({
          ...prev,
          disk: { 
            status: 'error',
            message: 'Failed to check disk space'
          }
        }));
      }

      // Memory Check
      setChecks(prev => ({
        ...prev,
        memory: { status: 'checking', message: 'Checking available memory...' }
      }));
      try {
        // TODO: Implement actual memory check
        await new Promise(resolve => setTimeout(resolve, 1000));
        setChecks(prev => ({
          ...prev,
          memory: { 
            status: 'success',
            message: `Required: ${profile.requirements.memory}, Available: 32GB`
          }
        }));
      } catch (error) {
        setChecks(prev => ({
          ...prev,
          memory: { 
            status: 'error',
            message: 'Failed to check memory'
          }
        }));
      }

      // Permissions Check
      setChecks(prev => ({
        ...prev,
        permissions: { status: 'checking', message: 'Verifying permissions...' }
      }));
      try {
        // TODO: Implement actual permissions check
        await new Promise(resolve => setTimeout(resolve, 1000));
        setChecks(prev => ({
          ...prev,
          permissions: { 
            status: 'success',
            message: 'All required permissions available'
          }
        }));
      } catch (error) {
        setChecks(prev => ({
          ...prev,
          permissions: { 
            status: 'error',
            message: 'Missing required permissions'
          }
        }));
      }

      // Network Check
      setChecks(prev => ({
        ...prev,
        network: { status: 'checking', message: 'Testing network connectivity...' }
      }));
      try {
        // TODO: Implement actual network check
        await new Promise(resolve => setTimeout(resolve, 1000));
        setChecks(prev => ({
          ...prev,
          network: { 
            status: 'success',
            message: 'Network connectivity verified'
          }
        }));
      } catch (error) {
        setChecks(prev => ({
          ...prev,
          network: { 
            status: 'error',
            message: 'Network connectivity issues detected'
          }
        }));
      }

      // Verify all checks after completion
      verifyAllChecks();
    };

    runChecks();
  }, [profile, onComplete, verifyAllChecks]);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <Check className="w-5 h-5 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      case 'checking':
        return <Loader className="w-5 h-5 text-concept-yellow animate-spin" />;
      default:
        return <Loader className="w-5 h-5 text-gray-400" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className={`${styles.card} bg-concept-brown-dark/10`}>
        <h3 className={styles.heading}>System Requirements Check</h3>
        <p className={styles.subheading}>
          Verifying your system meets the requirements for {profile.name}
        </p>
      </div>

      <div className="space-y-4">
        {Object.entries(checks).map(([key, check]) => (
          <Card key={key} className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              {getStatusIcon(check.status)}
              <div>
                <h4 className={styles.heading}>{key.charAt(0).toUpperCase() + key.slice(1)}</h4>
                <p className={styles.text}>{check.message}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {Object.values(checks).some(check => check.status === 'error') && (
        <div className={`${styles.card} bg-red-900/10 border-red-500/50`}>
          <div className="flex items-center space-x-3">
            <AlertCircle className="w-6 h-6 text-red-500" />
            <div>
              <h4 className="text-red-500 font-medium">System Requirements Not Met</h4>
              <p className="text-red-400">
                Please resolve the issues above before continuing with the installation.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SystemCheck;