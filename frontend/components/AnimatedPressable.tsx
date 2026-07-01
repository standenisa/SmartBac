import { ReactNode } from 'react';
import { Pressable, StyleProp, ViewStyle } from 'react-native';
import Animated, { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';

const AnimatedPressableView = Animated.createAnimatedComponent(Pressable);

interface AnimatedPressableProps {
  onPress: () => void;
  children: ReactNode;
  style?: StyleProp<ViewStyle>;
  disabled?: boolean;
  scale?: number;
}

export default function AnimatedPressable({
  onPress,
  children,
  style,
  disabled = false,
  scale = 0.95,
}: AnimatedPressableProps) {
  const pressed = useSharedValue(1);

  const animStyle = useAnimatedStyle(() => ({
    transform: [{ scale: pressed.value }],
  }));

  return (
    <AnimatedPressableView
      onPress={onPress}
      onPressIn={() => { pressed.value = withSpring(scale, { damping: 15, stiffness: 300 }); }}
      onPressOut={() => { pressed.value = withSpring(1, { damping: 10, stiffness: 200 }); }}
      disabled={disabled}
      style={[animStyle, style]}
    >
      {children}
    </AnimatedPressableView>
  );
}
