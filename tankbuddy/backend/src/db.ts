import fs from 'fs';
import path from 'path';

const DATA_FILE = path.join(__dirname, '..', 'data.json');

export interface TankData {
  settings: {
    deviceName: string;
    tunnelUrl: string;
    feedSchedule: string[];
  };
  activityLogs: Array<{
    timestamp: number;
    activityScore: number;
  }>;
  feedHistory: Array<{
    timestamp: number;
    amount: string;
  }>;
}

const defaultData: TankData = {
  settings: {
    deviceName: 'TankBuddy Hub',
    tunnelUrl: '',
    feedSchedule: []
  },
  activityLogs: [],
  feedHistory: []
};

// Initialize DB
export function initDB() {
  if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(defaultData, null, 2));
  }
}

// Read DB
export function readDB(): TankData {
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf-8');
    return JSON.parse(raw);
  } catch (error) {
    console.error('Error reading DB:', error);
    return defaultData;
  }
}

// Write DB
export function writeDB(data: TankData) {
  try {
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
  } catch (error) {
    console.error('Error writing DB:', error);
  }
}

// Update specific setting
export function updateSetting<K extends keyof TankData['settings']>(key: K, value: TankData['settings'][K]) {
  const data = readDB();
  data.settings[key] = value;
  writeDB(data);
}

// Log activity
export function logActivity(score: number) {
  const data = readDB();
  data.activityLogs.push({ timestamp: Date.now(), activityScore: score });

  // Keep only last 1000 logs to save space
  if (data.activityLogs.length > 1000) {
    data.activityLogs = data.activityLogs.slice(-1000);
  }

  writeDB(data);
}

// Log feed
export function logFeed(amount: string) {
  const data = readDB();
  data.feedHistory.push({ timestamp: Date.now(), amount });
  writeDB(data);
}
