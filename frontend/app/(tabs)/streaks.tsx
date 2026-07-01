import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, ScrollView, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Haptics from 'expo-haptics';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { apiGet, apiPost } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import { TYPO } from '@/constants/typography';
import DuoButton from '@/components/DuoButton';
import ConfettiAnimation from '@/components/ConfettiAnimation';
import AnimatedCounter from '@/components/AnimatedCounter';
import AnimatedPressable from '@/components/AnimatedPressable';
import StudyHeatmap from '@/components/StudyHeatmap';
import { useToast } from '@/contexts/ToastContext';

const { width } = Dimensions.get('window');

interface StreakData { currentStreak: number; longestStreak: number; totalDaysStudied: number; lastStudyDate: string | null; weeklyActivity: boolean[]; }
interface GamificationStats { xp: number; level: number; level_name: string; current_streak: number; best_streak: number; achievements_count: number; total_achievements: number; }
interface BackendAchievement { id: string; name: string; description: string; icon: string; unlocked: boolean; }
interface DailyChallenge { id: string; title: string; description: string; target: number; current: number; reward: number; emoji: string; }

const DAILY_CHALLENGES: DailyChallenge[] = [
  { id: '1', title: 'Exercise Master', description: '5 exercitii', target: 5, current: 0, reward: 10, emoji: '✏️' },
  { id: '2', title: 'Perfect Score', description: '3 corecte la rand', target: 3, current: 0, reward: 15, emoji: '🎯' },
  { id: '3', title: 'Study Session', description: '30 min studiu', target: 30, current: 0, reward: 20, emoji: '⏰' },
];

