import { useState, useEffect, useRef } from 'react';
import { StyleSheet, View, Text, ScrollView, Animated as RNAnimated } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Animated, { FadeInDown, FadeInUp, FadeIn } from 'react-native-reanimated';
import { Ionicons } from '@expo/vector-icons';
import { apiGet } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import ProgressRing from '@/components/ProgressRing';
import { StatsCardSkeleton } from '@/components/Skeleton';

interface PredictionData {
  predicted_grade: number;
  confidence_interval: number[];
  confidence_level: string;
  total_attempts: number;
  breakdown: Record<string, { accuracy: number; estimated_points: number; max_points: number; exercises_solved: number }>;
  insights: { type: string; message: string }[];
}

const GRADE_CFG: Record<string, { icon: keyof typeof Ionicons.glyphMap; title: string; sub: string; colors: [string, string] }> = {
  excellent: { icon: 'trophy', title: 'Excelent!', sub: 'Ești pregătit pentru nota maximă!', colors: ['#FBBF24', '#F59E0B'] },
  great: { icon: 'rocket', title: 'Foarte bine!', sub: 'Continuă tot așa!', colors: ['#34D399', '#06B6D4'] },
  good: { icon: 'fitness', title: 'Bine!', sub: 'Încă puțin efort și vei excela!', colors: ['#60A5FA', '#8B5CF6'] },
  ok: { icon: 'book', title: 'Poți mai mult!', sub: 'Focus pe subiectele slabe.', colors: ['#FB923C', '#FBBF24'] },
  low: { icon: 'disc', title: 'Hai la treabă!', sub: 'Exercițiu constant = progres.', colors: ['#F87171', '#FB923C'] },
};

function getGradeLevel(g: number) {
  if (g >= 9) return 'excellent';
  if (g >= 7.5) return 'great';
  if (g >= 6) return 'good';
  if (g >= 5) return 'ok';
  return 'low';
}
function getGradeColor(g: number) {
  if (g >= 9) return '#FBBF24';
  if (g >= 7.5) return DUO.green;
  if (g >= 6) return DUO.blue;
  if (g >= 5) return DUO.orange;
  return DUO.red;
}

const INSIGHT_ICONS: Record<string, keyof typeof Ionicons.glyphMap> = { positive: 'checkmark-circle', warning: 'alert-circle', focus: 'scan', tip: 'star' };
const INSIGHT_COLORS: Record<string, string> = { positive: '#34D399', warning: '#F87171', focus: '#FB923C', tip: '#60A5FA' };
const SUBJ = ['', 'Subiectul I', 'Subiectul II', 'Subiectul III'];
const SUBJ_DESC = ['', '30 puncte · Multiple choice', '30 puncte · Probleme', '30 puncte · Analiză'];
const SUBJ_COLORS = ['', '#34D399', '#60A5FA', '#A78BFA'];

