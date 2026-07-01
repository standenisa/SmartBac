import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, TextInput, ScrollView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { apiGet, apiPost } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import DuoButton from '@/components/DuoButton';
import { ExerciseCardSkeleton } from '@/components/Skeleton';
import ErrorState from '@/components/ErrorState';
import { useToast } from '@/contexts/ToastContext';
import { useSound } from '@/hooks/useSound';

interface Exercise { id: number; question: string; topic: string; difficulty: number; answer?: string; }
interface Result { exercise: Exercise; userAnswer: string; correct: boolean; correctAnswer: string; }

export default function QuickPracticeScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const { showToast } = useToast();
  const { playSound, haptic } = useSound();
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [results, setResults] = useState<Result[]>([]);
  const [finished, setFinished] = useState(false);

  useEffect(() => { fetchExercises(); }, []);

  const fetchExercises = async () => {
    try {
      setError(false);
      const data = await apiGet<any>(`/api/exercises/quick-practice?user_id=${user?.id}&count=3`);
      if (data.success) setExercises(data.exercises);
      else setError(true);
    } catch { setError(true); }
    setLoading(false);
  };

  const submitAnswer = async () => {
    if (!answer.trim()) return;
    const exercise = exercises[currentIndex];
    try {
      const data = await apiPost<any>('/api/exercises/submit-answer', {
        exercise_id: exercise.id, answer: answer.trim(), user_id: user?.id,
      });
      const correct = data.correct;

      if (correct) {
        playSound('correct');
        haptic('success');
      } else {
        playSound('wrong');
        haptic('error');
      }

      setResults(prev => [...prev, {
        exercise,
        userAnswer: answer.trim(),
        correct,
        correctAnswer: data.correct_answer || answer.trim(),
      }]);

      if (currentIndex < exercises.length - 1) {
        setCurrentIndex(prev => prev + 1);
        setAnswer('');
      } else {
        setFinished(true);
      }
    } catch {
      showToast({ type: 'error', title: 'Eroare', subtitle: 'Nu pot trimite raspunsul' });
    }
  };

  if (error) return <ErrorState preset="network" onRetry={() => { setLoading(true); fetchExercises(); }} />;
  if (loading) return (
    <View style={styles.container}>
      <View style={[styles.header, { paddingTop: insets.top + 12 }]}>
        <Text style={styles.headerTitle}>⚡ Quick Practice</Text>
      </View>
      <ExerciseCardSkeleton />
    </View>
  );

  if (finished) {
    const correctCount = results.filter(r => r.correct).length;
    const perfect = correctCount === results.length;
    return (
      <View style={styles.container}>
        <ScrollView showsVerticalScrollIndicator={false}>
          <LinearGradient
            colors={[perfect ? DUO.green + '30' : DUO.orange + '30', DUO.bg]}
            style={[styles.header, { paddingTop: insets.top + 12 }]}
          >
            <Text style={styles.summaryEmoji}>{perfect ? '🎉' : '💪'}</Text>
            <Text style={styles.summaryTitle}>
              {correctCount}/{results.length} corecte
            </Text>
            <Text style={styles.summarySubtitle}>
              {perfect ? 'Perfect!' : 'Continua sa exersezi!'}
            </Text>
          </LinearGradient>

          {results.map((r, i) => (
            <View key={i} style={[styles.resultCard, { borderLeftColor: r.correct ? DUO.green : DUO.red }]}>
              <Text style={styles.resultEmoji}>{r.correct ? '✅' : '❌'}</Text>
              <View style={styles.resultInfo}>
                <Text style={styles.resultQuestion} numberOfLines={2}>{r.exercise.question}</Text>
                <Text style={[styles.resultAnswer, { color: r.correct ? DUO.green : DUO.red }]}>
                  {r.correct ? r.userAnswer : `${r.userAnswer} → ${r.correctAnswer}`}
                </Text>
              </View>
            </View>
          ))}

          <View style={{ padding: 20, gap: 10 }}>
            <DuoButton title="INAPOI ACASA" onPress={() => router.push('/' as any)} color={DUO.green} glow />
            <DuoButton title="INCA O RUNDA" onPress={() => { setFinished(false); setResults([]); setCurrentIndex(0); setAnswer(''); setLoading(true); fetchExercises(); }} color={DUO.blue} />
          </View>
          <View style={{ height: 100 }} />
        </ScrollView>
      </View>
    );
  }

  const exercise = exercises[currentIndex];
  return (
    <View style={styles.container}>
      <View style={[styles.header, { paddingTop: insets.top + 12 }]}>
        <Text style={styles.headerTitle}>⚡ Quick Practice</Text>
        <Text style={styles.headerSubtitle}>{currentIndex + 1} / {exercises.length}</Text>
      </View>

      {/* Progress dots */}
      <View style={styles.dotsRow}>
        {exercises.map((_, i) => (
          <View key={i} style={[
            styles.dot,
            i < currentIndex ? styles.dotDone : i === currentIndex ? styles.dotCurrent : null,
          ]} />
        ))}
      </View>

      <ScrollView style={{ flex: 1 }} showsVerticalScrollIndicator={false}>
        <View style={styles.exerciseCard}>
          <View style={styles.badgeRow}>
            <View style={[styles.badge, { backgroundColor: DUO.blue + '20' }]}>
              <Text style={[styles.badgeText, { color: DUO.blue }]}>{exercise?.topic}</Text>
            </View>
          </View>
          <Text style={styles.question}>{exercise?.question}</Text>

          <TextInput
            style={styles.input}
            value={answer}
            onChangeText={setAnswer}
            placeholder="Raspunsul tau..."
            placeholderTextColor={DUO.textMuted}
            autoFocus
          />

          <DuoButton title="VERIFICA" onPress={submitAnswer} color={DUO.green} darkColor={DUO.greenDark} glow />
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  header: { paddingBottom: 16, paddingHorizontal: 20, borderBottomWidth: 1, borderBottomColor: DUO.surface, alignItems: 'center' },
  headerTitle: { fontSize: 22, fontWeight: '800', color: DUO.textPrimary },
  headerSubtitle: { fontSize: 13, color: DUO.textSecondary, fontWeight: '600', marginTop: 2 },
  dotsRow: { flexDirection: 'row', justifyContent: 'center', gap: 8, paddingVertical: 16 },
  dot: { width: 10, height: 10, borderRadius: 5, backgroundColor: DUO.surface },
  dotDone: { backgroundColor: DUO.green },
  dotCurrent: { backgroundColor: DUO.orange, width: 24 },
  exerciseCard: { backgroundColor: DUO.card, margin: 20, padding: 20, borderRadius: 20, borderWidth: 1, borderColor: DUO.surface },
  badgeRow: { flexDirection: 'row', gap: 8, marginBottom: 16 },
  badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 999 },
  badgeText: { fontSize: 12, fontWeight: '800' },
  question: { fontSize: 18, color: DUO.textPrimary, lineHeight: 28, marginBottom: 20, fontWeight: '700' },
  input: { backgroundColor: DUO.surface, borderWidth: 1, borderColor: DUO.surfaceLight, borderRadius: 16, padding: 16, fontSize: 16, marginBottom: 16, color: DUO.textPrimary, fontWeight: '600', borderBottomWidth: 4, borderBottomColor: DUO.cardDark },
  summaryEmoji: { fontSize: 56, marginBottom: 8 },
  summaryTitle: { fontSize: 28, fontWeight: '800', color: DUO.textPrimary },
  summarySubtitle: { fontSize: 14, color: DUO.textSecondary, fontWeight: '600' },
  resultCard: { flexDirection: 'row', alignItems: 'center', backgroundColor: DUO.card, marginHorizontal: 20, marginBottom: 8, padding: 14, borderRadius: 12, borderLeftWidth: 3, borderWidth: 1, borderColor: DUO.surface },
  resultEmoji: { fontSize: 24, marginRight: 12 },
  resultInfo: { flex: 1 },
  resultQuestion: { fontSize: 13, color: DUO.textPrimary, fontWeight: '600', marginBottom: 2 },
  resultAnswer: { fontSize: 14, fontWeight: '800' },
});
