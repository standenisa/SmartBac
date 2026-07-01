import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, ScrollView, Dimensions, Image, ImageBackground } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { apiGet, apiPost } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import { TYPO } from '@/constants/typography';
import StreakBadge from '@/components/StreakBadge';
import ProgressRing from '@/components/ProgressRing';
import AnimatedPressable from '@/components/AnimatedPressable';
import AnimatedCounter from '@/components/AnimatedCounter';

const { width } = Dimensions.get('window');

interface Stats { total_attempts: number; correct_answers: number; accuracy: number; }
interface GamificationData { xp: number; level: number; level_name: string; current_streak: number; }
interface DailyChallengeData { exercise: any; countdown_seconds: number; attempted: boolean; completed: boolean; xp_reward: number; }

const PROFILES: { id: string; name: string; icon: keyof typeof Ionicons.glyphMap; color: string; difficulty: string }[] = [
  { id: 'M1', name: 'Mate-Info', icon: 'code-slash', color: DUO.purple, difficulty: 'Avansat' },
  { id: 'M2', name: 'Științe', icon: 'flask', color: DUO.blue, difficulty: 'Mediu-Avansat' },
  { id: 'M3', name: 'Tehnologic', icon: 'construct', color: DUO.orange, difficulty: 'Mediu' },
  { id: 'M4', name: 'Pedagogic', icon: 'people', color: DUO.green, difficulty: 'Accesibil' },
];

const PROFILE_NAMES: Record<string, string> = {
  M1: 'Mate-Info',
  M2: 'Științele Naturii',
  M3: 'Tehnologic',
  M4: 'Pedagogic',
};

type IconName = keyof typeof Ionicons.glyphMap;

const LESSONS: { id: string; label: string; icon: IconName; color: string }[] = [
  { id: 'eq', label: 'Ecuatii', icon: 'calculator', color: DUO.green },
  { id: 'der', label: 'Derivate', icon: 'trending-up', color: DUO.blue },
  { id: 'lim', label: 'Limite', icon: 'infinite', color: DUO.purple },
  { id: 'int', label: 'Integrale', icon: 'analytics', color: DUO.orange },
  { id: 'mat', label: 'Matrici', icon: 'grid', color: DUO.red },
  { id: 'prob', label: 'Probabilitati', icon: 'dice', color: DUO.yellow },
  { id: 'geo', label: 'Geometrie', icon: 'triangle', color: DUO.cyan },
  { id: 'trig', label: 'Trigonometrie', icon: 'pulse', color: DUO.pink },
];

