import { View, Text, StyleSheet } from 'react-native';
import Animated, { useAnimatedStyle, withTiming, runOnJS, useSharedValue, SlideInUp, SlideOutUp } from 'react-native-reanimated';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import { DUO } from '@/constants/duo';

export type ToastType = 'success' | 'error' | 'achievement' | 'streak' | 'levelup';

export interface ToastData {
  type: ToastType;
  title: string;
  subtitle?: string;
}

const TOAST_CONFIG: Record<ToastType, { color: string; emoji: string }> = {
  success: { color: DUO.green, emoji: '✅' },
  error: { color: DUO.red, emoji: '❌' },
  achievement: { color: DUO.purple, emoji: '🏆' },
  streak: { color: DUO.orange, emoji: '🔥' },
  levelup: { color: DUO.yellow, emoji: '⭐' },
};

interface ToastProps {
  data: ToastData;
  onDismiss: () => void;
}

export default function Toast({ data, onDismiss }: ToastProps) {
  const cfg = TOAST_CONFIG[data.type];
  const translateY = useSharedValue(0);

  const swipe = Gesture.Pan()
    .onUpdate((e) => { if (e.translationY < 0) translateY.value = e.translationY; })
    .onEnd((e) => {
      if (e.translationY < -50) {
        translateY.value = withTiming(-200, { duration: 200 }, () => runOnJS(onDismiss)());
      } else {
        translateY.value = withTiming(0, { duration: 200 });
      }
    });

  const animStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }],
  }));

  return (
    <GestureDetector gesture={swipe}>
      <Animated.View
        entering={SlideInUp.duration(300)}
        exiting={SlideOutUp.duration(200)}
        style={[styles.container, { borderLeftColor: cfg.color }, animStyle]}
      >
        <Text style={styles.emoji}>{cfg.emoji}</Text>
        <View style={styles.textContainer}>
          <Text style={styles.title}>{data.title}</Text>
          {data.subtitle && <Text style={styles.subtitle}>{data.subtitle}</Text>}
        </View>
      </Animated.View>
    </GestureDetector>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 60,
    left: 16,
    right: 16,
    backgroundColor: DUO.card,
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    borderLeftWidth: 4,
    borderWidth: 1,
    borderColor: DUO.surface,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 12,
    zIndex: 9999,
  },
  emoji: { fontSize: 24, marginRight: 12 },
  textContainer: { flex: 1 },
  title: { fontSize: 15, fontWeight: '800', color: DUO.textPrimary },
  subtitle: { fontSize: 12, fontWeight: '600', color: DUO.textSecondary, marginTop: 2 },
});