export default function StreaksScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const { showToast } = useToast();
  const [streakData, setStreakData] = useState<StreakData>({ currentStreak: 0, longestStreak: 0, totalDaysStudied: 0, lastStudyDate: null, weeklyActivity: [false, false, false, false, false, false, false] });
  const [gamification, setGamification] = useState<GamificationStats | null>(null);
  const [streakFreezes, setStreakFreezes] = useState(0);
  const [achievements, setAchievements] = useState<BackendAchievement[]>([]);
  const [todayCompleted, setTodayCompleted] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [heatmapData, setHeatmapData] = useState<Record<string, number>>({});

  useEffect(() => { loadData(); }, []);

  useEffect(() => {
    if (!user?.id) return;
    fetchBackend();
    fetchHeatmap();
  }, [user?.id]);

  const fetchHeatmap = async () => {
    try {
      const data = await apiGet<any>(`/api/stats/activity?user_id=${user?.id}`);
      if (data.activity) setHeatmapData(data.activity);
    } catch {
      // Generate mock data for demo
      const mock: Record<string, number> = {};
      const today = new Date();
      for (let i = 0; i < 84; i++) {
        const d = new Date(today);
        d.setDate(d.getDate() - i);
        const ds = d.toISOString().split('T')[0];
        mock[ds] = Math.random() > 0.35 ? Math.floor(Math.random() * 12) : 0;
      }
      setHeatmapData(mock);
    }
  };

  const loadData = async () => {
    try {
      const stored = await AsyncStorage.getItem('streakData');
      if (stored) {
        const data = JSON.parse(stored);
        const today = new Date().toDateString();
        const yesterday = new Date(Date.now() - 86400000).toDateString();
        if (data.lastStudyDate === today) { setTodayCompleted(true); setStreakData(data); }
        else if (data.lastStudyDate === yesterday) setStreakData(data);
        else if (data.lastStudyDate) setStreakData({ ...data, currentStreak: 0, weeklyActivity: [false, false, false, false, false, false, false] });
      }
    } catch (e) { console.log('Error:', e); }
  };

  const fetchBackend = async () => {
    try {
      const [sData, aData] = await Promise.all([
        apiGet<any>(`/api/gamification/stats?user_id=${user?.id}`),
        apiGet<any>(`/api/gamification/achievements?user_id=${user?.id}`),
      ]);
      if (sData.success) {
        setGamification(sData);
        setStreakFreezes(sData.streak_freezes || 0);
      }
      if (aData.success) setAchievements(aData.achievements || []);
    } catch (e) { console.log('Error:', e); }
  };

  const checkIn = async () => {
    if (todayCompleted) return;
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    const today = new Date();
    const newWeekly = [...streakData.weeklyActivity];
    newWeekly[today.getDay()] = true;
    const newStreak = streakData.currentStreak + 1;
    const newData: StreakData = {
      currentStreak: newStreak, longestStreak: Math.max(newStreak, streakData.longestStreak),
      totalDaysStudied: streakData.totalDaysStudied + 1, lastStudyDate: today.toDateString(), weeklyActivity: newWeekly,
    };
    setStreakData(newData); setTodayCompleted(true); setShowConfetti(true);
    await AsyncStorage.setItem('streakData', JSON.stringify(newData));
    setTimeout(() => setShowConfetti(false), 2500);
  };

  const days = ['D', 'L', 'M', 'M', 'J', 'V', 'S'];
  const streak = gamification?.current_streak ?? streakData.currentStreak;
  const bestStreak = gamification?.best_streak ?? streakData.longestStreak;

  return (
    <View style={styles.container}>
      <ConfettiAnimation visible={showConfetti} />
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <LinearGradient colors={[DUO.card, DUO.bg]} style={[styles.header, { paddingTop: insets.top + 12 }]}>
          <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
            <Ionicons name="flame" size={28} color={DUO.orange} />
            <Text style={[styles.headerTitle, TYPO.heading1]}>Streak-uri</Text>
          </View>
          <Text style={[styles.headerSubtitle, TYPO.label]}>Construieste obiceiuri de studiu</Text>
        </LinearGradient>

        {/* Study Heatmap */}
        <View style={{ marginHorizontal: 20, marginBottom: 16 }}>
          <StudyHeatmap activity={heatmapData} weeks={12} />
        </View>

        {/* Main Streak */}
        <View style={styles.streakCard}>
          <Ionicons name={streak >= 7 ? 'flame' : streak > 0 ? 'leaf' : 'snow'} size={56} color={streak >= 7 ? DUO.orange : streak > 0 ? DUO.green : DUO.cyan} />
          <AnimatedCounter value={streak} style={styles.streakNum} />
          <Text style={styles.streakLabel}>Zile consecutive</Text>
          {!todayCompleted ? (
            <DuoButton title="CHECK IN AZI!" onPress={checkIn} color={DUO.green} darkColor={DUO.greenDark} glow style={{ marginTop: 16 }} />
          ) : (
            <View style={styles.doneBadge}>
              <Ionicons name="checkmark-circle" size={16} color={DUO.green} />
              <Text style={styles.doneText}>Azi completat!</Text>
            </View>
          )}
        </View>

        {/* XP / Level */}
        {gamification && (
          <View style={styles.xpRow}>
            <View style={[styles.xpCard, { shadowColor: DUO.yellow }]}>
              <Ionicons name="flash" size={20} color={DUO.yellow} />
              <Text style={[styles.xpValue, { color: DUO.yellow }]}>{gamification.xp}</Text>
              <Text style={styles.xpLabel}>XP</Text>
            </View>
            <View style={[styles.xpCard, { shadowColor: DUO.purple }]}>
              <Ionicons name="medal" size={20} color={DUO.purple} />
              <Text style={[styles.xpValue, { color: DUO.purple }]}>Lv.{gamification.level}</Text>
              <Text style={styles.xpLabel}>{gamification.level_name}</Text>
            </View>
          </View>
        )}

        {/* Streak Freeze & Liga */}
        <View style={styles.freezeRow}>
          <AnimatedPressable
            style={styles.freezeCard}
            onPress={async () => {
              if (streakFreezes <= 0) { showToast({ type: 'error', title: 'Nu ai freeze-uri', subtitle: 'Obtii freeze la fiecare 7 zile de streak' }); return; }
              try {
                const data = await apiPost<any>(`/api/gamification/streak/freeze?user_id=${user?.id}`);
                if (data.success) {
                  setStreakFreezes(data.streak_freezes);
                  showToast({ type: 'streak', title: 'Freeze activat!', subtitle: 'Streak-ul tau este protejat azi' });
                }
              } catch (e) { console.log('Error:', e); }
            }}
          >
            <Ionicons name="snow" size={24} color={DUO.cyan} />
            <Text style={styles.freezeCount}>{streakFreezes}</Text>
            <Text style={styles.freezeLabel}>Freeze</Text>
          </AnimatedPressable>

          <AnimatedPressable style={styles.ligaCard} onPress={() => router.push('/(tabs)/leagues')}>
            <Ionicons name="trophy" size={24} color={DUO.yellow} />
            <Text style={styles.ligaText}>Liga</Text>
            <Ionicons name="arrow-forward" size={14} color={DUO.yellow} />
          </AnimatedPressable>
        </View>

        {/* Weekly */}
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, TYPO.heading3]}>Saptamana asta</Text>
          <View style={styles.weekRow}>
            {streakData.weeklyActivity.map((active, i) => (
              <View key={i} style={styles.dayCol}>
                <View style={[styles.dayCircle, active && styles.dayCircleActive, i === new Date().getDay() && styles.dayCircleToday]}>
                  {active && <Ionicons name="checkmark" size={18} color={DUO.white} />}
                </View>
                <Text style={[styles.dayLabel, i === new Date().getDay() && { color: DUO.orange }]}>{days[i]}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Stats Row */}
        <View style={styles.miniRow}>
          <View style={[styles.miniCard, { shadowColor: DUO.orange }]}>
            <Text style={[styles.miniNum, { color: DUO.orange }]}>{bestStreak}</Text>
            <Text style={styles.miniLabel}>Best Streak</Text>
          </View>
          <View style={[styles.miniCard, { shadowColor: DUO.blue }]}>
            <Text style={[styles.miniNum, { color: DUO.blue }]}>{streakData.totalDaysStudied}</Text>
            <Text style={styles.miniLabel}>Total Zile</Text>
          </View>
        </View>

        {/* Challenges */}
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, TYPO.heading3]}>Provocari Zilnice</Text>
          {DAILY_CHALLENGES.map((c) => {
            const prog = Math.min(c.current / c.target, 1);
            const done = c.current >= c.target;
            return (
              <View key={c.id} style={styles.challengeCard}>
                <View style={styles.challengeRow}>
                  <Ionicons name={c.emoji === '✏️' ? 'pencil' : c.emoji === '🎯' ? 'disc' : 'alarm'} size={28} color={DUO.orange} />
                  <View style={styles.challengeInfo}>
                    <Text style={styles.challengeTitle}>{c.title}</Text>
                    <Text style={styles.challengeDesc}>{c.description}</Text>
                  </View>
                  <View style={styles.rewardBadge}>
                    <Text style={styles.rewardText}>+{c.reward}</Text>
                    <Text style={styles.rewardSub}>XP</Text>
                  </View>
                </View>
                <View style={styles.progBg}>
                  <View style={[styles.progFill, { width: `${prog * 100}%`, backgroundColor: done ? DUO.green : DUO.orange }]} />
                </View>
                <View style={{ flexDirection: 'row', justifyContent: 'flex-end', alignItems: 'center', gap: 4 }}>
                  <Text style={styles.progText}>{c.current}/{c.target}</Text>
                  {done && <Ionicons name="checkmark-circle" size={14} color={DUO.green} />}
                </View>
              </View>
            );
          })}
        </View>

        {/* Achievements */}
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, TYPO.heading3]}>
            Realizari {gamification ? `(${gamification.achievements_count}/${gamification.total_achievements})` : ''}
          </Text>
          <View style={styles.achieveGrid}>
            {(achievements.length > 0 ? achievements : [
              { id: '1', name: 'Getting Started', description: '3 zile streak', icon: '🌱', unlocked: false },
              { id: '2', name: 'One Week', description: '7 zile streak', icon: '🔥', unlocked: false },
              { id: '3', name: 'Two Weeks', description: '14 zile streak', icon: '⚡', unlocked: false },
              { id: '4', name: 'Monthly', description: '30 zile streak', icon: '🏆', unlocked: false },
            ]).map((a) => (
              <View key={a.id} style={[styles.achieveCard, !a.unlocked && styles.achieveLocked]}>
                <Text style={[styles.achieveEmoji, !a.unlocked && { opacity: 0.3 }]}>{a.icon}</Text>
                <Text style={[styles.achieveTitle, !a.unlocked && { color: DUO.textMuted }]}>{a.name}</Text>
                <Text style={styles.achieveDesc}>{a.description}</Text>
                {!a.unlocked && <View style={styles.lockBadge}><Text style={{ fontSize: 14 }}>🔒</Text></View>}
              </View>
            ))}
          </View>
        </View>

        {/* Quote */}
        <View style={styles.quoteCard}>
          <Text style={styles.quoteText}>"Succesul este suma eforturilor mici, repetate zi de zi."</Text>
          <Text style={styles.quoteAuthor}>- Robert Collier</Text>
        </View>

        <View style={{ height: 100 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  header: { paddingBottom: 20, paddingHorizontal: 20, borderBottomWidth: 1, borderBottomColor: DUO.surface },
  headerTitle: { fontSize: 28, fontWeight: '800', color: DUO.textPrimary, marginBottom: 4 },
  headerSubtitle: { fontSize: 14, color: DUO.textSecondary, fontWeight: '600' },
  streakCard: { marginHorizontal: 20, marginTop: 20, backgroundColor: DUO.orange + '10', borderRadius: DUO.radiusLg, padding: 30, alignItems: 'center', borderWidth: 1, borderColor: DUO.orange + '25' },
  streakNum: { fontSize: 72, fontWeight: '800', color: DUO.textPrimary },
  streakLabel: { fontSize: 16, fontWeight: '700', color: DUO.textSecondary },
  doneBadge: { backgroundColor: DUO.green + '20', paddingHorizontal: 20, paddingVertical: 10, borderRadius: DUO.radiusFull, marginTop: 16, borderWidth: 1, borderColor: DUO.green + '30' },
  doneText: { fontSize: 15, fontWeight: '800', color: DUO.green },
  freezeRow: { flexDirection: 'row', paddingHorizontal: 20, gap: 10, marginTop: 16 },
  freezeCard: { flex: 1, backgroundColor: DUO.cyan + '15', paddingVertical: 16, borderRadius: 16, alignItems: 'center', borderWidth: 1, borderColor: DUO.cyan + '25' },
  freezeCount: { fontSize: 22, fontWeight: '800', color: DUO.cyan },
  freezeLabel: { fontSize: 11, color: DUO.textMuted, fontWeight: '700', marginTop: 2 },
  ligaCard: { flex: 1, backgroundColor: DUO.yellow + '15', paddingVertical: 16, borderRadius: 16, alignItems: 'center', borderWidth: 1, borderColor: DUO.yellow + '25', justifyContent: 'center' },
  ligaText: { fontSize: 15, fontWeight: '800', color: DUO.yellow },
  xpRow: { flexDirection: 'row', paddingHorizontal: 20, gap: 10, marginTop: 16 },
  xpCard: { flex: 1, backgroundColor: DUO.card, paddingVertical: 16, borderRadius: DUO.radius, alignItems: 'center', borderWidth: 1, borderColor: DUO.surface, shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.2, shadowRadius: 8, elevation: 4 },
  xpValue: { fontSize: 20, fontWeight: '800' },
  xpLabel: { fontSize: 11, color: DUO.textMuted, fontWeight: '700', marginTop: 2 },
  section: { padding: 20 },
  sectionTitle: { fontSize: 18, fontWeight: '800', color: DUO.textPrimary, marginBottom: 14 },
  weekRow: { flexDirection: 'row', justifyContent: 'space-between', backgroundColor: DUO.card, padding: 16, borderRadius: DUO.radiusLg, borderWidth: 1, borderColor: DUO.surface },
  dayCol: { alignItems: 'center' },
  dayCircle: { width: 36, height: 36, borderRadius: 18, backgroundColor: DUO.surface, justifyContent: 'center', alignItems: 'center', marginBottom: 4 },
  dayCircleActive: { backgroundColor: DUO.green },
  dayCircleToday: { borderWidth: 2, borderColor: DUO.orange },
  dayLabel: { fontSize: 12, fontWeight: '700', color: DUO.textMuted },
  miniRow: { flexDirection: 'row', paddingHorizontal: 20, gap: 10 },
  miniCard: { flex: 1, backgroundColor: DUO.card, padding: 16, borderRadius: DUO.radius, alignItems: 'center', borderWidth: 1, borderColor: DUO.surface, shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.2, shadowRadius: 8, elevation: 4 },
  miniNum: { fontSize: 28, fontWeight: '800' },
  miniLabel: { fontSize: 12, color: DUO.textMuted, fontWeight: '700', marginTop: 2 },
  challengeCard: { backgroundColor: DUO.card, padding: 16, borderRadius: DUO.radius, marginBottom: 10, borderWidth: 1, borderColor: DUO.surface },
  challengeRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  challengeInfo: { flex: 1 },
  challengeTitle: { fontSize: 15, fontWeight: '800', color: DUO.textPrimary },
  challengeDesc: { fontSize: 12, color: DUO.textMuted, fontWeight: '600' },
  rewardBadge: { backgroundColor: DUO.yellow + '20', paddingHorizontal: 10, paddingVertical: 4, borderRadius: DUO.radiusFull, alignItems: 'center', borderWidth: 1, borderColor: DUO.yellow + '30' },
  rewardText: { fontSize: 14, fontWeight: '800', color: DUO.yellow },
  rewardSub: { fontSize: 9, color: DUO.yellow, fontWeight: '700' },
  progBg: { height: 6, backgroundColor: DUO.surface, borderRadius: 3, overflow: 'hidden', marginBottom: 4 },
  progFill: { height: '100%', borderRadius: 3 },
  progText: { fontSize: 12, color: DUO.textMuted, textAlign: 'right', fontWeight: '700' },
  achieveGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  achieveCard: { width: (width - 50) / 2, backgroundColor: DUO.card, padding: 16, borderRadius: DUO.radius, alignItems: 'center', borderWidth: 1, borderColor: DUO.surface },
  achieveLocked: { opacity: 0.5 },
  achieveEmoji: { fontSize: 32, marginBottom: 8 },
  achieveTitle: { fontSize: 13, fontWeight: '800', color: DUO.textPrimary, textAlign: 'center', marginBottom: 2 },
  achieveDesc: { fontSize: 11, color: DUO.textMuted, textAlign: 'center', fontWeight: '600' },
  lockBadge: { position: 'absolute', top: 8, right: 8 },
  quoteCard: { marginHorizontal: 20, backgroundColor: DUO.card, padding: 24, borderRadius: DUO.radiusLg, borderWidth: 1, borderColor: DUO.purple + '20' },
  quoteText: { fontSize: 15, fontStyle: 'italic', color: DUO.textPrimary, lineHeight: 22, marginBottom: 10, fontWeight: '600' },
  quoteAuthor: { fontSize: 13, color: DUO.textMuted, textAlign: 'right', fontWeight: '600' },
});
