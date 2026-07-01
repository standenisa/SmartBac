import { useEffect } from 'react';
import { Text, TextStyle } from 'react-native';
import Animated, { useSharedValue, useAnimatedProps, withTiming, Easing } from 'react-native-reanimated';

const AnimatedText = Animated.createAnimatedComponent(Text);

interface AnimatedCounterProps {
  value: number;
  duration?: number;
  style?: TextStyle;
  suffix?: string;
  prefix?: string;
}

export default function AnimatedCounter({
  value,
  duration = 800,
  style,
  suffix = '',
  prefix = '',
}: AnimatedCounterProps) {
  const animValue = useSharedValue(0);

  useEffect(() => {
    animValue.value = withTiming(value, {
      duration,
      easing: Easing.out(Easing.cubic),
    });
  }, [value]);

  const animProps = useAnimatedProps(() => ({
    children: `${prefix}${Math.round(animValue.value)}${suffix}` as any,
  }));

  return <AnimatedText style={style} animatedProps={animProps} />;
}
