import { 
  Brain,
  MessageSquare,
  Database,
  Search,
  Robot,
  Cloud,
  FolderOpen
} from 'lucide-react';

export const categories = {
  'Essential Tools': {
    icon: Brain,
    items: [
      { id: 'memory', name: 'Memory System', description: 'Knowledge graph-based persistent memory', official: true },
      { id: 'filesystem', name: 'File System', description: 'Local file access and management', official: true },
      { id: 'computer', name: 'Computer Control', description: 'Direct computer interaction capabilities', official: true }
    ]
  },
  'Communication & Collaboration': {
    icon: MessageSquare,
    items: [
      { id: 'slack', name: 'Slack', description: 'Channel management and messaging', official: true },
      { id: 'github', name: 'GitHub', description: 'Repository and issue management', official: true },
      { id: 'gitlab', name: 'GitLab', description: 'Project management and CI/CD', official: true },
      { id: 'notion', name: 'Notion', description: 'Workspace integration', community: true }
    ]
  },
  'Data & Storage': {
    icon: Database,
    items: [
      { id: 'postgres', name: 'PostgreSQL', description: 'Database integration with schema inspection', official: true },
      { id: 'sqlite', name: 'SQLite', description: 'Local database operations', official: true },
      { id: 'gdrive', name: 'Google Drive', description: 'Cloud storage integration', official: true },
      { id: 'bigquery', name: 'BigQuery', description: 'Big data querying capabilities', community: true }
    ]
  }
};