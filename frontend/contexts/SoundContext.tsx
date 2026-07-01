import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface SoundSettings {
  soundEnabled: boolean;
  hapticsEnabled: boolean;
}

interface SoundContextValue {
  settings: SoundSettings;
  toggleSound: () => void;
  toggleHaptics: () => void;
}

const SoundContext = createContext<SoundContextValue>({
  settings: { soundEnabled: true, hapticsEnabled: true },
  toggleSound: () => {},
  toggleHaptics: () => {},
});

export function useSettings() {
  return useContext(SoundContext);
}

export function SoundProvider({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<SoundSettings>({
    soundEnabled: true,
    hapticsEnabled: true,
  });

  useEffect(() => {
    AsyncStorage.getItem('soundSettings').then((stored) => {
      if (stored) setSettings(JSON.parse(stored));
    });
  }, []);

  const save = (newSettings: SoundSettings) => {
    setSettings(newSettings);
    AsyncStorage.setItem('soundSettings', JSON.stringify(newSettings));
  };

  const toggleSound = () => save({ ...settings, soundEnabled: !settings.soundEnabled });
  const toggleHaptics = () => save({ ...settings, hapticsEnabled: !settings.hapticsEnabled });

  return (
    <SoundContext.Provider value={{ settings, toggleSound, toggleHaptics }}>
      {children}
    </SoundContext.Provider>
  );
}
