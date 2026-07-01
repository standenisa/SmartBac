import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { apiGet } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import ProgressRing from '@/components/ProgressRing';

interface SubjectDetail { attempts: number; correct: number; accuracy: number; }
interface GamificationData { xp: number; level: number; level_name: string; current_streak: number; best_streak: number; }

export default function ProgressScreen() {
  const { user } = useAuth();
  const [stats, setStats] = useState<{ total: number; correct: number; accuracy: number } | null>(null);
  const [subjects, setSubjects] = useState<Record<string, SubjectDetail>>({});
  const [gamification, setGamification] = useState<GamificationData | null>(null);

  useEffect(() => {
    if (!user?.id) return;
    fetchAll();
  }, [user?.id]);

  const fetchAll = async () => {
    try {
      const [sData, dData, gData] = await Promise.all([
        apiGet<any>(`/api/stats?user_id=${user?.id}`),
        apiGet<any>(`/api/stats/detailed?user_id=${user?.id}`),
        apiGet<any>(`/api/gamification/stats?user_id=${user?.id}`),
      ]);
      setStats({ total: sData.total_attempts || 0, correct: sData.correct_answers || 0, accuracy: Math.round(sData.accuracy) || 0 });
      setSubjects({
        subject_1: dData.subject_1 || { attempts: 0, correct: 0, accuracy: 0 },
        subject_2: dData.subject_2 || { attempts: 0, correct: 0, accuracy: 0 },
        subject_3: dData.subject_3 || { attempts: 0, correct: 0, accuracy: 0 },
      });
      if (gData.success) setGamification({ xp: gData.xp, level: gData.level, level_name: gData.level_name, current_streak: gData.current_streak, best_streak: gData.best_streak });
    } catch (e) { console.log('Error:', e); }
  };

  const getColor = (a: number) => { if (a >= 80) return DUO.green; if (a >= 60) return DUO.yellow; if (a >= 40) return DUO.orange; return DUO.red; };

  if (!stats) return <View style={styles.container}><Text style={{ fontSize: 48, textAlign: 'center', marginTop: 100 }}>🦉</Text><Text style={styles.loadingText}>Se incarca...</Text></View>;

  const subjectLabels: Record<string, string> = { subject_1: 'Subiectul I', subject_2: 'Subiectul II', subject_3: 'Subiectul III' };
  const subjectColors: Record<string, string> = { subject_1: DUO.blue, subject_2: DUO.green, subject_3: DUO.purple };

  return (
    <ScrollView style={styles.container}>
      <LinearGradient colors={[DUO.card, DUO.bg]} style={styles.header}>
        <Text style={styles.headerTitle}>Progresul tau</Text>
        <Text style={styles.headerSubtitle}>Urmareste-ti evolutia 🦉</Text>
      </LinearGradient>

      {/* XP Level */}
      {gamification && (
        <View style={styles.xpCard}>
          <View style={styles.xpRow}>
            {[
              { icon: '⚡', value: `${gamification.xp}`, label: 'XP Total', color: DUO.yellow },
              { icon: '🏅', value: `Lv. ${gamification.level}`, label: gamification.level_name, color: DUO.purple },
              { icon: '🔥', value: `${gamification.current_streak}`, label: 'Streak', color: DUO.orange },
            ].map((item, i) => (
              <View key={i} style={[styles.xpItem, i > 0 && { borderLeftWidth: 1, borderLeftColor: DUO.surface }]}>
                <Text style={styles.xpIcon}>{item.icon}</Text>
                <Text style={[styles.xpValue, { color: item.color }]}>{item.value}</Text>
                <Text style={styles.xpLabel}>{item.label}</Text>
              </View>
            ))}
          </View>
        </View>
      )}

      {/* Overall Ring + Stats */}
      <View style={styles.overviewSection}>
        <ProgressRing progress={stats.accuracy / 100} size={100} strokeWidth={8} color={getColor(stats.accuracy)} value={`${stats.accuracy}%`} label="Acuratete" />
        <View style={styles.overviewStats}>
          <View style={styles.overviewStatRow}>
            <Text style={styles.overviewStatLabel}>Exercitii rezolvate</Text>
            <Text style={[styles.overviewStatValue, { color: DUO.green }]}>{stats.total}</Text>
          </View>
          <View style={styles.overviewStatRow}>
            <Text style={styles.overviewStatLabel}>Corecte</Text>
            <Text style={[styles.overviewStatValue, { color: DUO.blue }]}>{stats.correct}</Text>
          </View>
          <View style={styles.overviewStatRow}>
            <Text style={styles.overviewStatLabel}>Acuratete</Text>
            <Text style={[styles.overviewStatValue, { color: getColor(stats.accuracy) }]}>{stats.accuracy}%</Text>
          </View>
        </View>
      </View>

      {/* Subject Progress */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Progres pe Subiecte</Text>
        {(['subject_1', 'subject_2', 'subject_3'] as const).map((key) => {
          const s = subjects[key] || { attempts: 0, correct: 0, accuracy: 0 };
          const color = subjectColors[key];
          return (
            <View key={key} style={styles.subjectRow}>
              <View style={styles.subjectHeader}>
                <Text style={styles.subjectName}>{subjectLabels[key]}</Text>
                <Text style={[styles.subjectAcc, { color: getColor(s.accuracy) }]}>{s.accuracy.toFixed(0)}%</Text>
              </View>
              <View style={styles.progressBg}>
                <LinearGradient colors={[color, color + 'AA']} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={[styles.progressFill, { width: `${Math.min(s.accuracy, 100)}%` }]} />
              </View>
              <Text style={styles.subjectDetail}>{s.correct}/{s.attempts} corecte</Text>
            </View>
          );
        })}
      </View>

      <View style={{ height: 100 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  loadingText: { fontSize: 16, textAlign: 'center', marginTop: 16, color: DUO.textSecondary, fontWeight: '700' },
  header: { paddingTop: 60, paddingBottom: 20, paddingHorizontal: 20, borderBottomWidth: 1, borderBottomColor: DUO.surface },
  headerTitle: { fontSize: 28, fontWeight: '800', color: DUO.textPrimary, marginBottom: 4 },
  headerSubtitle: { fontSize: 14, color: DUO.textSecondary, fontWeight: '600' },
  xpCard: { marginHorizontal: 20, marginTop: 20, backgroundColor: DUO.card, borderRadius: DUO.radiusLg, padding: 20, borderWidth: 1, borderColor: DUO.purple + '20' },
  xpRow: { flexDirection: 'row', alignItems: 'center' },
  xpItem: { flex: 1, alignItems: 'center', paddingHorizontal: 4 },
  xpIcon: { fontSize: 20, marginBottom: 4 },
  xpValue: { fontSize: 18, fontWeight: '800' },
  xpLabel: { fontSize: 11, color: DUO.textMuted, marginTop: 2, fontWeight: '600' },
  overviewSection: { flexDirection: 'row', alignItems: 'center', marginHorizontal: 20, marginTop: 20, backgroundColor: DUO.card, borderRadius: DUO.radiusLg, padding: 20, borderWidth: 1, borderColor: DUO.surface },
  overviewStats: { flex: 1, marginLeft: 20, gap: 10 },
  overviewStatRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  overviewStatLabel: { fontSize: 13, color: DUO.textSecondary, fontWeight: '600' },
  overviewStatValue: { fontSize: 16, fontWeight: '800' },
  card: { backgroundColor: DUO.card, marginHorizontal: 20, marginTop: 16, borderRadius: DUO.radiusLg, padding: 20, borderWidth: 1, borderColor: DUO.surface },
  cardTitle: { fontSize: 18, fontWeight: '800', color: DUO.textPrimary, marginBottom: 20 },
  subjectRow: { marginBottom: 18 },
  subjectHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  subjectName: { fontSize: 15, fontWeight: '700', color: DUO.textPrimary },
  subjectAcc: { fontSize: 16, fontWeight: '800' },
  progressBg: { height: 10, backgroundColor: DUO.surface, borderRadius: 5, overflow: 'hidden', marginBottom: 4 },
  progressFill: { height: '100%', borderRadius: 5 },
  subjectDetail: { fontSize: 12, color: DUO.textMuted, fontWeight: '600' },
});
