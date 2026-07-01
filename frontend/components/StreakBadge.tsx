import { View, Text, StyleSheet } from 'react-native';
import { DUO } from '@/constants/duo';

interface StreakBadgeProps {
  count: number;
  size?: 'small' | 'large';
}

export default function StreakBadge({ count, size = 'small' }: StreakBadgeProps) {
  const isLarge = size === 'large';
  return (
    <View style={[styles.badge, isLarge && styles.badgeLarge]}>
      <Text style={[styles.flame, isLarge && styles.flameLarge]}>
        {count > 0 ? '\uD83D\uDD25' : '\u2744\uFE0F'}
      </Text>
      <Text style={[styles.count, isLarge && styles.countLarge]}>{count}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: DUO.orange + '25',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: DUO.radiusFull,
    gap: 4,
    borderWidth: 1,
    borderColor: DUO.orange + '40',
  },
  badgeLarge: {
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  flame: {
    fontSize: 16,
  },
  flameLarge: {
    fontSize: 28,
  },
  count: {
    fontSize: 14,
    fontWeight: '800',
    color: DUO.orange,
  },
  countLarge: {
    fontSize: 24,
  },
});
