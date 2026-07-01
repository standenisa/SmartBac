import { Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { DUO } from '@/constants/duo';
import AnimatedPressable from '@/components/AnimatedPressable';

interface DuoButtonProps {
  title: string;
  onPress: () => void;
  color?: string;
  darkColor?: string;
  textColor?: string;
  disabled?: boolean;
  size?: 'small' | 'medium' | 'large';
  style?: ViewStyle;
  textStyle?: TextStyle;
  glow?: boolean;
}

export default function DuoButton({
  title,
  onPress,
  color = DUO.green,
  darkColor,
  textColor = DUO.white,
  disabled = false,
  size = 'large',
  style,
  textStyle,
  glow = false,
}: DuoButtonProps) {
  const dark = darkColor || darken(color);
  const padV = size === 'small' ? 10 : size === 'medium' ? 14 : 16;
  const padH = size === 'small' ? 20 : size === 'medium' ? 28 : 32;
  const fontSize = size === 'small' ? 14 : size === 'medium' ? 16 : 18;

  return (
    <AnimatedPressable
      onPress={onPress}
      disabled={disabled}
      style={[
        styles.button,
        {
          backgroundColor: disabled ? DUO.surface : color,
          borderBottomColor: disabled ? DUO.textMuted : dark,
          paddingVertical: padV,
          paddingHorizontal: padH,
        },
        glow && !disabled && {
          shadowColor: color,
          shadowOffset: { width: 0, height: 4 },
          shadowOpacity: 0.4,
          shadowRadius: 12,
          elevation: 8,
        },
        style,
      ] as ViewStyle[]}
    >
      <Text
        style={[
          styles.text,
          {
            color: disabled ? DUO.textMuted : textColor,
            fontSize,
          },
          textStyle,
        ]}
      >
        {title}
      </Text>
    </AnimatedPressable>
  );
}

function darken(hex: string): string {
  const num = parseInt(hex.replace('#', ''), 16);
  const r = Math.max(0, ((num >> 16) & 0xFF) - 30);
  const g = Math.max(0, ((num >> 8) & 0xFF) - 30);
  const b = Math.max(0, (num & 0xFF) - 30);
  return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, '0')}`;
}

const styles = StyleSheet.create({
  button: {
    borderRadius: DUO.radius,
    borderBottomWidth: DUO.borderBottom,
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontWeight: '800',
    letterSpacing: 0.5,
    textTransform: 'uppercase',
  },
});
