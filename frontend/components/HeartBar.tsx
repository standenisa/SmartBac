import { View, Text, StyleSheet } from 'react-native';

interface HeartBarProps {
  hearts: number;
  maxHearts?: number;
}

export default function HeartBar({ hearts, maxHearts = 3 }: HeartBarProps) {
  return (
    <View style={styles.container}>
      {Array.from({ length: maxHearts }).map((_, i) => (
        <Text key={i} style={[styles.heart, i >= hearts && styles.heartEmpty]}>
          {i < hearts ? '\u2764\uFE0F' : '\uD83E\uDD0D'}
        </Text>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 2,
  },
  heart: {
    fontSize: 18,
  },
  heartEmpty: {
    opacity: 0.3,
  },
});
