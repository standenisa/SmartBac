import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, ScrollView, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { apiGet } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import { LeaderboardSkeleton } from '@/components/Skeleton';
import ErrorState from '@/components/ErrorState';

const { width } = Dimensions.get('window');

interface LeaderboardEntry {
  rank: number;
  user_id: number;
  username: string;
  weekly_xp: number;
  zone: 'promotion' | 'safe' | 'demotion';
}

interface TierInfo {
  name: string;
  color: string;
  emoji: string;
}

export default function LeaguesScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const [league, setLeague] = useState('Bronz');
  const [tier, setTier] = useState<TierInfo>({ name: 'Bronz', color: '#CD7F32', emoji: '🥉' });
  const [weeklyXP, setWeeklyXP] = useState(0);
  const [rank, setRank] = useState(0);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [weekReset, setWeekReset] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => { fetchLeague(); }, []);

  const fetchLeague = async () => {
    try {
      setError(false);
      const data = await apiGet<any>(`/api/leagues?user_id=${user?.id}`);
      if (data.success) {
        setLeague(data.league);
        setTier(data.tier);
        setWeeklyXP(data.weekly_xp);
        setRank(data.rank);
        setLeaderboard(data.leaderboard);
        setWeekReset(data.week_reset);
      }
    } catch { setError(true); }
    setLoading(false);
  };

  const getCountdown = () => {
    if (!weekReset) return '…';
    const diff = new Date(weekReset).getTime() - Date.now();
    if (diff <= 0) return 'Reset iminent!';
    const days = Math.floor(diff / 86400000);
    const hours = Math.floor((diff % 86400000) / 3600000);
    return `${days}z ${hours}h`;
  };

  if (error) return <ErrorState preset="network" onRetry={() => { setLoading(true); fetchLeague(); }} />;

  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <LinearGradient
          colors={[tier.color + '30', DUO.bg]}
          style={[styles.header, { paddingTop: insets.top + 12 }]}
        >
          <Text style={styles.headerEmoji}>{tier.emoji}</Text>
          <Text style={[styles.headerTitle, { color: tier.color }]}>Liga {league}</Text>
          <Text style={styles.headerSubtitle}>Saptamana se reseteaza in {getCountdown()}</Text>
        </LinearGradient>

        {loading ? (
          <View style={{ padding: 20 }}><LeaderboardSkeleton /></View>
        ) : (
          <>
            {/* User Stats */}
            <View style={styles.statsRow}>
              <View style={[styles.statCard, { borderColor: tier.color + '40' }]}>
                <Text style={[styles.statValue, { color: tier.color }]}>#{rank}</Text>
                <Text style={styles.statLabel}>Locul tau</Text>
              </View>
              <View style={[styles.statCard, { borderColor: DUO.yellow + '40' }]}>
                <Text style={[styles.statValue, { color: DUO.yellow }]}>{weeklyXP}</Text>
                <Text style={styles.statLabel}>XP saptamana</Text>
              </View>
            </View>

            {/* Podium Top 3 */}
            {leaderboard.length >= 3 && (
              <View style={styles.podium}>
                {[1, 0, 2].map((idx) => {
                  const entry = leaderboard[idx];
                  if (!entry) return null;
                  const isFirst = idx === 0;
                  const medals = ['🥇', '🥈', '🥉'];
                  return (
                    <View key={idx} style={[styles.podiumItem, isFirst && styles.podiumFirst]}>
                      <Text style={styles.podiumMedal}>{medals[idx]}</Text>
                      <View style={[
                        styles.podiumAvatar,
                        { height: isFirst ? 56 : 44, width: isFirst ? 56 : 44, borderColor: tier.color },
                      ]}>
                        <Text style={styles.podiumInitial}>{entry.username[0]?.toUpperCase()}</Text>
                      </View>
                      <Text style={styles.podiumName} numberOfLines={1}>{entry.username}</Text>
                      <Text style={styles.podiumXP}>{entry.weekly_xp} XP</Text>
                    </View>
                  );
                })}
              </View>
            )}

            {/* Full Leaderboard */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Clasament</Text>
              {leaderboard.map((entry) => {
                const isUser = entry.user_id === user?.id;
                const zoneColor = entry.zone === 'promotion' ? DUO.green : entry.zone === 'demotion' ? DUO.red : 'transparent';
                return (
                  <View key={entry.rank} style={[
                    styles.leaderRow,
                    isUser && styles.leaderRowHighlight,
                    { borderLeftColor: zoneColor, borderLeftWidth: entry.zone !== 'safe' ? 3 : 0 },
                  ]}>
                    <Text style={[styles.leaderRank, isUser && { color: tier.color }]}>
                      {entry.rank}
                    </Text>
                    <View style={styles.leaderAvatar}>
                      <Text style={styles.leaderAvatarText}>{entry.username[0]?.toUpperCase()}</Text>
                    </View>
                    <View style={styles.leaderInfo}>
                      <Text style={[styles.leaderName, isUser && { color: tier.color, fontWeight: '800' }]}>
                        {entry.username} {isUser ? '(Tu)' : ''}
                      </Text>
                    </View>
                    <Text style={[styles.leaderXP, isUser && { color: tier.color }]}>
                      {entry.weekly_xp} XP
                    </Text>
                  </View>
                );
              })}
            </View>

            {/* Legend */}
            <View style={styles.legend}>
              <View style={styles.legendItem}>
                <View style={[styles.legendDot, { backgroundColor: DUO.green }]} />
                <Text style={styles.legendText}>Zona promovare</Text>
              </View>
              <View style={styles.legendItem}>
                <View style={[styles.legendDot, { backgroundColor: DUO.red }]} />
                <Text style={styles.legendText}>Zona retrogradare</Text>
              </View>
            </View>
          </>
        )}

        <View style={{ height: 100 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  header: { paddingBottom: 24, paddingHorizontal: 20, alignItems: 'center', borderBottomWidth: 1, borderBottomColor: DUO.surface },
  headerEmoji: { fontSize: 56, marginBottom: 8 },
  headerTitle: { fontSize: 28, fontWeight: '800', marginBottom: 4 },
  headerSubtitle: { fontSize: 13, color: DUO.textSecondary, fontWeight: '600' },
  statsRow: { flexDirection: 'row', paddingHorizontal: 20, gap: 10, marginTop: 16 },
  statCard: { flex: 1, backgroundColor: DUO.card, paddingVertical: 16, borderRadius: 16, alignItems: 'center', borderWidth: 1 },
  statValue: { fontSize: 28, fontWeight: '800' },
  statLabel: { fontSize: 11, color: DUO.textMuted, fontWeight: '700', marginTop: 2 },
  podium: { flexDirection: 'row', justifyContent: 'center', alignItems: 'flex-end', paddingVertical: 24, gap: 12 },
  podiumItem: { alignItems: 'center', width: (width - 80) / 3 },
  podiumFirst: { marginBottom: 16 },
  podiumMedal: { fontSize: 24, marginBottom: 4 },
  podiumAvatar: { borderRadius: 28, backgroundColor: DUO.card, borderWidth: 2, justifyContent: 'center', alignItems: 'center', marginBottom: 6 },
  podiumInitial: { fontSize: 18, fontWeight: '800', color: DUO.textPrimary },
  podiumName: { fontSize: 12, fontWeight: '700', color: DUO.textPrimary, textAlign: 'center' },
  podiumXP: { fontSize: 11, fontWeight: '700', color: DUO.textMuted },
  section: { padding: 20 },
  sectionTitle: { fontSize: 18, fontWeight: '800', color: DUO.textPrimary, marginBottom: 14 },
  leaderRow: { flexDirection: 'row', alignItems: 'center', backgroundColor: DUO.card, padding: 12, borderRadius: 12, marginBottom: 6, borderWidth: 1, borderColor: DUO.surface },
  leaderRowHighlight: { borderColor: DUO.yellow + '40' },
  leaderRank: { width: 28, fontSize: 16, fontWeight: '800', color: DUO.textMuted, textAlign: 'center' },
  leaderAvatar: { width: 36, height: 36, borderRadius: 18, backgroundColor: DUO.surface, justifyContent: 'center', alignItems: 'center', marginHorizontal: 10 },
  leaderAvatarText: { fontSize: 14, fontWeight: '800', color: DUO.textPrimary },
  leaderInfo: { flex: 1 },
  leaderName: { fontSize: 14, fontWeight: '700', color: DUO.textPrimary },
  leaderXP: { fontSize: 14, fontWeight: '800', color: DUO.yellow },
  legend: { flexDirection: 'row', justifyContent: 'center', gap: 20, paddingVertical: 8 },
  legendItem: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  legendDot: { width: 8, height: 8, borderRadius: 4 },
  legendText: { fontSize: 11, color: DUO.textMuted, fontWeight: '600' },
});
