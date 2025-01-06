import React, { useState, useEffect } from 'react';
import { 
  CheckCircle2, 
  AlertTriangle, 
  XCircle,
  Loader,
  RefreshCw
} from 'lucide-react';
import { useTheme } from '../../../shared/contexts';
import { Button, Card } from '../../../shared/components';

const ValidationCheck = ({ profile, securityConfig, integrations, onComplete }) => {
  const { styles } = useTheme();
  const [validationState, setValidationState] = useState({
    status: 'pending',
    checks: {
      system: { status: 'pending', details: [] },
      security: { status: 'pending', details: [] },
      integrations: { status: 'pending', details: [] },
      performance: { status: 'pending', details: [] }
    }
  });

  const runValidation = async () => {
    setValidationState(prev => ({
      ...prev,
      status: 'running',
      checks: Object.keys(prev.checks).reduce((acc, key) => ({
        ...acc,
        [key]: { status: 'pending', details: [] }
      }), {})
    }));

    // System Validation
    await validateSystem();
    // Security Validation
    await validateSecurity();
    // Integration Validation
    await validateIntegrations();
    // Performance Validation
    await validatePerformance();

    // Check overall status
    const allChecks = Object.values(validationState.checks);
    const hasErrors = allChecks.some(check => check.status === 'error');
    const hasWarnings = allChecks.some(check => check.status === 'warning');
    
    setValidationState(prev => ({
      ...prev,
      status: hasErrors ? 'error' : hasWarnings ? 'warning' : 'success'
    }));

    if (!hasErrors) {
      onComplete(true);
    }
  };

  const validateSystem = async () => {
    setValidationState(prev => ({
      ...prev,
      checks: {
        ...prev.checks,
        system: { status: 'running', details: [] }
      }
    }));

    try {
      // Simulated system checks
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setValidationState(prev => ({
        ...prev,
        checks: {
          ...prev.checks,
          system: {
            status: 'success',
            details: [
              'System requirements met',
              'Sufficient disk space available',
              'Memory allocation verified'
            ]
          }
        }
      }));
    } catch (error) {
      setValidationState(prev => ({
        ...prev,
        checks: {
          ...prev.checks,
          system: {
            status: 'error',
            details: ['Failed to validate system requirements']
          }
        }
      }));
    }
  };

  const validateSecurity = async () => {
    setValidationState(prev => ({
      ...prev,
      checks: {
        ...prev.checks,
        security: { status: 'running', details: [] }
      }
    }));

    try {
      // Simulated security checks
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const details = [];
      let status = 'success';

      // Check encryption
      if (securityConfig.encryption.enabled) {
        details.push('Encryption properly configured');
      } else {
        details.push('Warning: Encryption not enabled');
        status = 'warning';
      }

      // Check authentication
      if (securityConfig.authentication.mfa) {
        details.push('MFA enabled');
      } else if (profile.id === 'enterprise') {
        details.push('Warning: MFA recommended for enterprise setup');
        status = 'warning';
      }

      setValidationState(prev => ({
        ...prev,
        checks: {
          ...prev.checks,
          security: { status, details }
        }
      }));
    } catch (error) {
      setValidationState(prev => ({
        ...prev,
        checks: {
          ...prev.checks,
          security: {
            status: 'error',
            details: ['Failed to validate security configuration']
          }
        }
      }));
    }
  };

  const validateIntegrations = async () => {
    setValidationState(prev => ({
      ...prev,
      checks: {
        ...prev.checks,
        integrations: { status: 'running', details: [] }
      }
    }));

    try {
      // Simulated integration checks
      await new Promise(resolve => setTimeout(resolve, 1200));
      
      const details = [];
      let status = 'success';

      // Check each integration
      Object.entries(integrations).forEach(([name, config]) => {
        if (config.configured) {
          details.push(`${name} integration verified`);
        } else {
          details.push(`Warning: ${name} integration not configured`);
          status = 'warning';
        }
      });

      setValidationState(prev => ({
        ...prev,
        checks: {
          ...prev.checks,
          integrations: { status, details }
        }
      }));
    } catch (error) {
      setValidationState(prev => ({
        ...prev,
        checks: {
          ...prev.checks,
          integrations: {
            status: 'error',
            details: ['Failed to validate integrations']
          }
        }
      }));
    }
  };

  const validatePerformance = async () => {
    setValidationState(prev => ({
      ...prev,
      checks: {
        ...prev.checks,
        performance: { status: 'running', details: [] }
      }
    }));

    try {
      // Simulated performance checks
      await new Promise(resolve => setTimeout(resolve, 800));
      
      setValidationState(prev => ({
        ...prev,
        checks: {
          ...prev.checks,
          performance: {
            status: 'success',
            details: [
              'Memory allocation optimized',
              'Cache configuration verified',
              'Network latency within acceptable range'
            ]
          }
        }
      }));
    } catch (error) {
      setValidationState(prev => ({
        ...prev,
        checks: {
          ...prev.checks,
          performance: {
            status: 'error',
            details: ['Failed to validate performance metrics']
          }
        }
      }));
    }
  };

  useEffect(() => {
    runValidation();
  }, []);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'running':
        return <Loader className="w-5 h-5 text-concept-yellow animate-spin" />;
      default:
        return <Loader className="w-5 h-5 text-gray-400" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className={`${styles.card} bg-concept-brown-dark/10`}>
        <h3 className={styles.heading}>Configuration Validation</h3>
        <p className={styles.subheading}>
          Verifying all components are properly configured
        </p>
      </div>

      <div className="space-y-4">
        {Object.entries(validationState.checks).map(([key, check]) => (
          <Card key={key}>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {getStatusIcon(check.status)}
                <div>
                  <h4 className={styles.heading}>
                    {key.charAt(0).toUpperCase() + key.slice(1)} Validation
                  </h4>
                  <div className="space-y-1 mt-2">
                    {check.details.map((detail, index) => (
                      <p 
                        key={index} 
                        className={`text-sm ${
                          detail.toLowerCase().includes('warning')
                            ? 'text-yellow-500'
                            : styles.text
                        }`}
                      >
                        {detail}
                      </p>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {validationState.status !== 'running' && (
        <div className="flex justify-between items-center">
          <Button
            variant="secondary"
            onClick={runValidation}
            icon={RefreshCw}
          >
            Run Validation Again
          </Button>

          {validationState.status === 'success' && (
            <Button
              variant="primary"
              onClick={() => onComplete(true)}
            >
              Continue
            </Button>
          )}
        </div>
      )}

      {validationState.status === 'error' && (
        <div className={`${styles.card} bg-red-900/10 border-red-500/50`}>
          <div className="flex items-center space-x-3">
            <XCircle className="w-6 h-6 text-red-500" />
            <div>
              <h4 className="text-red-500 font-medium">Validation Failed</h4>
              <p className="text-red-400">
                Please resolve the issues above before continuing.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ValidationCheck;