import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, ScrollView, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

const screenWidth = Dimensions.get('window').width;

interface Stats {
  total_attempts: number;
  correct_answers: number;
  accuracy: number;
}

interface SubjectStats {
  subject: number;
  total: number;
  correct: number;
  accuracy: number;
}

interface TopicStats {
  topic: string;
  total: number;
  correct: number;
  accuracy: number;
}

interface DifficultyStats {
  difficulty: number;
  total: number;
  correct: number;
  accuracy: number;
}

export default function AnalyticsScreen() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [subjectStats, setSubjectStats] = useState<SubjectStats[]>([]);
  const [topicStats, setTopicStats] = useState<TopicStats[]>([]);
  const [difficultyStats, setDifficultyStats] = useState<DifficultyStats[]>([]);
  const [recentActivity, setRecentActivity] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [prediction, setPrediction] = useState<number | null>(null);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      // Fetch basic stats
      const statsRes = await fetch('http://localhost:5000/api/stats');
      const statsData = await statsRes.json();
      setStats(statsData);

      // Fetch detailed analytics
      const analyticsRes = await fetch('http://localhost:5000/api/analytics/detailed');
      const analyticsData = await analyticsRes.json();

      if (analyticsData.success) {
        setSubjectStats(analyticsData.by_subject || []);
        setTopicStats(analyticsData.by_topic || []);
        setDifficultyStats(analyticsData.by_difficulty || []);
        setRecentActivity(analyticsData.recent_activity || []);
      }

      // Fetch prediction
      const predRes = await fetch('http://localhost:5000/api/ml/predict-grade');
      const predData = await predRes.json();
      if (predData.predicted_grade) {
        setPrediction(predData.predicted_grade);
      }
    } catch (error) {
      console.log('Error fetching analytics:', error);
    }
    setLoading(false);
  };

  const getAccuracyColor = (accuracy: number) => {
    if (accuracy >= 80) return '#10b981';
    if (accuracy >= 60) return '#f59e0b';
    if (accuracy >= 40) return '#f97316';
    return '#ef4444';
  };

  const getGradeColor = (grade: number): [string, string] => {
    if (grade >= 9) return ['#10b981', '#059669'];
    if (grade >= 7) return ['#f59e0b', '#d97706'];
    if (grade >= 5) return ['#f97316', '#ea580c'];
    return ['#ef4444', '#dc2626'];
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Se încarcă analizele...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <LinearGradient
        colors={['#3b82f6', '#1d4ed8']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <Text style={styles.headerTitle}>📊 Analytics</Text>
        <Text style={styles.headerSubtitle}>Analizează-ți progresul</Text>
      </LinearGradient>

      {/* Prediction Card */}
      {prediction && (
        <View style={styles.predictionCard}>
          <LinearGradient
            colors={getGradeColor(prediction)}
            style={styles.predictionGradient}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
          >
            <Text style={styles.predictionLabel}>Predicție Notă BAC</Text>
            <Text style={styles.predictionValue}>{prediction.toFixed(2)}</Text>
            <Text style={styles.predictionHint}>Bazat pe performanța ta actuală</Text>
          </LinearGradient>
        </View>
      )}

      {/* Overview Stats */}
      <View style={styles.overviewCard}>
        <Text style={styles.cardTitle}>Sumar General</Text>
        <View style={styles.overviewGrid}>
          <View style={styles.overviewItem}>
            <Text style={styles.overviewValue}>{stats?.total_attempts || 0}</Text>
            <Text style={styles.overviewLabel}>Exerciții</Text>
          </View>
          <View style={styles.overviewItem}>
            <Text style={styles.overviewValue}>{stats?.correct_answers || 0}</Text>
            <Text style={styles.overviewLabel}>Corecte</Text>
          </View>
          <View style={styles.overviewItem}>
            <Text style={[styles.overviewValue, { color: getAccuracyColor(stats?.accuracy || 0) }]}>
              {stats?.accuracy || 0}%
            </Text>
            <Text style={styles.overviewLabel}>Acuratețe</Text>
          </View>
        </View>
      </View>

      {/* Subject Performance */}
      <View style={styles.sectionCard}>
        <Text style={styles.cardTitle}>Performanță pe Subiecte</Text>
        {[1, 2, 3].map((subj) => {
          const subjData = subjectStats.find(s => s.subject === subj);
          const accuracy = subjData?.accuracy || 0;
          const total = subjData?.total || 0;
          const correct = subjData?.correct || 0;

          return (
            <View key={subj} style={styles.barRow}>
              <View style={styles.barLabel}>
                <Text style={styles.barLabelText}>Subiectul {subj}</Text>
                <Text style={styles.barLabelStats}>{correct}/{total}</Text>
              </View>
              <View style={styles.barContainer}>
                <View
                  style={[
                    styles.bar,
                    {
                      width: `${Math.min(accuracy, 100)}%`,
                      backgroundColor: getAccuracyColor(accuracy),
                    },
                  ]}
                />
              </View>
              <Text style={[styles.barValue, { color: getAccuracyColor(accuracy) }]}>
                {accuracy.toFixed(0)}%
              </Text>
            </View>
          );
        })}
      </View>

      {/* Difficulty Performance */}
      <View style={styles.sectionCard}>
        <Text style={styles.cardTitle}>Performanță pe Dificultate</Text>
        {[1, 2, 3, 4].map((diff) => {
          const diffData = difficultyStats.find(d => d.difficulty === diff);
          const accuracy = diffData?.accuracy || 0;
          const total = diffData?.total || 0;

          const diffLabels = ['', 'Ușor', 'Mediu', 'Dificil', 'Expert'];
          const diffEmojis = ['', '🟢', '🟡', '🟠', '🔴'];

          return (
            <View key={diff} style={styles.barRow}>
              <View style={styles.barLabel}>
                <Text style={styles.barLabelText}>
                  {diffEmojis[diff]} {diffLabels[diff]}
                </Text>
                <Text style={styles.barLabelStats}>{total} ex.</Text>
              </View>
              <View style={styles.barContainer}>
                <View
                  style={[
                    styles.bar,
                    {
                      width: `${Math.min(accuracy, 100)}%`,
                      backgroundColor: getAccuracyColor(accuracy),
                    },
                  ]}
                />
              </View>
              <Text style={[styles.barValue, { color: getAccuracyColor(accuracy) }]}>
                {total > 0 ? `${accuracy.toFixed(0)}%` : '-'}
              </Text>
            </View>
          );
        })}
      </View>

      {/* Topic Heatmap */}
      <View style={styles.sectionCard}>
        <Text style={styles.cardTitle}>Heatmap Topicuri</Text>
        <Text style={styles.cardSubtitle}>Culorile arată punctele forte și slabe</Text>
        <View style={styles.heatmapGrid}>
          {topicStats.slice(0, 12).map((topic, index) => (
            <View
              key={index}
              style={[
                styles.heatmapCell,
                { backgroundColor: getAccuracyColor(topic.accuracy) + '30' },
              ]}
            >
              <Text style={styles.heatmapEmoji}>
                {topic.accuracy >= 80 ? '💪' : topic.accuracy >= 50 ? '📚' : '🎯'}
              </Text>
              <Text style={styles.heatmapTopic} numberOfLines={2}>
                {topic.topic}
              </Text>
              <Text style={[styles.heatmapAccuracy, { color: getAccuracyColor(topic.accuracy) }]}>
                {topic.accuracy.toFixed(0)}%
              </Text>
            </View>
          ))}
        </View>

        {topicStats.length === 0 && (
          <View style={styles.emptyState}>
            <Text style={styles.emptyStateEmoji}>📝</Text>
            <Text style={styles.emptyStateText}>
              Rezolvă mai multe exerciții pentru a vedea analiza pe topicuri
            </Text>
          </View>
        )}
      </View>

      {/* Activity Chart (Simple) */}
      <View style={styles.sectionCard}>
        <Text style={styles.cardTitle}>Activitate Recentă</Text>
        <Text style={styles.cardSubtitle}>Ultimele 7 zile</Text>
        <View style={styles.activityChart}>
          {(recentActivity.length > 0 ? recentActivity : [0, 0, 0, 0, 0, 0, 0]).map((count, index) => {
            const maxCount = Math.max(...recentActivity, 1);
            const height = (count / maxCount) * 100;
            const days = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];

            return (
              <View key={index} style={styles.activityBarWrapper}>
                <View style={styles.activityBarContainer}>
                  <View
                    style={[
                      styles.activityBar,
                      {
                        height: `${Math.max(height, 5)}%`,
                        backgroundColor: count > 0 ? '#3b82f6' : '#e5e7eb',
                      },
                    ]}
                  />
                </View>
                <Text style={styles.activityDay}>{days[index]}</Text>
                <Text style={styles.activityCount}>{count}</Text>
              </View>
            );
          })}
        </View>
      </View>

      {/* Tips Based on Performance */}
      <View style={styles.tipsCard}>
        <Text style={styles.cardTitle}>💡 Recomandări</Text>
        {stats && stats.accuracy < 50 && (
          <View style={styles.tipItem}>
            <Text style={styles.tipIcon}>📚</Text>
            <Text style={styles.tipText}>
              Acuratețea ta este sub 50%. Încearcă să revezi teoria înainte de a rezolva exerciții.
            </Text>
          </View>
        )}
        {stats && stats.accuracy >= 50 && stats.accuracy < 70 && (
          <View style={styles.tipItem}>
            <Text style={styles.tipIcon}>💪</Text>
            <Text style={styles.tipText}>
              Ești pe drumul cel bun! Concentrează-te pe subiectele cu acuratețe mai mică.
            </Text>
          </View>
        )}
        {stats && stats.accuracy >= 70 && (
          <View style={styles.tipItem}>
            <Text style={styles.tipIcon}>🚀</Text>
            <Text style={styles.tipText}>
              Excelent! Încearcă exerciții mai dificile pentru a te pregăti și mai bine.
            </Text>
          </View>
        )}
        {(!stats || stats.total_attempts < 10) && (
          <View style={styles.tipItem}>
            <Text style={styles.tipIcon}>🎯</Text>
            <Text style={styles.tipText}>
              Rezolvă mai multe exerciții pentru a primi recomandări personalizate.
            </Text>
          </View>
        )}
      </View>

      <View style={{ height: 100 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f7fa',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f7fa',
  },
  loadingText: {
    fontSize: 18,
    color: '#6b7280',
  },
  header: {
    paddingTop: 60,
    paddingBottom: 30,
    paddingHorizontal: 24,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: '800',
    color: 'white',
    marginBottom: 8,
  },
  headerSubtitle: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.9)',
  },
  predictionCard: {
    marginHorizontal: 20,
    marginTop: -20,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 5,
  },
  predictionGradient: {
    padding: 24,
    alignItems: 'center',
  },
  predictionLabel: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
    marginBottom: 8,
  },
  predictionValue: {
    fontSize: 48,
    fontWeight: '800',
    color: 'white',
  },
  predictionHint: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
    marginTop: 8,
  },
  overviewCard: {
    backgroundColor: 'white',
    marginHorizontal: 20,
    marginTop: 20,
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1f2937',
    marginBottom: 16,
  },
  cardSubtitle: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: -12,
    marginBottom: 16,
  },
  overviewGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  overviewItem: {
    alignItems: 'center',
  },
  overviewValue: {
    fontSize: 32,
    fontWeight: '800',
    color: '#1f2937',
  },
  overviewLabel: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 4,
  },
  sectionCard: {
    backgroundColor: 'white',
    marginHorizontal: 20,
    marginTop: 16,
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  barRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  barLabel: {
    width: 100,
  },
  barLabelText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#1f2937',
  },
  barLabelStats: {
    fontSize: 11,
    color: '#6b7280',
  },
  barContainer: {
    flex: 1,
    height: 12,
    backgroundColor: '#e5e7eb',
    borderRadius: 6,
    marginHorizontal: 12,
    overflow: 'hidden',
  },
  bar: {
    height: '100%',
    borderRadius: 6,
  },
  barValue: {
    width: 45,
    fontSize: 14,
    fontWeight: '700',
    textAlign: 'right',
  },
  heatmapGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  heatmapCell: {
    width: (screenWidth - 72) / 3,
    padding: 12,
    borderRadius: 12,
    alignItems: 'center',
  },
  heatmapEmoji: {
    fontSize: 20,
    marginBottom: 4,
  },
  heatmapTopic: {
    fontSize: 10,
    color: '#4b5563',
    textAlign: 'center',
    marginBottom: 4,
    height: 28,
  },
  heatmapAccuracy: {
    fontSize: 14,
    fontWeight: '700',
  },
  emptyState: {
    alignItems: 'center',
    padding: 20,
  },
  emptyStateEmoji: {
    fontSize: 40,
    marginBottom: 12,
  },
  emptyStateText: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
  },
  activityChart: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    height: 120,
    paddingTop: 20,
  },
  activityBarWrapper: {
    alignItems: 'center',
    flex: 1,
  },
  activityBarContainer: {
    width: 24,
    height: 80,
    backgroundColor: '#f3f4f6',
    borderRadius: 12,
    justifyContent: 'flex-end',
    overflow: 'hidden',
  },
  activityBar: {
    width: '100%',
    borderRadius: 12,
  },
  activityDay: {
    fontSize: 11,
    color: '#6b7280',
    marginTop: 6,
    fontWeight: '600',
  },
  activityCount: {
    fontSize: 10,
    color: '#9ca3af',
  },
  tipsCard: {
    backgroundColor: '#fffbeb',
    marginHorizontal: 20,
    marginTop: 16,
    borderRadius: 16,
    padding: 20,
  },
  tipItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  tipIcon: {
    fontSize: 20,
    marginRight: 12,
  },
  tipText: {
    flex: 1,
    fontSize: 14,
    color: '#78350f',
    lineHeight: 20,
  },
});
