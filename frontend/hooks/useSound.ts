import { useCallback } from 'react';
import * as Haptics from 'expo-haptics';
import { useSettings } from '@/contexts/SoundContext';

type SoundName = 'correct' | 'wrong' | 'xp' | 'levelup';

export function useSound() {
  const { settings } = useSettings();

  // No sound files ship in assets/sounds; keep the API so call sites stay unchanged.
  const playSound = useCallback(async (_name: SoundName) => {}, []);

  const haptic = useCallback((type: 'success' | 'error' | 'light' | 'medium' = 'light') => {
    if (!settings.hapticsEnabled) return;
    switch (type) {
      case 'success':
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
        break;
      case 'error':
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
        break;
      case 'medium':
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
        break;
      default:
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
  }, [settings.hapticsEnabled]);

  return { playSound, haptic };
}
