import { useEffect } from 'react';
import { Text, StyleSheet } from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSequence,
  runOnJS,
} from 'react-native-reanimated';
import { DUO } from '@/constants/duo';

interface XPPopupProps {
  xp: number;
  visible: boolean;
  onDone?: () => void;
}

export default function XPPopup({ xp, visible, onDone }: XPPopupProps) {
  const translateY = useSharedValue(0);
  const opacity = useSharedValue(0);
  const scale = useSharedValue(0.5);

  useEffect(() => {
    if (visible) {
      translateY.value = 0;
      opacity.value = 0;
      scale.value = 0.5;

      opacity.value = withSequence(
        withTiming(1, { duration: 200 }),
        withTiming(1, { duration: 800 }),
        withTiming(0, { duration: 400 }, () => {
          if (onDone) runOnJS(onDone)();
        })
      );
      translateY.value = withTiming(-80, { duration: 1400 });
      scale.value = withSequence(
        withTiming(1.3, { duration: 200 }),
        withTiming(1, { duration: 200 })
      );
    }
  }, [visible]);

  const animStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }, { scale: scale.value }],
    opacity: opacity.value,
  }));

  if (!visible) return null;

  return (
    <Animated.View style={[styles.container, animStyle]}>
      <Text style={styles.text}>+{xp} XP</Text>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    alignSelf: 'center',
    top: '40%',
    backgroundColor: DUO.yellow,
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: DUO.radiusFull,
    borderBottomWidth: 3,
    borderBottomColor: DUO.yellowDark,
    zIndex: 999,
    shadowColor: DUO.yellow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.5,
    shadowRadius: 16,
    elevation: 10,
  },
  text: {
    fontSize: 24,
    fontWeight: '900',
    color: '#1B1B2F',
  },
});