export default function AnalyticsScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [prediction, setPrediction] = useState<PredictionData | null>(null);
  const pulseAnim = useRef(new RNAnimated.Value(1)).current;

  useEffect(() => {
    if (!user?.id) return;
    fetchAll();
  }, [user?.id]);

  useEffect(() => {
    if (!prediction) return;
    RNAnimated.loop(RNAnimated.sequence([
      RNAnimated.timing(pulseAnim, { toValue: 1.04, duration: 2200, useNativeDriver: true }),
      RNAnimated.timing(pulseAnim, { toValue: 1, duration: 2200, useNativeDriver: true }),
    ])).start();
  }, [prediction]);

  const fetchAll = async () => {
    try {
      const predData = await apiGet<any>(`/api/ml/predict-grade?user_id=${user?.id}`);
      if (predData.success && predData.prediction) setPrediction(predData.prediction);
    } catch (e) { console.log(e); }
    setLoading(false);
  };

  if (loading) return (
    <View style={[styles.container, { paddingTop: insets.top + 40 }]}>
      <StatsCardSkeleton /><StatsCardSkeleton />
    </View>
  );

  const grade = prediction?.predicted_grade || 0;
  const lvl = getGradeLevel(grade);
  const color = getGradeColor(grade);
  const cfg = GRADE_CFG[lvl];
  const conf = prediction?.confidence_interval;
  const confLvl = prediction?.confidence_level;
  const levelColor = confLvl === 'high' || confLvl === 'very_high' ? DUO.green :
    confLvl === 'medium' ? DUO.yellow : DUO.orange;

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 100 }}>

      {/* ─── HERO ─── */}
      {prediction ? (
        <View style={[styles.hero, { paddingTop: insets.top + 12 }]}>
          <LinearGradient
            colors={[cfg.colors[0] + '12', cfg.colors[1] + '08', 'transparent']}
            style={StyleSheet.absoluteFill}
          />

          <Animated.View entering={FadeInDown.delay(100).springify()}>
            <Text style={styles.pageLabel}>PREDICȚIE BAC</Text>
          </Animated.View>

          <Animated.View entering={FadeInDown.delay(200).springify()} style={styles.ringWrap}>
            <RNAnimated.View style={{ transform: [{ scale: pulseAnim }] }}>
              <ProgressRing progress={grade / 10} size={170} strokeWidth={14} color={color}>
                <Text style={[styles.gradeNum, { color }]}>{grade.toFixed(1)}</Text>
                <Text style={styles.gradeOf}>din 10</Text>
              </ProgressRing>
            </RNAnimated.View>
          </Animated.View>

          <Animated.View entering={FadeInDown.delay(300).springify()} style={styles.heroMeta}>
            <Text style={styles.heroTitle}>{cfg.title}</Text>
            <Text style={styles.heroSub}>{cfg.sub}</Text>
          </Animated.View>

          {conf && (
            <Animated.View entering={FadeIn.delay(500)} style={styles.confRow}>
              <View style={[styles.confChip, { borderColor: color + '35' }]}>
                <Text style={styles.confChipLabel}>MIN</Text>
                <Text style={[styles.confChipVal, { color }]}>{conf[0].toFixed(1)}</Text>
              </View>
              <View style={[styles.confDash, { backgroundColor: color + '30' }]} />
              <View style={[styles.confChip, { borderColor: color + '35' }]}>
                <Text style={styles.confChipLabel}>MAX</Text>
                <Text style={[styles.confChipVal, { color }]}>{conf[1].toFixed(1)}</Text>
              </View>
            </Animated.View>
          )}
        </View>
      ) : (
        <View style={[styles.hero, { paddingTop: insets.top + 40 }]}>
          <Text style={styles.pageLabel}>PREDICȚIE BAC</Text>
          <Ionicons name="stats-chart" size={56} color={DUO.textMuted} style={{ marginVertical: 20 }} />
          <Text style={styles.heroTitle}>Predicție Notă</Text>
          <Text style={styles.heroSub}>Rezolvă minim 10 exerciții pentru predicție</Text>
        </View>
      )}

      {/* ─── SUBJECTS ─── */}
      {prediction?.breakdown && Object.keys(prediction.breakdown).length > 0 && (
        <Animated.View entering={FadeInUp.delay(500).springify()} style={styles.section}>
          <Text style={styles.sectionTitle}>Performanță pe subiecte</Text>
          {[1, 2, 3].map((subj, idx) => {
            const key = `subject_${subj}`;
            const data = prediction.breakdown[key];
            if (!data) return null;
            const pct = data.accuracy;
            const sc = SUBJ_COLORS[subj];
            return (
              <Animated.View key={subj} entering={FadeInUp.delay(550 + idx * 80).springify()}>
                <View style={styles.subjCard}>
                  <View style={styles.subjLeft}>
                    <View style={[styles.subjDot, { backgroundColor: sc }]} />
                    <View>
                      <Text style={styles.subjName}>{SUBJ[subj]}</Text>
                      <Text style={styles.subjDesc}>{SUBJ_DESC[subj]}</Text>
                    </View>
                  </View>
                  <Text style={[styles.subjPts, { color: sc }]}>
                    {data.estimated_points.toFixed(0)}<Text style={styles.subjPtsMax}>/{data.max_points}</Text>
                  </Text>
                </View>
                <View style={styles.barOuter}>
                  <LinearGradient
                    colors={[sc, sc + '70']}
                    start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
                    style={[styles.barInner, { width: `${Math.min(pct, 100)}%` }]}
                  />
                </View>
                <View style={styles.subjFooter}>
                  <Text style={styles.subjFooterText}>{pct.toFixed(0)}% acuratețe</Text>
                  <Text style={styles.subjFooterText}>{data.exercises_solved} exerciții</Text>
                </View>
              </Animated.View>
            );
          })}
        </Animated.View>
      )}

      {/* ─── INSIGHTS ─── */}
      {prediction?.insights && prediction.insights.length > 0 && (
        <Animated.View entering={FadeInUp.delay(700).springify()} style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Recomandări</Text>
            <View style={styles.aiBadge}>
              <Text style={styles.aiBadgeText}>AI</Text>
            </View>
          </View>
          {prediction.insights.map((ins, i) => {
            const ic = INSIGHT_COLORS[ins.type] || DUO.blue;
            return (
              <Animated.View key={i} entering={FadeInUp.delay(750 + i * 60).springify()}>
                <View style={styles.insightCard}>
                  <View style={[styles.insightBullet, { backgroundColor: ic + '18' }]}>
                    <Ionicons name={INSIGHT_ICONS[ins.type] || 'star'} size={16} color={ic} />
                  </View>
                  <Text style={styles.insightMsg}>{ins.message}</Text>
                </View>
              </Animated.View>
            );
          })}
        </Animated.View>
      )}

      {/* ─── MODEL INFO ─── */}
      {prediction && (
        <Animated.View entering={FadeInUp.delay(900).springify()} style={styles.modelCard}>
          <View style={styles.modelRow}>
            <Text style={styles.modelLabel}>Model</Text>
            <Text style={styles.modelVal}>ML Ensemble</Text>
          </View>
          <View style={styles.modelDivider} />
          <View style={styles.modelRow}>
            <Text style={styles.modelLabel}>Încredere</Text>
            <View style={[styles.levelPill, { backgroundColor: levelColor + '15' }]}>
              <Text style={[styles.levelText, { color: levelColor }]}>
                {confLvl === 'very_high' ? 'Foarte ridicată' : confLvl === 'high' ? 'Ridicată' :
                  confLvl === 'medium' ? 'Medie' : 'Scăzută'}
              </Text>
            </View>
          </View>
          <View style={styles.modelDivider} />
          <View style={styles.modelRow}>
            <Text style={styles.modelLabel}>Date analizate</Text>
            <Text style={styles.modelVal}>{prediction.total_attempts} exerciții</Text>
          </View>
        </Animated.View>
      )}

    </ScrollView>
  );
}

