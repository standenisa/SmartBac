import { useEffect } from 'react';
import { View, StyleSheet, ViewStyle } from 'react-native';
import Animated, { useSharedValue, useAnimatedStyle, withRepeat, withTiming, interpolateColor } from 'react-native-reanimated';
import { DUO } from '@/constants/duo';

interface SkeletonBoxProps {
  width?: number | string;
  height?: number;
  borderRadius?: number;
  style?: ViewStyle;
}

function SkeletonBox({ width = '100%', height = 20, borderRadius = 8, style }: SkeletonBoxProps) {
  const pulse = useSharedValue(0);

  useEffect(() => {
    pulse.value = withRepeat(withTiming(1, { duration: 1000 }), -1, true);
  }, []);

  const animStyle = useAnimatedStyle(() => ({
    backgroundColor: interpolateColor(pulse.value, [0, 1], [DUO.surface, DUO.surfaceLight]),
  }));

  return <Animated.View style={[{ width: width as any, height, borderRadius }, animStyle, style]} />;
}

export function ExerciseCardSkeleton() {
  return (
    <View style={styles.exerciseCard}>
      <View style={styles.badgeRow}>
        <SkeletonBox width={80} height={24} borderRadius={12} />
        <SkeletonBox width={60} height={24} borderRadius={12} />
      </View>
      <SkeletonBox height={20} style={{ marginBottom: 8 }} />
      <SkeletonBox height={20} width="80%" style={{ marginBottom: 16 }} />
      <SkeletonBox height={50} borderRadius={16} />
    </View>
  );
}

export function StatsCardSkeleton() {
  return (
    <View style={styles.statsRow}>
      {[1, 2, 3].map(i => (
        <View key={i} style={styles.statCard}>
          <SkeletonBox width={50} height={28} borderRadius={6} style={{ marginBottom: 6 }} />
          <SkeletonBox width={60} height={12} borderRadius={4} />
        </View>
      ))}
    </View>
  );
}

export function LeaderboardSkeleton() {
  return (
    <View>
      {[1, 2, 3, 4, 5].map(i => (
        <View key={i} style={styles.leaderRow}>
          <SkeletonBox width={24} height={24} borderRadius={12} />
          <SkeletonBox width={32} height={32} borderRadius={16} style={{ marginLeft: 12 }} />
          <View style={{ flex: 1, marginLeft: 12 }}>
            <SkeletonBox height={14} width="60%" style={{ marginBottom: 4 }} />
            <SkeletonBox height={10} width="30%" />
          </View>
          <SkeletonBox width={50} height={20} borderRadius={10} />
        </View>
      ))}
    </View>
  );
}

export function AchievementGridSkeleton() {
  return (
    <View style={styles.achieveGrid}>
      {[1, 2, 3, 4, 5, 6].map(i => (
        <View key={i} style={styles.achieveCard}>
          <SkeletonBox width={40} height={40} borderRadius={20} style={{ marginBottom: 8 }} />
          <SkeletonBox width={60} height={10} borderRadius={4} />
        </View>
      ))}
    </View>
  );
}

export default SkeletonBox;

const styles = StyleSheet.create({
  exerciseCard: { backgroundColor: DUO.card, margin: 20, padding: 20, borderRadius: 20, borderWidth: 1, borderColor: DUO.surface },
  badgeRow: { flexDirection: 'row', gap: 8, marginBottom: 16 },
  statsRow: { flexDirection: 'row', paddingHorizontal: 20, gap: 10 },
  statCard: { flex: 1, backgroundColor: DUO.card, paddingVertical: 16, borderRadius: 16, alignItems: 'center', borderWidth: 1, borderColor: DUO.surface },
  leaderRow: { flexDirection: 'row', alignItems: 'center', paddingVertical: 12, paddingHorizontal: 16, borderBottomWidth: 1, borderBottomColor: DUO.surface },
  achieveGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  achieveCard: { width: '30%', backgroundColor: DUO.card, padding: 16, borderRadius: 16, alignItems: 'center', borderWidth: 1, borderColor: DUO.surface, aspectRatio: 1 },
});
