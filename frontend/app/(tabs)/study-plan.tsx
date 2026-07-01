// Study Plan — sesiuni recomandate pe baza acurateței per topic.
import { useState, useEffect } from 'react';
import {
  StyleSheet, View, Text, ScrollView, ActivityIndicator,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { DUO } from '@/constants/duo';
import { TYPO } from '@/constants/typography';
import { apiGet } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import AnimatedPressable from '@/components/AnimatedPressable';
import ProgressRing from '@/components/ProgressRing';
import Animated, { FadeInDown } from 'react-native-reanimated';

interface TopicMastery {
  topic: string;
  topicName: string;
  accuracy: number;
  attempts: number;
  mastery: 'master' | 'good' | 'learning' | 'weak' | 'new';
  emoji: string;
}

interface StudySession {
  id: number;
  title: string;
  description: string;
  topic: string;
  duration: number; // minutes
  type: 'review' | 'practice' | 'challenge' | 'theory';
  emoji: string;
  color: string;
}

const TOPIC_NAMES: Record<string, string> = {
  ecuatii: 'Ecuatii', ecuatii_gradul_1: 'Ecuatii gr. I',
  ecuatii_gradul_2: 'Ecuatii gr. II', derivate: 'Derivate',
  integrale: 'Integrale', limite: 'Limite',
  matrice: 'Matrice', determinanti: 'Determinanti',
  trigonometrie: 'Trigonometrie', combinatorica: 'Combinatorica',
  probabilitati: 'Probabilitati', geometrie: 'Geometrie',
  functii: 'Functii', vectori: 'Vectori',
  numere_complexe: 'Nr. Complexe', progresii: 'Progresii',
  logaritmi: 'Logaritmi', radicali: 'Radicali',
};

// Topicurile din backend pot veni cu chei in engleza — le mapam pe cheia canonica.
const TOPIC_ALIASES: Record<string, string> = {
  equation: 'ecuatii', derivative: 'derivate', integral: 'integrale',
  limit: 'limite', matrix: 'matrice', trigonometry: 'trigonometrie',
  combinatorics: 'combinatorica', probability: 'probabilitati',
  geometry: 'geometrie', function: 'functii',
};

const MASTERY_CONFIG = {
  master: { emoji: '🏆', color: DUO.green, label: 'Maestru' },
  good: { emoji: '✅', color: DUO.blue, label: 'Bun' },
  learning: { emoji: '📖', color: DUO.yellow, label: 'In curs' },
  weak: { emoji: '⚠️', color: DUO.orange, label: 'Slab' },
  new: { emoji: '🆕', color: DUO.textMuted, label: 'Nou' },
};

export default function StudyPlanScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [masteries, setMasteries] = useState<TopicMastery[]>([]);
  const [sessions, setSessions] = useState<StudySession[]>([]);
  const [overallMastery, setOverallMastery] = useState(0);
  const [studyStreak, setStudyStreak] = useState(0);
  const [daysUntilBAC, setDaysUntilBAC] = useState(0);

  useEffect(() => {
    setDaysUntilBAC(Math.max(0, Math.ceil(
      (new Date('2026-07-01').getTime() - Date.now()) / 86400000
    )));
  }, []);

  useEffect(() => {
    if (!user?.id) return;
    fetchStudyPlan();
  }, [user?.id]);

  const fetchStudyPlan = async () => {
    try {
      // Fetch stats and insights
      const [stats, insights, gamification] = await Promise.all([
        apiGet<any>(`/api/stats/detailed?user_id=${user?.id}`).catch(() => null),
        apiGet<any>(`/api/ml/insights?user_id=${user?.id}`).catch(() => null),
        apiGet<any>(`/api/gamification/stats?user_id=${user?.id}`).catch(() => null),
      ]);

      if (gamification?.success) {
        setStudyStreak(gamification.current_streak || 0);
      }

      // Build topic mastery from detailed stats
      const topicStats: Record<string, { correct: number; total: number }> = {};

      if (stats?.topics) {
        for (const [topic, data] of Object.entries(stats.topics as Record<string, any>)) {
          const key = TOPIC_ALIASES[topic] || topic;
          topicStats[key] = {
            correct: (topicStats[key]?.correct || 0) + (data.correct || 0),
            total: (topicStats[key]?.total || 0) + (data.attempts || 0),
          };
        }
      }

      // Build mastery list
      const allTopics = new Set([
        ...Object.keys(topicStats),
        ...Object.keys(TOPIC_NAMES),
      ]);

      const masteryList: TopicMastery[] = [];
      let totalAcc = 0;
      let accCount = 0;

      for (const topic of allTopics) {
        const name = TOPIC_NAMES[topic];
        if (!name) continue;

        const s = topicStats[topic];
        const accuracy = s && s.total > 0 ? Math.round((s.correct / s.total) * 100) : 0;
        const attempts = s?.total || 0;

        let mastery: TopicMastery['mastery'] = 'new';
        if (attempts === 0) mastery = 'new';
        else if (accuracy >= 85) mastery = 'master';
        else if (accuracy >= 70) mastery = 'good';
        else if (accuracy >= 50) mastery = 'learning';
        else mastery = 'weak';

        masteryList.push({
          topic,
          topicName: name,
          accuracy,
          attempts,
          mastery,
          emoji: MASTERY_CONFIG[mastery].emoji,
        });

        if (attempts > 0) {
          totalAcc += accuracy;
          accCount++;
        }
      }

      // Sort: weak first, then learning, then new, then good, then master
      const order = { weak: 0, learning: 1, new: 2, good: 3, master: 4 };
      masteryList.sort((a, b) => order[a.mastery] - order[b.mastery]);

      setMasteries(masteryList);
      setOverallMastery(accCount > 0 ? Math.round(totalAcc / accCount) : 0);

      // Generate study sessions based on weaknesses
      const generatedSessions: StudySession[] = [];
      let sessionId = 1;

      // Priority 1: Weak topics — review
      for (const m of masteryList.filter(m => m.mastery === 'weak')) {
        generatedSessions.push({
          id: sessionId++,
          title: `Recapitulare: ${m.topicName}`,
          description: `Acuratete ${m.accuracy}% — necesita practica suplimentara`,
          topic: m.topic,
          duration: 15,
          type: 'review',
          emoji: '🔄',
          color: DUO.orange,
        });
      }

      // Priority 2: Learning topics — practice
      for (const m of masteryList.filter(m => m.mastery === 'learning').slice(0, 3)) {
        generatedSessions.push({
          id: sessionId++,
          title: `Practica: ${m.topicName}`,
          description: `Acuratete ${m.accuracy}% — aproape acolo!`,
          topic: m.topic,
          duration: 10,
          type: 'practice',
          emoji: '💪',
          color: DUO.blue,
        });
      }

      // Priority 3: New topics — theory
      for (const m of masteryList.filter(m => m.mastery === 'new').slice(0, 2)) {
        generatedSessions.push({
          id: sessionId++,
          title: `Invata: ${m.topicName}`,
          description: 'Incepe cu teoria si formule de baza',
          topic: m.topic,
          duration: 20,
          type: 'theory',
          emoji: '📚',
          color: DUO.purple,
        });
      }

      // Priority 4: Challenge for good topics
      for (const m of masteryList.filter(m => m.mastery === 'good').slice(0, 2)) {
        generatedSessions.push({
          id: sessionId++,
          title: `Challenge: ${m.topicName}`,
          description: `Exercitii dificile pentru a ajunge la maestru`,
          topic: m.topic,
          duration: 10,
          type: 'challenge',
          emoji: '🎯',
          color: DUO.green,
        });
      }

      // If no sessions generated, add defaults
      if (generatedSessions.length === 0) {
        generatedSessions.push(
          { id: 1, title: 'Incepe cu Ecuatii', description: 'Ecuatii de baza clasa 9', topic: 'ecuatii', duration: 15, type: 'theory', emoji: '📚', color: DUO.purple },
          { id: 2, title: 'Practica Derivate', description: 'Derivate functii elementare', topic: 'derivate', duration: 10, type: 'practice', emoji: '💪', color: DUO.blue },
          { id: 3, title: 'Invata Matrice', description: 'Operatii cu matrice', topic: 'matrice', duration: 20, type: 'theory', emoji: '📚', color: DUO.purple },
        );
      }

      setSessions(generatedSessions);
    } catch (e) {
      console.log('StudyPlan error:', e);
      // Fallback sessions
      setSessions([
        { id: 1, title: 'Rezolva 5 ecuatii', description: 'Practica zilnica', topic: 'ecuatii', duration: 10, type: 'practice', emoji: '💪', color: DUO.blue },
        { id: 2, title: 'Recapitulare Derivate', description: 'Reguli de derivare', topic: 'derivate', duration: 15, type: 'review', emoji: '🔄', color: DUO.orange },
      ]);
    }
    setLoading(false);
  };

  const totalStudyTime = sessions.reduce((s, x) => s + x.duration, 0);
  const weakCount = masteries.filter(m => m.mastery === 'weak').length;
  const masterCount = masteries.filter(m => m.mastery === 'master').length;

  if (loading) {
    return (
      <View style={[styles.container, { paddingTop: insets.top }]}>
        <ActivityIndicator size="large" color={DUO.green} style={{ marginTop: 100 }} />
        <Text style={styles.loadingText}>Se genereaza planul de studiu...</Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <LinearGradient colors={[DUO.card, DUO.bg]} style={styles.header}>
        <Text style={styles.headerEmoji}>🗺️</Text>
        <View>
          <Text style={[TYPO.heading3, { color: DUO.textPrimary }]}>Plan de Studiu AI</Text>
          <Text style={[TYPO.label, { color: DUO.textSecondary }]}>Personalizat pe punctele tale slabe</Text>
        </View>
      </LinearGradient>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentInner}>
        {/* Hero Stats */}
        <Animated.View entering={FadeInDown.duration(400)} style={styles.heroRow}>
          <View style={styles.heroCard}>
            <ProgressRing progress={overallMastery / 100} size={64} strokeWidth={5} color={DUO.green}>
              <Text style={styles.heroValue}>{overallMastery}%</Text>
            </ProgressRing>
            <Text style={styles.heroLabel}>Maestrie</Text>
          </View>
          <View style={styles.heroCard}>
            <Text style={styles.heroEmoji}>📅</Text>
            <Text style={styles.heroValue}>{daysUntilBAC}</Text>
            <Text style={styles.heroLabel}>Zile pana la BAC</Text>
          </View>
          <View style={styles.heroCard}>
            <Text style={styles.heroEmoji}>⏱️</Text>
            <Text style={styles.heroValue}>{totalStudyTime}m</Text>
            <Text style={styles.heroLabel}>Plan azi</Text>
          </View>
        </Animated.View>

        {/* AI Recommendations */}
        {weakCount > 0 && (
          <Animated.View entering={FadeInDown.delay(100).duration(400)} style={styles.aiCard}>
            <Text style={styles.aiIcon}>🤖</Text>
            <View style={{ flex: 1 }}>
              <Text style={styles.aiTitle}>Recomandare AI</Text>
              <Text style={styles.aiText}>
                Ai {weakCount} {weakCount === 1 ? 'topic slab' : 'topicuri slabe'} care necesita atentie.
                {masterCount > 0 ? ` Felicitari pentru ${masterCount} topicuri stapanite!` : ''}
                {' '}Concentreaza-te pe sesiunile de mai jos.
              </Text>
            </View>
          </Animated.View>
        )}

        {/* Today's Sessions */}
        <Text style={styles.sectionTitle}>SESIUNI RECOMANDATE</Text>
        {sessions.map((session, i) => (
          <Animated.View key={session.id} entering={FadeInDown.delay(150 + i * 80).duration(400)}>
            <AnimatedPressable
              style={styles.sessionCard}
              onPress={() => router.push('/(tabs)/exercises' as any)}
            >
              <View style={[styles.sessionIcon, { backgroundColor: session.color + '20' }]}>
                <Text style={styles.sessionEmoji}>{session.emoji}</Text>
              </View>
              <View style={styles.sessionInfo}>
                <Text style={styles.sessionTitle}>{session.title}</Text>
                <Text style={styles.sessionDesc}>{session.description}</Text>
                <View style={styles.sessionMeta}>
                  <Text style={[styles.sessionDuration, { color: session.color }]}>
                    {session.duration} min
                  </Text>
                  <View style={[styles.sessionTypeBadge, { backgroundColor: session.color + '15' }]}>
                    <Text style={[styles.sessionTypeText, { color: session.color }]}>
                      {session.type === 'review' ? 'Recapitulare' :
                       session.type === 'practice' ? 'Practica' :
                       session.type === 'challenge' ? 'Challenge' : 'Teorie'}
                    </Text>
                  </View>
                </View>
              </View>
              <Text style={styles.sessionArrow}>›</Text>
            </AnimatedPressable>
          </Animated.View>
        ))}

        {/* Topic Mastery Grid */}
        <Text style={styles.sectionTitle}>MAESTRIE PE TOPICURI</Text>
        <View style={styles.masteryGrid}>
          {masteries.slice(0, 12).map((m, i) => (
            <Animated.View
              key={m.topic}
              entering={FadeInDown.delay(300 + i * 50).duration(300)}
              style={[styles.masteryCard, { borderColor: MASTERY_CONFIG[m.mastery].color + '30' }]}
            >
              <Text style={styles.masteryEmoji}>{m.emoji}</Text>
              <Text style={styles.masteryName} numberOfLines={1}>{m.topicName}</Text>
              <Text style={[styles.masteryAcc, { color: MASTERY_CONFIG[m.mastery].color }]}>
                {m.attempts > 0 ? `${m.accuracy}%` : '—'}
              </Text>
              <View style={styles.masteryBar}>
                <View style={[styles.masteryBarFill, {
                  width: `${Math.max(m.accuracy, 5)}%`,
                  backgroundColor: MASTERY_CONFIG[m.mastery].color,
                }]} />
              </View>
            </Animated.View>
          ))}
        </View>

        {/* Legend */}
        <View style={styles.legend}>
          {Object.entries(MASTERY_CONFIG).map(([key, cfg]) => (
            <View key={key} style={styles.legendItem}>
              <Text style={styles.legendEmoji}>{cfg.emoji}</Text>
              <Text style={[styles.legendLabel, { color: cfg.color }]}>{cfg.label}</Text>
            </View>
          ))}
        </View>

        <View style={{ height: 100 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  header: {
    flexDirection: 'row', alignItems: 'center', paddingBottom: 14,
    paddingHorizontal: 20, gap: 12, borderBottomWidth: 1, borderBottomColor: DUO.surface,
  },
  headerEmoji: { fontSize: 32 },
  content: { flex: 1 },
  contentInner: { padding: 20, gap: 16 },
  loadingText: { color: DUO.textSecondary, textAlign: 'center', marginTop: 16, fontSize: 14, fontWeight: '600' },

  heroRow: { flexDirection: 'row', gap: 10 },
  heroCard: {
    flex: 1, backgroundColor: DUO.card, borderRadius: 16, padding: 14,
    alignItems: 'center', gap: 6, borderWidth: 1, borderColor: DUO.surface,
  },
  heroEmoji: { fontSize: 28 },
  heroValue: { fontSize: 20, fontWeight: '900', color: DUO.textPrimary },
  heroLabel: { fontSize: 10, fontWeight: '700', color: DUO.textMuted, textTransform: 'uppercase', letterSpacing: 0.5 },

  aiCard: {
    flexDirection: 'row', backgroundColor: DUO.green + '10', borderRadius: 16,
    padding: 16, gap: 12, borderWidth: 1, borderColor: DUO.green + '25', alignItems: 'flex-start',
  },
  aiIcon: { fontSize: 24 },
  aiTitle: { fontSize: 14, fontWeight: '800', color: DUO.green, marginBottom: 4 },
  aiText: { fontSize: 13, fontWeight: '500', color: DUO.textSecondary, lineHeight: 19 },

  sectionTitle: { fontSize: 12, fontWeight: '800', color: DUO.textMuted, letterSpacing: 1.5, marginTop: 8 },

  sessionCard: {
    flexDirection: 'row', backgroundColor: DUO.card, borderRadius: 16,
    padding: 16, alignItems: 'center', gap: 14, borderWidth: 1, borderColor: DUO.surface,
  },
  sessionIcon: { width: 48, height: 48, borderRadius: 14, justifyContent: 'center', alignItems: 'center' },
  sessionEmoji: { fontSize: 22 },
  sessionInfo: { flex: 1, gap: 4 },
  sessionTitle: { fontSize: 15, fontWeight: '800', color: DUO.textPrimary },
  sessionDesc: { fontSize: 12, fontWeight: '500', color: DUO.textSecondary },
  sessionMeta: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 2 },
  sessionDuration: { fontSize: 12, fontWeight: '800' },
  sessionTypeBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 999 },
  sessionTypeText: { fontSize: 10, fontWeight: '800' },
  sessionArrow: { fontSize: 24, fontWeight: '300', color: DUO.textMuted },

  masteryGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  masteryCard: {
    width: '31%' as any, backgroundColor: DUO.card, borderRadius: 12,
    padding: 12, alignItems: 'center', gap: 4, borderWidth: 1,
  },
  masteryEmoji: { fontSize: 20 },
  masteryName: { fontSize: 11, fontWeight: '700', color: DUO.textPrimary, textAlign: 'center' },
  masteryAcc: { fontSize: 16, fontWeight: '900' },
  masteryBar: { width: '100%', height: 4, backgroundColor: DUO.surface, borderRadius: 2, overflow: 'hidden' },
  masteryBarFill: { height: '100%', borderRadius: 2 },

  legend: { flexDirection: 'row', justifyContent: 'center', gap: 12, flexWrap: 'wrap' },
  legendItem: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  legendEmoji: { fontSize: 14 },
  legendLabel: { fontSize: 11, fontWeight: '700' },
});