const F = DUO;

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: F.bg },

  // Hero
  hero: { alignItems: 'center', paddingBottom: 28, paddingHorizontal: 24 },
  pageLabel: {
    fontSize: 11, fontFamily: F.fontBold, letterSpacing: 2.5,
    color: F.textMuted, marginBottom: 16,
  },
  ringWrap: { marginBottom: 24 },
  gradeNum: { fontSize: 52, fontFamily: F.fontBlack, letterSpacing: -2 },
  gradeOf: { fontSize: 13, fontFamily: F.fontSemiBold, color: F.textMuted, marginTop: -4 },
  heroMeta: { alignItems: 'center', marginBottom: 20 },
  heroTitle: { fontSize: 24, fontFamily: F.fontBlack, color: F.textPrimary, letterSpacing: -0.5 },
  heroSub: { fontSize: 14, fontFamily: F.fontMedium, color: F.textSecondary, marginTop: 6, textAlign: 'center' },

  // Confidence chips
  confRow: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  confChip: {
    paddingHorizontal: 18, paddingVertical: 10, borderRadius: 12,
    borderWidth: 1, backgroundColor: F.card, alignItems: 'center',
  },
  confChipLabel: { fontSize: 9, fontFamily: F.fontBold, color: F.textMuted, letterSpacing: 1.5, marginBottom: 2 },
  confChipVal: { fontSize: 20, fontFamily: F.fontBlack },
  confDash: { width: 20, height: 2, borderRadius: 1 },

  // Sections
  section: {
    marginHorizontal: 16, marginTop: 20, backgroundColor: F.card,
    borderRadius: F.radiusLg, padding: 20,
    borderWidth: 1, borderColor: F.surface + '60',
  },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 },
  sectionTitle: { fontSize: 16, fontFamily: F.fontBold, color: F.textPrimary, marginBottom: 18, letterSpacing: -0.2 },

  // Subjects
  subjCard: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  subjLeft: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  subjDot: { width: 10, height: 10, borderRadius: 5 },
  subjName: { fontSize: 14, fontFamily: F.fontBold, color: F.textPrimary },
  subjDesc: { fontSize: 11, fontFamily: F.fontMedium, color: F.textMuted, marginTop: 1 },
  subjPts: { fontSize: 22, fontFamily: F.fontBlack },
  subjPtsMax: { fontSize: 14, fontFamily: F.fontSemiBold, color: F.textMuted },
  barOuter: { height: 6, backgroundColor: F.surface + '80', borderRadius: 3, overflow: 'hidden', marginTop: 4 },
  barInner: { height: '100%', borderRadius: 3 },
  subjFooter: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 6, marginBottom: 20 },
  subjFooterText: { fontSize: 11, fontFamily: F.fontMedium, color: F.textMuted },

  // AI badge
  aiBadge: { backgroundColor: F.purple + '18', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8 },
  aiBadgeText: { fontSize: 10, fontFamily: F.fontBlack, color: F.purple, letterSpacing: 1 },

  // Insights
  insightCard: { flexDirection: 'row', alignItems: 'flex-start', marginBottom: 16 },
  insightBullet: {
    width: 36, height: 36, borderRadius: 10,
    justifyContent: 'center', alignItems: 'center', marginRight: 14,
  },
  insightMsg: { flex: 1, fontSize: 14, fontFamily: F.fontMedium, color: F.textPrimary, lineHeight: 21 },

  // Model info
  modelCard: {
    marginHorizontal: 16, marginTop: 20, padding: 18,
    backgroundColor: F.card, borderRadius: F.radiusLg,
    borderWidth: 1, borderColor: F.surface + '60',
  },
  modelRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingVertical: 8 },
  modelLabel: { fontSize: 13, fontFamily: F.fontMedium, color: F.textMuted },
  modelVal: { fontSize: 13, fontFamily: F.fontBold, color: F.textPrimary },
  modelDivider: { height: 1, backgroundColor: F.surface + '50', marginVertical: 2 },
  levelPill: { paddingHorizontal: 12, paddingVertical: 5, borderRadius: 8 },
  levelText: { fontSize: 12, fontFamily: F.fontBold },
});