export default function HomeScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const [selectedProfile, setSelectedProfile] = useState<'M1' | 'M2' | 'M3' | 'M4' | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [gamification, setGamification] = useState<GamificationData | null>(null);
  const [greeting, setGreeting] = useState('');
  const [dailyChallenge, setDailyChallenge] = useState<DailyChallengeData | null>(null);
  const [completedToday, setCompletedToday] = useState(0);

  useEffect(() => { updateGreeting(); }, []);

  useEffect(() => {
    if (!user?.id) return;
    fetchStats(); fetchProfile(); fetchGamification(); fetchActivity(); fetchDailyChallenge();
  }, [user?.id]);

  const updateGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Buna dimineata');
    else if (hour < 18) setGreeting('Buna ziua');
    else setGreeting('Buna seara');
  };

  const fetchStats = async () => {
    try {
      const data = await apiGet<Stats>(`/api/stats?user_id=${user?.id}`);
      setStats(data);
    } catch (e) { console.log('fetchStats failed:', e); }
  };

  const fetchProfile = async () => {
    try {
      if (user?.profile) { setSelectedProfile(user.profile as any); return; }
      const data = await apiGet<{ profile: string }>(`/api/get-profile?user_id=${user?.id}`);
      if (data.profile) setSelectedProfile(data.profile as any);
    } catch (e) { console.log('fetchProfile failed:', e); }
  };

  const fetchGamification = async () => {
    try {
      const data = await apiGet<any>(`/api/gamification/stats?user_id=${user?.id}`);
      if (data.success) setGamification({ xp: data.xp, level: data.level, level_name: data.level_name, current_streak: data.current_streak });
    } catch (e) { console.log('fetchGamification failed:', e); }
  };

  const fetchActivity = async () => {
    try {
      const data = await apiGet<any>(`/api/stats/activity?user_id=${user?.id}`);
      const today = new Date().toISOString().slice(0, 10);
      setCompletedToday(data.activity?.[today] || 0);
    } catch (e) { console.log('fetchActivity failed:', e); }
  };

  const fetchDailyChallenge = async () => {
    try {
      const data = await apiGet<any>(`/api/daily-challenge?user_id=${user?.id}`);
      if (data.success) setDailyChallenge(data);
    } catch (e) { console.log('fetchDailyChallenge failed:', e); }
  };

  const formatCountdown = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${h}h ${m}m`;
  };

  const setProfile = async (profile: 'M1' | 'M2' | 'M3' | 'M4') => {
    setSelectedProfile(profile);
    try {
      await apiPost('/api/set-profile', { profile });
    } catch (e) { console.log('setProfile failed:', e); }
  };

  const dailyGoal = 5;
  const progressPercent = Math.min(completedToday / dailyGoal, 1);
  const xpProgress = gamification ? (gamification.xp % 100) / 100 : 0;
  const daysUntilBAC = Math.max(0, Math.ceil((new Date('2026-07-01').getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)));

  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <LinearGradient colors={[DUO.bgLight, DUO.bg]} style={[styles.header, { paddingTop: insets.top + 12 }]}>
          <View>
            <Text style={[styles.greeting, TYPO.caption]}>{greeting}!</Text>
            <Text style={[styles.userName, TYPO.heading2]}>BAC 2026 · {selectedProfile || 'M1'}</Text>
          </View>
          <View style={styles.headerRight}>
            <StreakBadge count={gamification?.current_streak || 0} />
            <View style={styles.xpBadge}>
              <Ionicons name="flash" size={14} color={DUO.yellow} />
              <Text style={styles.xpText}>{gamification?.xp || 0}</Text>
            </View>
            <AnimatedPressable onPress={() => router.push('/settings')} style={styles.settingsBtn}>
              <Ionicons name="settings-sharp" size={18} color={DUO.textSecondary} />
            </AnimatedPressable>
          </View>
        </LinearGradient>

        {/* Hero Banner */}
        <View style={styles.heroBanner}>
          <ImageBackground
            source={require('@/assets/images/hero-math.jpeg')}
            style={styles.heroImage}
            imageStyle={{ borderRadius: 20, opacity: 0.4 }}
          >
            <LinearGradient
              colors={['rgba(15,23,42,0.6)', 'rgba(15,23,42,0.9)']}
              style={styles.heroOverlay}
            >
              <Text style={styles.heroTitle}>SmartBAC</Text>
              <Text style={styles.heroSubtitle}>Pregătirea ta inteligentă pentru BAC</Text>
              <View style={styles.heroBadgeRow}>
                <View style={styles.heroBadge}>
                  <Ionicons name="flash" size={14} color={DUO.yellow} />
                  <Text style={styles.heroBadgeText}>AI-Powered</Text>
                </View>
                <View style={styles.heroBadge}>
                  <Ionicons name="school" size={14} color={DUO.green} />
                  <Text style={styles.heroBadgeText}>{daysUntilBAC} zile</Text>
                </View>
              </View>
            </LinearGradient>
          </ImageBackground>
        </View>

        {/* Daily Goal with Progress Ring */}
        <View style={styles.dailyCard}>
          <ProgressRing progress={progressPercent} size={80} strokeWidth={6} color={DUO.green}>
            <Text style={styles.dailyRingText}>{completedToday}/{dailyGoal}</Text>
          </ProgressRing>
          <View style={styles.dailyInfo}>
            <Text style={[styles.dailyTitle, TYPO.subheading]}>Obiectivul de azi</Text>
            <Text style={[styles.dailySubtitle, TYPO.label]}>{completedToday}/{dailyGoal} exercitii rezolvate</Text>
            <View style={styles.progressBarBg}>
              <LinearGradient
                colors={[DUO.green, DUO.greenLight]}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
                style={[styles.progressBarFill, { width: `${progressPercent * 100}%` }]}
              />
            </View>
          </View>
        </View>

        {/* Profile Selection */}
        <View style={styles.profileCard}>
          <View style={styles.profileHeader}>
            <Ionicons name="school" size={18} color={DUO.purple} />
            <Text style={[styles.profileTitle, TYPO.subheading]}>Profilul tău BAC</Text>
          </View>
          <Text style={[styles.profileSubtitle, TYPO.label]}>
            {selectedProfile
              ? `${selectedProfile} — ${PROFILE_NAMES[selectedProfile]}`
              : 'Selectează profilul liceului tău'}
          </Text>
          <View style={styles.profileGrid}>
            {PROFILES.map(p => {
              const active = selectedProfile === p.id;
              return (
                <TouchableOpacity
                  key={p.id}
                  style={[styles.profileItem, active && { borderColor: p.color, backgroundColor: p.color + '15' }]}
                  onPress={() => setProfile(p.id as any)}
                  activeOpacity={0.7}
                >
                  <View style={[styles.profileIconWrap, { backgroundColor: active ? p.color : DUO.surface }]}>
                    <Ionicons name={p.icon} size={20} color={active ? DUO.white : DUO.textMuted} />
                  </View>
                  <Text style={[styles.profileItemId, active && { color: p.color }]}>{p.id}</Text>
                  <Text style={styles.profileItemName}>{p.name}</Text>
                  <Text style={[styles.profileItemDiff, active && { color: p.color }]}>{p.difficulty}</Text>
                </TouchableOpacity>
              );
            })}
          </View>
        </View>

        {/* XP Level Bar */}
        {gamification && (
          <View style={styles.levelCard}>
            <View style={styles.levelHeader}>
              <LinearGradient colors={[DUO.yellow, DUO.yellowDark]} style={styles.levelBadge}>
                <Text style={styles.levelBadgeText}>Lv. {gamification.level}</Text>
              </LinearGradient>
              <Text style={[styles.levelName, TYPO.label]}>{gamification.level_name}</Text>
            </View>
            <View style={styles.xpBarBg}>
              <LinearGradient colors={[DUO.yellow, DUO.orange]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={[styles.xpBarFill, { width: `${xpProgress * 100}%` }]} />
            </View>
            <Text style={[styles.xpBarLabel, TYPO.caption]}>{gamification.xp % 100}/100 XP</Text>
          </View>
        )}

        {/* Daily Challenge Card */}
        {dailyChallenge && !dailyChallenge.completed && (
          <AnimatedPressable
            style={styles.dailyChallengeCard}
            onPress={() => router.push('/(tabs)/exercises')}
          >
            <LinearGradient colors={[DUO.orange + '20', DUO.orange + '05']} style={styles.dcGradient}>
              <View style={styles.dcLeft}>
                <LinearGradient
                  colors={[DUO.orange, DUO.orangeDark]}
                  style={styles.dcIconWrap}
                >
                  <Ionicons name="trophy" size={22} color={DUO.white} />
                </LinearGradient>
                <View>
                  <Text style={[styles.dcTitle, TYPO.subheading]}>Provocarea Zilnica</Text>
                  <Text style={styles.dcSubtitle}>+{dailyChallenge.xp_reward} XP bonus</Text>
                </View>
              </View>
              <View style={styles.dcRight}>
                <View style={styles.dcTimerRow}>
                  <Ionicons name="time-outline" size={12} color={DUO.textMuted} />
                  <Text style={styles.dcTimer}>{formatCountdown(dailyChallenge.countdown_seconds)}</Text>
                </View>
                <View style={styles.dcButtonRow}>
                  <Text style={styles.dcButton}>INCEPE</Text>
                  <Ionicons name="arrow-forward" size={14} color={DUO.orange} />
                </View>
              </View>
            </LinearGradient>
          </AnimatedPressable>
        )}

        {/* Quick Stats */}
        <View style={styles.statsRow}>
          {[
            { value: stats?.total_attempts || 0, label: 'Exercitii', color: DUO.green },
            { value: stats?.accuracy || 0, label: 'Acuratete', color: DUO.blue, suffix: '%' },
            { value: daysUntilBAC, label: 'Zile BAC', color: DUO.orange },
          ].map((s, i) => (
            <View key={i} style={[styles.statCard, { shadowColor: s.color }]}>
              <AnimatedCounter
                value={s.value}
                suffix={s.suffix || ''}
                style={{ ...styles.statNumber, color: s.color }}
              />
              <Text style={[styles.statLabel, TYPO.caption]}>{s.label}</Text>
            </View>
          ))}
        </View>

        {/* Learning Path */}
        <Text style={[styles.sectionTitle, TYPO.heading2]}>Calea de invatare</Text>
        <View style={styles.pathContainer}>
          {LESSONS.map((lesson, index) => {
            const isUnlocked = index < 3;
            const offset = index % 2 === 0 ? -30 : 30;
            return (
              <View key={lesson.id} style={styles.pathItem}>
                {index > 0 && (
                  <View style={[styles.pathLine, { backgroundColor: isUnlocked ? lesson.color + '60' : DUO.surface }]} />
                )}
                <TouchableOpacity
                  style={[
                    styles.lessonCircle,
                    {
                      backgroundColor: isUnlocked ? lesson.color + '20' : DUO.surface,
                      borderColor: isUnlocked ? lesson.color : DUO.surface,
                      marginLeft: offset,
                      shadowColor: isUnlocked ? lesson.color : 'transparent',
                      shadowOpacity: isUnlocked ? 0.4 : 0,
                      shadowRadius: 12,
                      shadowOffset: { width: 0, height: 4 },
                      elevation: isUnlocked ? 8 : 0,
                    },
                  ]}
                  onPress={() => isUnlocked && router.push('/(tabs)/exercises')}
                  activeOpacity={isUnlocked ? 0.7 : 1}
                >
                  {isUnlocked ? (
                    <Ionicons name={lesson.icon} size={32} color={lesson.color} />
                  ) : (
                    <Ionicons name="lock-closed" size={28} color={DUO.textMuted} />
                  )}
                </TouchableOpacity>
                <Text style={[styles.lessonLabel, { marginLeft: offset, color: isUnlocked ? DUO.textPrimary : DUO.textMuted }]}>
                  {lesson.label}
                </Text>
              </View>
            );
          })}
        </View>

        {/* Quick Actions */}
        <Text style={[styles.sectionTitle, TYPO.heading2]}>Actiuni rapide</Text>
        <View style={styles.actionsGrid}>
          {([
            { icon: 'flash' as IconName, title: 'Quick Practice', route: '/(tabs)/quick-practice', colors: [DUO.yellow, DUO.yellowDark] as [string, string] },
            { icon: 'school' as IconName, title: 'Simulare', route: '/(tabs)/exam', colors: [DUO.purple, DUO.purpleDark] as [string, string] },
            { icon: 'book' as IconName, title: 'Teorie', route: '/(tabs)/theory', colors: [DUO.blue, DUO.blueDark] as [string, string] },
            { icon: 'chatbubbles' as IconName, title: 'Chat AI', route: '/(tabs)/chat', colors: [DUO.green, DUO.greenDark] as [string, string] },
          ]).map((action, i) => (
            <AnimatedPressable key={i} style={styles.actionCard} onPress={() => router.push(action.route as any)}>
              <LinearGradient colors={action.colors} style={styles.actionGradient}>
                <View style={styles.actionIconWrap}>
                  <Ionicons name={action.icon} size={26} color={DUO.white} />
                </View>
                <Text style={styles.actionTitle}>{action.title}</Text>
              </LinearGradient>
            </AnimatedPressable>
          ))}
        </View>

        <View style={{ height: 100 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 20, paddingBottom: 16 },
  greeting: { color: DUO.textSecondary },
  userName: { color: DUO.textPrimary, marginTop: 2 },
  headerRight: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  xpBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: DUO.yellow + '20', paddingHorizontal: 10, paddingVertical: 4, borderRadius: DUO.radiusFull, gap: 4, borderWidth: 1, borderColor: DUO.yellow + '30' },
  xpText: { fontSize: 14, fontWeight: '800', color: DUO.yellow },
  settingsBtn: { width: 36, height: 36, borderRadius: 18, backgroundColor: DUO.surface, justifyContent: 'center', alignItems: 'center' },
  dailyCard: { flexDirection: 'row', backgroundColor: DUO.card, marginHorizontal: 20, borderRadius: DUO.radiusLg, padding: 16, marginBottom: 16, alignItems: 'center', borderWidth: 1, borderColor: DUO.green + '20' },
  dailyRingText: { fontSize: 14, fontWeight: '800', color: DUO.green },
  dailyInfo: { flex: 1, marginLeft: 16 },
  dailyTitle: { color: DUO.textPrimary, marginBottom: 2 },
  dailySubtitle: { color: DUO.textSecondary, marginBottom: 8 },
  progressBarBg: { height: 8, backgroundColor: DUO.surface, borderRadius: 4, overflow: 'hidden' },
  progressBarFill: { height: '100%', borderRadius: 4 },
  profileCard: { backgroundColor: DUO.card, marginHorizontal: 20, borderRadius: DUO.radiusLg, padding: 16, marginBottom: 16, borderWidth: 1, borderColor: DUO.purple + '20' },
  profileHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 4 },
  profileTitle: { color: DUO.textPrimary },
  profileSubtitle: { color: DUO.textSecondary, marginBottom: 14 },
  profileGrid: { flexDirection: 'row', gap: 8 },
  profileItem: {
    flex: 1, alignItems: 'center', paddingVertical: 14, paddingHorizontal: 4,
    borderRadius: DUO.radius, backgroundColor: DUO.surface,
    borderWidth: 1.5, borderColor: DUO.surfaceLight, gap: 4,
  },
  profileIconWrap: {
    width: 36, height: 36, borderRadius: 10,
    justifyContent: 'center', alignItems: 'center', marginBottom: 2,
  },
  profileItemId: { fontSize: 14, fontWeight: '900', color: DUO.textPrimary },
  profileItemName: { fontSize: 10, fontWeight: '600', color: DUO.textMuted, textAlign: 'center' },
  profileItemDiff: { fontSize: 9, fontWeight: '700', color: DUO.textMuted, marginTop: 2 },
  levelCard: { backgroundColor: DUO.card, marginHorizontal: 20, borderRadius: DUO.radiusLg, padding: 16, marginBottom: 16, borderWidth: 1, borderColor: DUO.yellow + '15' },
  levelHeader: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 10 },
  levelBadge: { paddingHorizontal: 12, paddingVertical: 4, borderRadius: DUO.radiusFull },
  levelBadgeText: { fontSize: 13, fontWeight: '800', color: '#1B1B2F' },
  levelName: { color: DUO.textSecondary },
  xpBarBg: { height: 8, backgroundColor: DUO.surface, borderRadius: 4, overflow: 'hidden' },
  xpBarFill: { height: '100%', borderRadius: 4 },
  xpBarLabel: { color: DUO.textMuted, textAlign: 'right', marginTop: 4 },
  dailyChallengeCard: { marginHorizontal: 20, marginBottom: 16, borderRadius: 20, overflow: 'hidden', borderWidth: 1, borderColor: DUO.orange + '25' },
  dcGradient: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 16 },
  dcLeft: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  dcIconWrap: {
    width: 44, height: 44, borderRadius: 14,
    justifyContent: 'center', alignItems: 'center',
    shadowColor: DUO.orange, shadowOpacity: 0.4, shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 }, elevation: 4,
  },
  dcTitle: { color: DUO.textPrimary },
  dcSubtitle: { fontSize: 12, fontWeight: '700', color: DUO.orange },
  dcRight: { alignItems: 'flex-end', gap: 4 },
  dcTimerRow: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  dcTimer: { fontSize: 11, color: DUO.textMuted, fontWeight: '600' },
  dcButtonRow: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  dcButton: { fontSize: 13, fontWeight: '800', color: DUO.orange, letterSpacing: 0.5 },
  statsRow: { flexDirection: 'row', paddingHorizontal: 20, gap: 10, marginBottom: 24 },
  statCard: { flex: 1, backgroundColor: DUO.card, paddingVertical: 14, borderRadius: DUO.radius, alignItems: 'center', borderWidth: 1, borderColor: DUO.surfaceLight, shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.2, shadowRadius: 8, elevation: 4 },
  statNumber: { fontSize: 22, fontWeight: '800' },
  statLabel: { color: DUO.textMuted, marginTop: 2 },
  sectionTitle: { color: DUO.textPrimary, paddingHorizontal: 20, marginBottom: 16 },
  pathContainer: { alignItems: 'center', paddingBottom: 24 },
  pathItem: { alignItems: 'center', marginBottom: 8 },
  pathLine: { width: 4, height: 24, borderRadius: 2, marginBottom: 4 },
  lessonCircle: { width: 70, height: 70, borderRadius: 35, justifyContent: 'center', alignItems: 'center', borderWidth: 2, marginBottom: 4 },
  lessonLabel: { fontSize: 12, fontWeight: '700' },
  actionsGrid: { flexDirection: 'row', flexWrap: 'wrap', paddingHorizontal: 20, gap: 10 },
  actionCard: { width: (width - 50) / 2, borderRadius: DUO.radiusLg, overflow: 'hidden', borderBottomWidth: DUO.borderBottom, borderBottomColor: 'rgba(0,0,0,0.2)' },
  actionGradient: { paddingVertical: 24, alignItems: 'center', borderRadius: DUO.radiusLg, gap: 10 },
  actionIconWrap: {
    width: 48, height: 48, borderRadius: 14,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center', alignItems: 'center',
  },
  actionTitle: { fontSize: 14, fontWeight: '800', color: DUO.white, letterSpacing: 0.3 },

  // Hero banner
  heroBanner: { marginHorizontal: 20, marginBottom: 16, borderRadius: 20, overflow: 'hidden' },
  heroImage: { width: '100%', height: 160 },
  heroOverlay: {
    flex: 1, justifyContent: 'center', paddingHorizontal: 24, paddingVertical: 20,
    borderRadius: 20, gap: 6,
  },
  heroTitle: { fontSize: 28, fontWeight: '900', color: DUO.white, letterSpacing: 1 },
  heroSubtitle: { fontSize: 14, fontWeight: '600', color: DUO.textSecondary },
  heroBadgeRow: { flexDirection: 'row', gap: 10, marginTop: 6 },
  heroBadge: {
    flexDirection: 'row', alignItems: 'center', gap: 4,
    backgroundColor: 'rgba(255,255,255,0.1)', paddingHorizontal: 10, paddingVertical: 4,
    borderRadius: 999, borderWidth: 1, borderColor: 'rgba(255,255,255,0.15)',
  },
  heroBadgeText: { fontSize: 12, fontWeight: '700', color: DUO.snow },
});
