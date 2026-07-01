import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, Modal, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { apiGet } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import ProgressRing from '@/components/ProgressRing';
import { AchievementGridSkeleton } from '@/components/Skeleton';

const { width } = Dimensions.get('window');

interface Achievement { id: string; name: string; description: string; icon: string; xp: number; unlocked: boolean; }
interface GamificationStats { xp: number; level: number; level_name: string; xp_progress: number; xp_needed: number; current_streak: number; best_streak: number; achievements_count: number; total_achievements: number; }

export default function AchievementsScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const [stats, setStats] = useState<GamificationStats | null>(null);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Achievement | null>(null);

  useEffect(() => {
    if (!user?.id) return;
    fetchData();
  }, [user?.id]);

  const fetchData = async () => {
    try {
      const [sData, aData] = await Promise.all([
        apiGet<any>(`/api/gamification/stats?user_id=${user?.id}`),
        apiGet<any>(`/api/gamification/achievements?user_id=${user?.id}`),
      ]);
      if (sData.success) setStats(sData);
      if (aData.success) setAchievements(aData.achievements || []);
    } catch (e) { console.log('Error:', e); }
    setLoading(false);
  };

  if (loading) return (
    <View style={styles.container}>
      <View style={[styles.header, { paddingTop: insets.top + 12 }]} />
      <View style={{ padding: 20 }}><AchievementGridSkeleton /></View>
    </View>
  );

  const xpProg = stats ? stats.xp_progress / stats.xp_needed : 0;
  const achieveProg = stats ? stats.achievements_count / stats.total_achievements : 0;

  return (
    <ScrollView style={styles.container}>
      {/* Detail Modal */}
      <Modal visible={selected !== null} transparent animationType="fade" onRequestClose={() => setSelected(null)}>
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setSelected(null)}>
          <View style={styles.modal}>
            {selected && (
              <>
                <Text style={styles.modalIcon}>{selected.icon}</Text>
                <Text style={styles.modalName}>{selected.name}</Text>
                <Text style={styles.modalDesc}>{selected.description}</Text>
                <View style={styles.modalXp}><Text style={styles.modalXpText}>+{selected.xp} XP ⚡</Text></View>
                <View style={[styles.modalBadge, { backgroundColor: selected.unlocked ? DUO.green + '20' : DUO.surface, borderColor: selected.unlocked ? DUO.green + '30' : DUO.surfaceLight }]}>
                  <Text style={[styles.modalBadgeText, { color: selected.unlocked ? DUO.green : DUO.textMuted }]}>
                    {selected.unlocked ? '✓ Deblocat' : '🔒 Blocat'}
                  </Text>
                </View>
              </>
            )}
          </View>
        </TouchableOpacity>
      </Modal>

      {/* Header */}
      <LinearGradient colors={[DUO.purple + '20', DUO.bg]} style={[styles.header, { paddingTop: insets.top + 12 }]}>
        <ProgressRing progress={achieveProg} size={80} strokeWidth={6} color={DUO.purple}>
          <Text style={styles.levelNum}>{stats?.level || 1}</Text>
        </ProgressRing>
        <Text style={styles.levelName}>{stats?.level_name || 'Incepator'}</Text>
        <Text style={styles.xpText}>{stats?.xp || 0} XP</Text>
        <View style={styles.xpBarBg}>
          <LinearGradient colors={[DUO.yellow, DUO.orange]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={[styles.xpBarFill, { width: `${xpProg * 100}%` }]} />
        </View>
        <Text style={styles.xpProgress}>{stats?.xp_progress || 0}/{stats?.xp_needed || 100} XP la nivel urmator</Text>
      </LinearGradient>

      {/* Stats Strip */}
      <View style={styles.statsStrip}>
        {[
          { emoji: '🔥', value: stats?.current_streak || 0, label: 'Streak' },
          { emoji: '⭐', value: stats?.best_streak || 0, label: 'Best' },
          { emoji: '🏆', value: `${stats?.achievements_count || 0}/${stats?.total_achievements || 0}`, label: 'Realizari' },
        ].map((item, i) => (
          <View key={i} style={[styles.stripItem, i > 0 && { borderLeftWidth: 1, borderLeftColor: DUO.surface }]}>
            <Text style={styles.stripEmoji}>{item.emoji}</Text>
            <Text style={styles.stripValue}>{item.value}</Text>
            <Text style={styles.stripLabel}>{item.label}</Text>
          </View>
        ))}
      </View>

      {/* Achievements Grid */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Realizari</Text>
        <View style={styles.grid}>
          {achievements.map((a) => (
            <TouchableOpacity key={a.id} style={[styles.achieveCard, !a.unlocked && styles.achieveLocked]} onPress={() => setSelected(a)}>
              <Text style={[styles.achieveIcon, !a.unlocked && { opacity: 0.3 }]}>{a.unlocked ? a.icon : '🔒'}</Text>
              <Text style={[styles.achieveName, !a.unlocked && { color: DUO.textMuted }]} numberOfLines={2}>{a.name}</Text>
              <View style={[styles.achieveXpBadge, !a.unlocked && { backgroundColor: DUO.surface }]}>
                <Text style={[styles.achieveXpText, !a.unlocked && { color: DUO.textMuted }]}>+{a.xp}</Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* Tips */}
      <View style={[styles.section, { paddingTop: 0 }]}>
        <Text style={styles.sectionTitle}>💡 Cum deblochezi mai multe</Text>
        {['Raspunde corect consecutiv', 'Rezolva din toate subiectele', 'Completeaza simulari de examen', 'Studiaza in fiecare zi'].map((tip, i) => (
          <View key={i} style={styles.tipCard}>
            <Text style={styles.tipText}>• {tip}</Text>
          </View>
        ))}
      </View>

      <View style={{ height: 100 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  header: { paddingBottom: 24, paddingHorizontal: 24, alignItems: 'center', borderBottomWidth: 1, borderBottomColor: DUO.surface },
  levelNum: { fontSize: 28, fontWeight: '800', color: DUO.purple },
  levelName: { fontSize: 22, fontWeight: '800', color: DUO.textPrimary, marginTop: 12, marginBottom: 4 },
  xpText: { fontSize: 16, color: DUO.textSecondary, fontWeight: '700', marginBottom: 12 },
  xpBarBg: { width: '100%', height: 8, backgroundColor: DUO.surface, borderRadius: 4, overflow: 'hidden' },
  xpBarFill: { height: '100%', borderRadius: 4 },
  xpProgress: { fontSize: 12, color: DUO.textMuted, marginTop: 6, fontWeight: '600' },
  statsStrip: { flexDirection: 'row', backgroundColor: DUO.card, marginHorizontal: 20, marginTop: 16, borderRadius: DUO.radiusLg, padding: 16, borderWidth: 1, borderColor: DUO.surface },
  stripItem: { flex: 1, alignItems: 'center', paddingHorizontal: 4 },
  stripEmoji: { fontSize: 24, marginBottom: 4 },
  stripValue: { fontSize: 20, fontWeight: '800', color: DUO.textPrimary },
  stripLabel: { fontSize: 11, color: DUO.textMuted, fontWeight: '700', marginTop: 2 },
  section: { padding: 20 },
  sectionTitle: { fontSize: 18, fontWeight: '800', color: DUO.textPrimary, marginBottom: 14 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  achieveCard: { width: (width - 60) / 3, backgroundColor: DUO.card, borderRadius: DUO.radius, padding: 12, alignItems: 'center', justifyContent: 'center', aspectRatio: 1, borderWidth: 1, borderColor: DUO.surface },
  achieveLocked: { opacity: 0.5 },
  achieveIcon: { fontSize: 32, marginBottom: 6 },
  achieveName: { fontSize: 10, fontWeight: '700', color: DUO.textPrimary, textAlign: 'center' },
  achieveXpBadge: { position: 'absolute', top: 6, right: 6, backgroundColor: DUO.yellow + '20', paddingHorizontal: 5, paddingVertical: 2, borderRadius: 6 },
  achieveXpText: { fontSize: 9, fontWeight: '800', color: DUO.yellow },
  tipCard: { backgroundColor: DUO.card, padding: 14, borderRadius: 12, marginBottom: 8, borderWidth: 1, borderColor: DUO.surface },
  tipText: { fontSize: 14, color: DUO.textPrimary, lineHeight: 20, fontWeight: '600' },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.7)', justifyContent: 'center', alignItems: 'center' },
  modal: { backgroundColor: DUO.card, borderRadius: 24, padding: 32, alignItems: 'center', width: '80%', borderWidth: 1, borderColor: DUO.surface },
  modalIcon: { fontSize: 64, marginBottom: 16 },
  modalName: { fontSize: 22, fontWeight: '800', color: DUO.textPrimary, marginBottom: 8, textAlign: 'center' },
  modalDesc: { fontSize: 14, color: DUO.textSecondary, textAlign: 'center', marginBottom: 16, lineHeight: 20, fontWeight: '600' },
  modalXp: { backgroundColor: DUO.yellow + '20', paddingHorizontal: 16, paddingVertical: 8, borderRadius: DUO.radiusFull, marginBottom: 12, borderWidth: 1, borderColor: DUO.yellow + '30' },
  modalXpText: { fontSize: 16, fontWeight: '800', color: DUO.yellow },
  modalBadge: { paddingHorizontal: 16, paddingVertical: 8, borderRadius: DUO.radiusFull, borderWidth: 1 },
  modalBadgeText: { fontSize: 14, fontWeight: '700' },
});
