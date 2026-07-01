import { useEffect } from 'react';
import { StyleSheet, View } from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withDelay,
} from 'react-native-reanimated';
import { DUO } from '@/constants/duo';

const CONFETTI_COLORS = [DUO.green, DUO.blue, DUO.red, DUO.orange, DUO.yellow, DUO.purple];
const PIECES = 24;

interface ConfettiProps {
  visible: boolean;
}

function ConfettiPiece({ index }: { index: number }) {
  const translateY = useSharedValue(-20);
  const translateX = useSharedValue(0);
  const opacity = useSharedValue(0);
  const rotate = useSharedValue(0);

  useEffect(() => {
    const startX = (Math.random() - 0.5) * 350;
    const endY = 600 + Math.random() * 200;
    const delay = Math.random() * 400;

    translateX.value = startX;

    opacity.value = withDelay(delay, withTiming(1, { duration: 100 }));
    translateY.value = withDelay(delay, withTiming(endY, { duration: 2000 + Math.random() * 1000 }));
    rotate.value = withDelay(delay, withTiming(360 * (Math.random() > 0.5 ? 1 : -1) * 3, { duration: 2500 }));

    // Fade out
    opacity.value = withDelay(delay + 1500, withTiming(0, { duration: 500 }));
  }, []);

  const style = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
      { rotate: `${rotate.value}deg` },
    ],
    opacity: opacity.value,
  }));

  const color = CONFETTI_COLORS[index % CONFETTI_COLORS.length];
  const isSquare = index % 3 === 0;

  return (
    <Animated.View
      style={[
        styles.piece,
        {
          backgroundColor: color,
          borderRadius: isSquare ? 2 : 6,
          width: isSquare ? 10 : 8,
          height: isSquare ? 10 : 12,
        },
        style,
      ]}
    />
  );
}

export default function ConfettiAnimation({ visible }: ConfettiProps) {
  if (!visible) return null;

  return (
    <View style={styles.container} pointerEvents="none">
      {Array.from({ length: PIECES }).map((_, i) => (
        <ConfettiPiece key={i} index={i} />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFillObject,
    alignItems: 'center',
    zIndex: 1000,
  },
  piece: {
    position: 'absolute',
    top: 0,
  },
});
