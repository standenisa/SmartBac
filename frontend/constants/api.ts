import { Platform } from 'react-native';
import Constants from 'expo-constants';

const getBaseUrl = () => {
  // Pe web → localhost direct
  if (Platform.OS === 'web') {
    return 'http://localhost:5001';
  }

  // IP-ul Mac-ului în rețeaua locală (actualizează dacă schimbi WiFi-ul)
  const LAN_IP = '192.168.0.185';

  // Pe telefon → IP-ul Mac-ului din hostUri
  const debuggerHost = Constants.expoConfig?.hostUri?.split(':')[0];
  // Cu --tunnel, hostUri e o adresă .exp.direct (nu poate atinge backend-ul local)
  // → folosim IP-ul LAN. Telefonul trebuie să fie pe ACELAȘI WiFi.
  if (debuggerHost && !debuggerHost.includes('exp.direct') && !debuggerHost.includes('exp.host')) {
    return `http://${debuggerHost}:5001`;
  }

  return `http://${LAN_IP}:5001`;
};

export const API_BASE_URL = getBaseUrl();
