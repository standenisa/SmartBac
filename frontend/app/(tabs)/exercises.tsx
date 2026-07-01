import { useState, useEffect, useRef } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, TextInput, ScrollView, Alert, Modal } from 'react-native';
import Animated, { useSharedValue, useAnimatedStyle, withSequence, withTiming, FadeInDown } from 'react-native-reanimated';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { apiGet, apiPost } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import { TYPO } from '@/constants/typography';
import DuoButton from '@/components/DuoButton';
import HeartBar from '@/components/HeartBar';
import XPPopup from '@/components/XPPopup';
import ConfettiAnimation from '@/components/ConfettiAnimation';
import ProgressRing from '@/components/ProgressRing';
import AnimatedPressable from '@/components/AnimatedPressable';
import { ExerciseCardSkeleton } from '@/components/Skeleton';
import ErrorState from '@/components/ErrorState';
import MathText from '@/components/MathText';
import { useToast } from '@/contexts/ToastContext';
import { useSound } from '@/hooks/useSound';

// Pașii pot veni ca obiecte {step, action, result} sau ca text simplu ("Step 3: ...")
function normalizeStep(step: any, index: number): { num: string | number; action: string; result: string } {
  if (typeof step === 'string') {
    const m = step.match(/^\s*(?:Step|Pas)\s*(\d+)\s*[:.)]\s*(.*)$/is);
    if (m) return { num: m[1], action: m[2].trim(), result: '' };
    return { num: index + 1, action: step.trim(), result: '' };
  }
  return {
    num: step?.step ?? index + 1,
    action: step?.action ?? '',
    result: step?.result ?? '',
  };
}

interface SolutionStep { step: number; action: string; result: string; }
interface Solution { id: number; question: string; answer: string; solution_steps: SolutionStep[]; hints: string[]; explanation: string; formula: string | null; }
interface Exercise { id: number; question: string; topic: string; difficulty: number; subject: number; }
interface Feedback { correct: boolean; message: string; correct_answer?: string; }
interface SessionResult { exercise: Exercise; correct: boolean; userAnswer: string; }

const TOPIC_COLORS: Record<string, string> = {
  equation: DUO.green,
  derivative: DUO.blue,
  limit: DUO.purple,
  integral: DUO.orange,
  matrix: DUO.red,
  probability: DUO.yellow,
  geometry: DUO.cyan,
  trigonometry: DUO.pink,
  function: DUO.green,
  sequence: DUO.blue,
  complex_number: DUO.purple,
  combinatorics: DUO.orange,
  vector: DUO.cyan,
};

export default function ExercisesScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const { showToast } = useToast();
  const { playSound, haptic } = useSound();
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [currentExercise, setCurrentExercise] = useState<Exercise | null>(null);
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [selectedSubject, setSelectedSubject] = useState<number | null>(null);
  const [showSolution, setShowSolution] = useState(false);
  const [solution, setSolution] = useState<Solution | null>(null);
  const [loadingSolution, setLoadingSolution] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [showHints, setShowHints] = useState(false);
  const [hints, setHints] = useState<string[]>([]);
  const [hintLevel, setHintLevel] = useState(0);
  const [hearts, setHearts] = useState(3);
  const [showXP, setShowXP] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [sessionResults, setSessionResults] = useState<SessionResult[]>([]);
  const [showSummary, setShowSummary] = useState(false);
  const [sessionStartTime, setSessionStartTime] = useState(Date.now());
  const advanceTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const shakeX = useSharedValue(0);
  const shakeStyle = useAnimatedStyle(() => ({ transform: [{ translateX: shakeX.value }] }));

  // Animated progress bar
  const progressWidth = useSharedValue(0);
  const progressStyle = useAnimatedStyle(() => ({ width: `${progressWidth.value}%` as any }));

  useEffect(() => { fetchExercises(); }, []);
  useEffect(() => { if (!loading) { setLoading(true); fetchExercises(); } }, [selectedSubject]);

  // Update progress bar animation when exercise changes
  useEffect(() => {
    if (currentExercise && exercises.length > 0) {
      const p = ((exercises.findIndex(ex => ex.id === currentExercise.id) + 1) / exercises.length) * 100;
      progressWidth.value = withTiming(p, { duration: 400 });
    }
  }, [currentExercise, exercises]);

  const resetExerciseState = () => {
    setAnswer(''); setFeedback(null); setShowSolution(false); setSolution(null);
    setShowHints(false); setHintLevel(0); setCurrentStep(0);
  };

  const fetchExercises = async () => {
    try {
      const profile = user?.profile;
      if (!profile) { Alert.alert('Alege profilul!', 'Te rog alege profilul (M1/M2) din Setari!'); setLoading(false); return; }
      let endpoint = `/api/exercises?profile=${profile}`;
      if (selectedSubject !== null) endpoint += `&subject=${selectedSubject}`;
      const data = await apiGet<Exercise[]>(endpoint);
      setExercises(data);
      if (data.length > 0) setCurrentExercise(data[0]);
      else Alert.alert('Info', 'Nu exista exercitii pentru acest filtru.');
      setLoading(false); resetExerciseState(); setHearts(3);
    } catch (err) { setError(true); setLoading(false); }
  };

  const submitAnswer = async () => {
    if (!answer.trim()) { Alert.alert('Atentie', 'Te rog introdu un raspuns!'); return; }
    if (!currentExercise) return;
    try {
      const result = await apiPost<Feedback>('/api/exercises/submit-answer', {
        exercise_id: currentExercise.id, answer: answer, user_id: user?.id,
      });
      setFeedback(result);
      // Salvăm rezultatul sesiunii
      setSessionResults(prev => [...prev, {
        exercise: currentExercise,
        correct: result.correct,
        userAnswer: answer.trim(),
      }]);
      if (result.correct) {
        playSound('correct');
        haptic('success');
        setShowConfetti(true); setShowXP(true);
        advanceTimer.current = setTimeout(() => nextExercise(), 2500);
      } else {
        playSound('wrong');
        haptic('error');
        shakeX.value = withSequence(
          withTiming(-12, { duration: 50 }), withTiming(12, { duration: 50 }),
          withTiming(-12, { duration: 50 }), withTiming(12, { duration: 50 }),
          withTiming(0, { duration: 50 })
        );
        setHearts(prev => Math.max(0, prev - 1));
      }
    } catch (error) { Alert.alert('Eroare', 'Nu pot trimite raspunsul!'); }
  };

  const fetchSolution = async () => {
    if (!currentExercise) return;
    setLoadingSolution(true);
    try {
      const data = await apiGet<any>(`/api/exercises/${currentExercise.id}/solution`);
      if (data.success && data.solution) { setSolution(data.solution); setCurrentStep(0); setShowSolution(true); }
      else Alert.alert('Info', 'Rezolvarea nu este disponibila.');
    } catch (error) { Alert.alert('Eroare', 'Nu pot incarca rezolvarea!'); }
    setLoadingSolution(false);
  };

  const fetchHints = async (level: number = 1) => {
    if (!currentExercise) return;
    try {
      const data = await apiGet<any>(`/api/exercises/${currentExercise.id}/hints?level=${level}&user_id=${user?.id}`);
      if (data.success) {
        setHints(data.hints || []);
        setHintLevel(level);
        setShowHints(true);
        if (level > 1) {
          showToast({ type: 'error', title: `-${data.xp_cost} XP`, subtitle: `Hint nivel ${level} deblocat` });
        }
      }
    } catch { setHints(['Gandeste-te la formulele invatate']); setShowHints(true); }
  };

  const nextExercise = () => {
    if (!currentExercise) return;
    if (advanceTimer.current) clearTimeout(advanceTimer.current);
    setShowConfetti(false);
    const idx = exercises.findIndex(ex => ex.id === currentExercise.id);
    if (idx < exercises.length - 1) {
      setCurrentExercise(exercises[idx + 1]);
      resetExerciseState();
    } else {
      // Sesiune terminată — arată summary cu feedback
      setShowSummary(true);
    }
  };

  const topicColor = currentExercise ? (TOPIC_COLORS[currentExercise.topic] || DUO.blue) : DUO.blue;

  // Session summary — feedback personalizat
  if (showSummary) {
    const totalQ = sessionResults.length;
    const correctQ = sessionResults.filter(r => r.correct).length;
    const accuracy = totalQ > 0 ? Math.round((correctQ / totalQ) * 100) : 0;
    const timeSpent = Math.round((Date.now() - sessionStartTime) / 60000);
    const xpEarned = correctQ * 10;

    // Analiză pe topicuri
    const topicStats: Record<string, { correct: number; total: number }> = {};
    sessionResults.forEach(r => {
      const t = r.exercise.topic;
      if (!topicStats[t]) topicStats[t] = { correct: 0, total: 0 };
      topicStats[t].total++;
      if (r.correct) topicStats[t].correct++;
    });

    const weakTopics = Object.entries(topicStats)
      .filter(([_, s]) => s.correct / s.total < 0.5)
      .map(([t]) => t);
    const strongTopics = Object.entries(topicStats)
      .filter(([_, s]) => s.correct / s.total >= 0.8)
      .map(([t]) => t);

    // Feedback personalizat
    let feedbackTitle = '';
    let feedbackIcon: keyof typeof Ionicons.glyphMap = 'book';
    let feedbackIconColor = DUO.blue;
    let feedbackMessages: string[] = [];

    if (accuracy >= 90) {
      feedbackTitle = 'Excelent!'; feedbackIcon = 'trophy'; feedbackIconColor = DUO.yellow;
      feedbackMessages = ['Performanta extraordinara!', 'Esti pregatit pentru BAC la acest nivel.', 'Incearca exercitii mai dificile pentru a te provoca.'];
    } else if (accuracy >= 70) {
      feedbackTitle = 'Foarte bine!'; feedbackIcon = 'star'; feedbackIconColor = DUO.yellow;
      feedbackMessages = ['Rezultat foarte bun!', 'Mai exerseaza putin si vei fi perfect.'];
      if (weakTopics.length > 0) feedbackMessages.push(`Concentreaza-te pe: ${weakTopics.join(', ')}`);
    } else if (accuracy >= 50) {
      feedbackTitle = 'Bine, dar poti mai mult!'; feedbackIcon = 'fitness'; feedbackIconColor = DUO.orange;
      feedbackMessages = ['Ai o baza solida, dar mai e loc de imbunatatire.'];
      if (weakTopics.length > 0) feedbackMessages.push(`Repeta teoria la: ${weakTopics.join(', ')}`);
      feedbackMessages.push('Foloseste hint-urile si solutiile pentru a intelege mai bine.');
    } else {
      feedbackTitle = 'Mai exerseaza!'; feedbackIcon = 'book'; feedbackIconColor = DUO.blue;
      feedbackMessages = ['Nu te descuraja! Practica face perfect.', 'Recomandam sa revezi teoria inainte de exercitii.'];
      if (weakTopics.length > 0) feedbackMessages.push(`Focus pe: ${weakTopics.join(', ')}`);
      feedbackMessages.push('Incearca cu exercitii mai usoare si creste gradual dificultatea.');
    }

    const resetSession = () => {
      setShowSummary(false);
      setSessionResults([]);
      setSessionStartTime(Date.now());
      setHearts(3);
      resetExerciseState();
      fetchExercises();
    };

    return (
      <View style={[styles.container, { paddingTop: insets.top }]}>
        <ScrollView contentContainerStyle={{ padding: 20, gap: 16 }}>
          {/* Header */}
          <Animated.View entering={FadeInDown.duration(400)} style={{ alignItems: 'center', gap: 8, marginTop: 20 }}>
            <Ionicons name={feedbackIcon} size={64} color={feedbackIconColor} />
            <Text style={{ fontSize: 28, fontWeight: '900', color: DUO.textPrimary, textAlign: 'center' }}>{feedbackTitle}</Text>
          </Animated.View>

          {/* Score Ring */}
          <Animated.View entering={FadeInDown.delay(100).duration(400)} style={{ alignItems: 'center' }}>
            <ProgressRing
              progress={accuracy / 100}
              size={120}
              strokeWidth={8}
              color={accuracy >= 70 ? DUO.green : accuracy >= 50 ? DUO.yellow : DUO.red}
            >
              <Text style={{ fontSize: 32, fontWeight: '900', color: accuracy >= 70 ? DUO.green : accuracy >= 50 ? DUO.yellow : DUO.red }}>
                {accuracy}%
              </Text>
            </ProgressRing>
          </Animated.View>

          {/* Stats Row */}
          <Animated.View entering={FadeInDown.delay(200).duration(400)} style={{ flexDirection: 'row', gap: 10 }}>
            <View style={{ flex: 1, backgroundColor: DUO.card, borderRadius: 14, padding: 14, alignItems: 'center', borderWidth: 1, borderColor: DUO.green + '20' }}>
              <Text style={{ fontSize: 24, fontWeight: '900', color: DUO.green }}>{correctQ}</Text>
              <Text style={{ fontSize: 11, fontWeight: '700', color: DUO.textMuted }}>CORECTE</Text>
            </View>
            <View style={{ flex: 1, backgroundColor: DUO.card, borderRadius: 14, padding: 14, alignItems: 'center', borderWidth: 1, borderColor: DUO.red + '20' }}>
              <Text style={{ fontSize: 24, fontWeight: '900', color: DUO.red }}>{totalQ - correctQ}</Text>
              <Text style={{ fontSize: 11, fontWeight: '700', color: DUO.textMuted }}>GRESITE</Text>
            </View>
            <View style={{ flex: 1, backgroundColor: DUO.card, borderRadius: 14, padding: 14, alignItems: 'center', borderWidth: 1, borderColor: DUO.yellow + '20' }}>
              <Text style={{ fontSize: 24, fontWeight: '900', color: DUO.yellow }}>+{xpEarned}</Text>
              <Text style={{ fontSize: 11, fontWeight: '700', color: DUO.textMuted }}>XP</Text>
            </View>
          </Animated.View>

          {/* Time */}
          <Animated.View entering={FadeInDown.delay(250).duration(400)} style={{ backgroundColor: DUO.card, borderRadius: 14, padding: 14, flexDirection: 'row', justifyContent: 'center', gap: 20, borderWidth: 1, borderColor: DUO.surface }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}><Ionicons name="timer" size={14} color={DUO.textSecondary} /><Text style={{ fontSize: 13, fontWeight: '700', color: DUO.textSecondary }}>Timp: {timeSpent} min</Text></View>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}><Ionicons name="create" size={14} color={DUO.textSecondary} /><Text style={{ fontSize: 13, fontWeight: '700', color: DUO.textSecondary }}>Exercitii: {totalQ}</Text></View>
          </Animated.View>

          {/* AI Feedback */}
          <Animated.View entering={FadeInDown.delay(300).duration(400)} style={{ backgroundColor: DUO.card, borderRadius: 16, padding: 18, gap: 10, borderWidth: 1, borderColor: DUO.blue + '20' }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
              <Ionicons name="hardware-chip" size={20} color={DUO.blue} />
              <Text style={{ fontSize: 15, fontWeight: '800', color: DUO.blue }}>Feedback AI</Text>
            </View>
            {feedbackMessages.map((msg, i) => (
              <View key={i} style={{ flexDirection: 'row', gap: 8, alignItems: 'flex-start' }}>
                <Text style={{ fontSize: 12, color: DUO.blue, marginTop: 2 }}>•</Text>
                <Text style={{ fontSize: 14, fontWeight: '600', color: DUO.textSecondary, flex: 1, lineHeight: 20 }}>{msg}</Text>
              </View>
            ))}
          </Animated.View>

          {/* Topic Breakdown */}
          {Object.keys(topicStats).length > 0 && (
            <Animated.View entering={FadeInDown.delay(400).duration(400)} style={{ backgroundColor: DUO.card, borderRadius: 16, padding: 18, gap: 10, borderWidth: 1, borderColor: DUO.surface }}>
              <Text style={{ fontSize: 13, fontWeight: '800', color: DUO.textMuted, letterSpacing: 1 }}>REZULTATE PE TOPICURI</Text>
              {Object.entries(topicStats).map(([topic, stats]) => {
                const acc = Math.round((stats.correct / stats.total) * 100);
                const color = acc >= 80 ? DUO.green : acc >= 50 ? DUO.yellow : DUO.red;
                return (
                  <View key={topic} style={{ gap: 4 }}>
                    <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Text style={{ fontSize: 14, fontWeight: '700', color: DUO.textPrimary, textTransform: 'capitalize' }}>{topic.replace(/_/g, ' ')}</Text>
                      <Text style={{ fontSize: 13, fontWeight: '800', color }}>{stats.correct}/{stats.total} ({acc}%)</Text>
                    </View>
                    <View style={{ height: 6, backgroundColor: DUO.surface, borderRadius: 3, overflow: 'hidden' }}>
                      <View style={{ width: `${acc}%`, height: '100%', backgroundColor: color, borderRadius: 3 } as any} />
                    </View>
                  </View>
                );
              })}
            </Animated.View>
          )}

          {/* Exerciții greșite */}
          {sessionResults.filter(r => !r.correct).length > 0 && (
            <Animated.View entering={FadeInDown.delay(500).duration(400)} style={{ backgroundColor: DUO.card, borderRadius: 16, padding: 18, gap: 10, borderWidth: 1, borderColor: DUO.red + '20' }}>
              <Text style={{ fontSize: 13, fontWeight: '800', color: DUO.red, letterSpacing: 1 }}>EXERCITII DE REPETAT</Text>
              {sessionResults.filter(r => !r.correct).map((r, i) => (
                <View key={i} style={{ backgroundColor: DUO.red + '10', borderRadius: 10, padding: 12, gap: 4 }}>
                  <Text style={{ fontSize: 13, fontWeight: '700', color: DUO.textPrimary }}>{r.exercise.question}</Text>
                  <Text style={{ fontSize: 12, fontWeight: '600', color: DUO.red }}>Răspunsul tău: {r.userAnswer}</Text>
                </View>
              ))}
            </Animated.View>
          )}

          {/* Buttons */}
          <Animated.View entering={FadeInDown.delay(600).duration(400)} style={{ gap: 10, marginTop: 8 }}>
            <AnimatedPressable onPress={resetSession}>
              <LinearGradient colors={[DUO.green, DUO.greenDark]} style={{ borderRadius: 16, padding: 18, alignItems: 'center' }}>
                <Text style={{ fontSize: 17, fontWeight: '800', color: DUO.white }}>Continua sa exersezi</Text>
              </LinearGradient>
            </AnimatedPressable>
            <AnimatedPressable onPress={() => { setShowSummary(false); setSessionResults([]); }} style={{ padding: 14, alignItems: 'center' }}>
              <Text style={{ fontSize: 14, fontWeight: '700', color: DUO.textMuted }}>Inapoi la exercitii</Text>
            </AnimatedPressable>
          </Animated.View>

          <View style={{ height: 40 }} />
        </ScrollView>
      </View>
    );
  }

  if (loading) return (
    <View style={styles.container}>
      <View style={[styles.topBar, { paddingTop: insets.top + 8 }]}>
        <View style={styles.progressBarBg}><View style={[styles.progressBarFillStatic, { width: '0%' }]} /></View>
      </View>
      <ExerciseCardSkeleton />
    </View>
  );

  if (error) return (
    <ErrorState preset="network" onRetry={() => { setError(false); setLoading(true); fetchExercises(); }} />
  );

  if (!currentExercise) return (
    <View style={styles.loadingContainer}><Ionicons name="school" size={64} color={DUO.textMuted} /><Text style={styles.loadingText}>Nu exista exercitii disponibile</Text></View>
  );

  return (
    <View style={styles.container}>
      <ConfettiAnimation visible={showConfetti} />
      <XPPopup xp={10} visible={showXP} onDone={() => setShowXP(false)} />

      {/* Solution Modal */}
      <Modal visible={showSolution} animationType="slide" transparent onRequestClose={() => setShowSolution(false)}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <ScrollView showsVerticalScrollIndicator={false}>
              <View style={styles.modalHeader}>
                <Text style={[styles.modalTitle, TYPO.heading2]}>Rezolvare</Text>
                <TouchableOpacity style={styles.closeBtn} onPress={() => setShowSolution(false)}>
                  <Text style={styles.closeBtnText}>✕</Text>
                </TouchableOpacity>
              </View>
              {solution && (
                <>
                  {solution.formula && (
                    <View style={styles.formulaBox}>
                      <Text style={[styles.formulaLabel, TYPO.caption]}>FORMULA</Text>
                      <Text style={styles.formulaText}>{solution.formula}</Text>
                    </View>
                  )}
                  {solution.solution_steps.map((step, index) => {
                    const s = normalizeStep(step, index);
                    return (
                      <View key={index} style={[styles.stepCard, index > currentStep && { opacity: 0.3 }]}>
                        <View style={styles.stepCircle}><Text style={styles.stepCircleText}>{s.num}</Text></View>
                        <View style={styles.stepBody}>
                          {!!s.action && <MathText text={s.action} style={styles.stepAction} />}
                          {!!s.result && <MathText text={s.result} style={styles.stepResult} />}
                        </View>
                      </View>
                    );
                  })}
                  {currentStep < solution.solution_steps.length - 1 && (
                    <TouchableOpacity style={styles.showAllBtn} onPress={() => setCurrentStep(solution.solution_steps.length - 1)}>
                      <Text style={styles.showAllBtnText}>Arata toti pasii</Text>
                    </TouchableOpacity>
                  )}
                  <View style={styles.stepNav}>
                    <TouchableOpacity onPress={() => setCurrentStep(Math.max(0, currentStep - 1))} disabled={currentStep === 0}>
                      <Text style={[styles.stepNavText, currentStep === 0 && { opacity: 0.3 }]}>← Anterior</Text>
                    </TouchableOpacity>
                    <Text style={styles.stepCounter}>{currentStep + 1}/{solution.solution_steps.length}</Text>
                    <TouchableOpacity onPress={() => setCurrentStep(Math.min(solution.solution_steps.length - 1, currentStep + 1))} disabled={currentStep >= solution.solution_steps.length - 1}>
                      <Text style={[styles.stepNavText, currentStep >= solution.solution_steps.length - 1 && { opacity: 0.3 }]}>Urmator →</Text>
                    </TouchableOpacity>
                  </View>
                  {solution.explanation && (
                    <View style={styles.explanationBox}><Text style={styles.explanationText}>{solution.explanation}</Text></View>
                  )}
                  <View style={styles.finalAnswer}>
                    <Text style={styles.finalAnswerLabel}>RASPUNS FINAL</Text>
                    <Text style={styles.finalAnswerText}>{solution.answer}</Text>
                  </View>
                </>
              )}
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* Top Bar */}
      <View style={[styles.topBar, { paddingTop: insets.top + 8 }]}>
        <View style={styles.progressBarBg}>
          <Animated.View style={[styles.progressBarFillAnimated, progressStyle, { backgroundColor: DUO.green }]} />
        </View>
        <View style={styles.topBarRow}>
          <Text style={styles.progressLabel}>{exercises.findIndex(ex => ex.id === currentExercise.id) + 1}/{exercises.length}</Text>
          <HeartBar hearts={hearts} />
        </View>
      </View>

      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* Subject Filter */}
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll} contentContainerStyle={styles.filterContent}>
          {[{ label: 'Toate', val: null }, { label: 'Sub. I', val: 1 }, { label: 'Sub. II', val: 2 }, { label: 'Sub. III', val: 3 }].map((f) => (
            <TouchableOpacity key={f.label} style={[styles.filterChip, selectedSubject === f.val && styles.filterChipActive]} onPress={() => setSelectedSubject(f.val)}>
              <Text style={[styles.filterChipText, selectedSubject === f.val && styles.filterChipTextActive]}>{f.label}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        {/* Exercise Card */}
        <Animated.View style={[styles.exerciseCard, shakeStyle, { borderTopWidth: 3, borderTopColor: topicColor }]}>
          <View style={styles.badgeRow}>
            <View style={[styles.badge, { backgroundColor: DUO.blue + '20', borderColor: DUO.blue + '30' }]}>
              <Text style={[styles.badgeText, { color: DUO.blue }]}>{currentExercise.topic}</Text>
            </View>
            <View style={[styles.badge, { backgroundColor: DUO.orange + '20', borderColor: DUO.orange + '30' }]}>
              <Text style={[styles.badgeText, { color: DUO.orange }]}>Nivel {currentExercise.difficulty}</Text>
            </View>
          </View>

          <Text style={styles.question}>{currentExercise.question}</Text>

          {showHints && hints.length > 0 && (
            <View style={styles.hintsBox}>
              <Text style={styles.hintsTitle}>Indicii:</Text>
              {hints.map((hint, i) => <Text key={i} style={styles.hintText}>• {hint}</Text>)}
            </View>
          )}

          <TextInput
            style={[styles.input, feedback?.correct === true && styles.inputCorrect, feedback?.correct === false && styles.inputWrong]}
            value={answer} onChangeText={setAnswer}
            placeholder="Scrie raspunsul tau aici..."
            placeholderTextColor={DUO.textMuted}
            editable={!feedback}
          />

          {!feedback && (
            <View style={styles.actionButtons}>
              <View style={styles.hintRow}>
                {hintLevel < 1 && (
                  <TouchableOpacity style={styles.hintButton} onPress={() => fetchHints(1)}>
                    <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}><Ionicons name="bulb" size={14} color={DUO.yellow} /><Text style={styles.hintButtonText}>Hint</Text></View>
                  </TouchableOpacity>
                )}
                {hintLevel >= 1 && hintLevel < 2 && (
                  <TouchableOpacity style={[styles.hintButton, { borderColor: DUO.orange + '30' }]} onPress={() => fetchHints(2)}>
                    <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}><Ionicons name="bulb" size={14} color={DUO.orange} /><Ionicons name="bulb" size={14} color={DUO.orange} /><Text style={[styles.hintButtonText, { color: DUO.orange }]}>-5 XP</Text></View>
                  </TouchableOpacity>
                )}
                {hintLevel >= 2 && hintLevel < 3 && (
                  <TouchableOpacity style={[styles.hintButton, { borderColor: DUO.red + '30' }]} onPress={() => fetchHints(3)}>
                    <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}><Ionicons name="bulb" size={14} color={DUO.red} /><Ionicons name="bulb" size={14} color={DUO.red} /><Ionicons name="bulb" size={14} color={DUO.red} /><Text style={[styles.hintButtonText, { color: DUO.red }]}>-10 XP</Text></View>
                  </TouchableOpacity>
                )}
              </View>
              <DuoButton title="VERIFICA" onPress={submitAnswer} color={DUO.green} darkColor={DUO.greenDark} glow />
            </View>
          )}

          {feedback && (
            <Animated.View
              entering={FadeInDown.springify().damping(15)}
              style={[styles.feedbackCard, feedback.correct ? styles.feedbackCorrect : styles.feedbackWrong]}
            >
              <Ionicons name={feedback.correct ? 'checkmark-circle' : 'sad'} size={48} color={feedback.correct ? DUO.green : DUO.red} />
              <Text style={[styles.feedbackTitle, { color: feedback.correct ? DUO.green : DUO.red }]}>
                {feedback.correct ? 'Excelent!' : 'Nu e corect'}
              </Text>
              <Text style={styles.feedbackMessage}>{feedback.message}</Text>
              {!feedback.correct && feedback.correct_answer && (
                <View style={styles.correctAnswerBox}>
                  <Text style={styles.correctAnswerLabel}>Raspuns corect:</Text>
                  <Text style={styles.correctAnswerText}>{feedback.correct_answer}</Text>
                </View>
              )}
              <View style={styles.feedbackActions}>
                <DuoButton title="VEZI REZOLVAREA" onPress={fetchSolution} color={DUO.blue} darkColor={DUO.blueDark} size="medium" disabled={loadingSolution} />
                <DuoButton title="CONTINUA" onPress={nextExercise} color={feedback.correct ? DUO.green : DUO.red} size="medium" />
              </View>
            </Animated.View>
          )}
        </Animated.View>

        {/* Navigation */}
        <View style={styles.navRow}>
          <TouchableOpacity style={[styles.navBtn, exercises.findIndex(ex => ex.id === currentExercise.id) === 0 && { opacity: 0.4 }]}
            onPress={() => { const idx = exercises.findIndex(ex => ex.id === currentExercise.id); if (idx > 0) { setCurrentExercise(exercises[idx - 1]); resetExerciseState(); } }}
            disabled={exercises.findIndex(ex => ex.id === currentExercise.id) === 0}>
            <Text style={styles.navBtnText}>← Anterior</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.navBtn} onPress={nextExercise}>
            <Text style={styles.navBtnText}>Urmator →</Text>
          </TouchableOpacity>
        </View>
        <View style={{ height: 40 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  loadingContainer: { flex: 1, backgroundColor: DUO.bg, justifyContent: 'center', alignItems: 'center' },
  loadingText: { fontSize: 16, color: DUO.textSecondary, fontWeight: '700' },
  topBar: { paddingHorizontal: 20, paddingBottom: 12, backgroundColor: DUO.card, borderBottomWidth: 1, borderBottomColor: DUO.surface },
  progressBarBg: { height: 10, backgroundColor: DUO.surface, borderRadius: 5, overflow: 'hidden', marginBottom: 8 },
  progressBarFillStatic: { height: '100%', backgroundColor: DUO.green, borderRadius: 5 },
  progressBarFillAnimated: { height: '100%', borderRadius: 5 },
  topBarRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  progressLabel: { fontSize: 14, fontWeight: '800', color: DUO.textSecondary },
  scrollView: { flex: 1 },
  filterScroll: { marginTop: 12 },
  filterContent: { paddingHorizontal: 20, gap: 8 },
  filterChip: { backgroundColor: DUO.card, paddingHorizontal: 16, paddingVertical: 10, borderRadius: DUO.radiusFull, borderWidth: 1, borderColor: DUO.surface },
  filterChipActive: { backgroundColor: DUO.blue, borderColor: DUO.blueDark },
  filterChipText: { fontSize: 14, fontWeight: '700', color: DUO.textSecondary },
  filterChipTextActive: { color: DUO.white },
  exerciseCard: { backgroundColor: DUO.card, margin: 20, padding: 20, borderRadius: DUO.radiusLg, borderWidth: 1, borderColor: DUO.surface },
  badgeRow: { flexDirection: 'row', gap: 8, marginBottom: 16 },
  badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: DUO.radiusFull, borderWidth: 1 },
  badgeText: { fontSize: 12, fontWeight: '800' },
  question: { fontSize: 18, color: DUO.textPrimary, lineHeight: 28, marginBottom: 20, fontWeight: '700' },
  hintsBox: { backgroundColor: DUO.yellow + '15', padding: 14, borderRadius: 12, marginBottom: 16, borderWidth: 1, borderColor: DUO.yellow + '30' },
  hintsTitle: { fontSize: 14, fontWeight: '800', color: DUO.yellow, marginBottom: 6 },
  hintText: { fontSize: 14, color: DUO.textPrimary, lineHeight: 22 },
  input: { backgroundColor: DUO.surface, borderWidth: 1, borderColor: DUO.surfaceLight, borderRadius: DUO.radius, padding: 16, fontSize: 16, marginBottom: 16, color: DUO.textPrimary, fontWeight: '600', borderBottomWidth: 4, borderBottomColor: DUO.cardDark },
  inputCorrect: { borderColor: DUO.green, backgroundColor: DUO.green + '15', borderBottomColor: DUO.greenDark },
  inputWrong: { borderColor: DUO.red, backgroundColor: DUO.red + '15', borderBottomColor: DUO.redDark },
  actionButtons: { gap: 12 },
  hintRow: { flexDirection: 'row', gap: 8 },
  hintButton: { backgroundColor: DUO.yellow + '15', padding: 14, borderRadius: DUO.radius, alignItems: 'center', borderWidth: 1, borderColor: DUO.yellow + '30' },
  hintButtonText: { color: DUO.yellow, fontSize: 15, fontWeight: '800' },
  feedbackCard: { padding: 20, borderRadius: DUO.radius, marginTop: 16, alignItems: 'center' },
  feedbackCorrect: { backgroundColor: DUO.green + '15', borderWidth: 1, borderColor: DUO.green + '30' },
  feedbackWrong: { backgroundColor: DUO.red + '15', borderWidth: 1, borderColor: DUO.red + '30' },
  feedbackTitle: { fontSize: 22, fontWeight: '800', marginBottom: 4 },
  feedbackMessage: { fontSize: 14, color: DUO.textSecondary, textAlign: 'center', marginBottom: 12, fontWeight: '600' },
  correctAnswerBox: { backgroundColor: DUO.surface, padding: 14, borderRadius: 12, width: '100%', marginBottom: 12 },
  correctAnswerLabel: { fontSize: 12, color: DUO.textMuted, fontWeight: '700', marginBottom: 4 },
  correctAnswerText: { fontSize: 16, color: DUO.textPrimary, fontWeight: '800' },
  feedbackActions: { gap: 10, width: '100%' },
  navRow: { flexDirection: 'row', paddingHorizontal: 20, gap: 10 },
  navBtn: { flex: 1, backgroundColor: DUO.card, padding: 16, borderRadius: DUO.radius, alignItems: 'center', borderWidth: 1, borderColor: DUO.surface, borderBottomWidth: 4, borderBottomColor: DUO.cardDark },
  navBtnText: { color: DUO.textSecondary, fontSize: 15, fontWeight: '800' },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.7)', justifyContent: 'flex-end' },
  modalContent: { backgroundColor: DUO.card, borderTopLeftRadius: 24, borderTopRightRadius: 24, maxHeight: '90%', padding: 24 },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  modalTitle: { color: DUO.textPrimary },
  closeBtn: { width: 36, height: 36, borderRadius: 18, backgroundColor: DUO.surface, justifyContent: 'center', alignItems: 'center' },
  closeBtnText: { fontSize: 16, fontWeight: '800', color: DUO.textSecondary },
  formulaBox: { backgroundColor: DUO.yellow + '15', padding: 14, borderRadius: 12, marginBottom: 16, borderLeftWidth: 4, borderLeftColor: DUO.yellow },
  formulaLabel: { color: DUO.yellow, marginBottom: 4 },
  formulaText: { fontSize: 15, color: DUO.textPrimary, fontWeight: '700', fontFamily: 'monospace' },
  stepCard: { flexDirection: 'row', marginBottom: 14, gap: 12 },
  stepCircle: { width: 30, height: 30, borderRadius: 15, backgroundColor: DUO.blue, justifyContent: 'center', alignItems: 'center' },
  stepCircleText: { color: DUO.white, fontWeight: '800', fontSize: 14 },
  stepBody: { flex: 1, backgroundColor: DUO.surface, padding: 12, borderRadius: 12 },
  stepAction: { fontSize: 14, color: DUO.textSecondary, fontWeight: '600', marginBottom: 4 },
  stepResult: { fontSize: 15, color: DUO.textPrimary, fontWeight: '800', fontFamily: 'monospace' },
  showAllBtn: { backgroundColor: DUO.surface, padding: 12, borderRadius: 12, alignItems: 'center', marginBottom: 12 },
  showAllBtnText: { color: DUO.textSecondary, fontWeight: '700', fontSize: 14 },
  stepNav: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingVertical: 12, borderTopWidth: 1, borderTopColor: DUO.surface, marginBottom: 12 },
  stepNavText: { color: DUO.blue, fontSize: 14, fontWeight: '800' },
  stepCounter: { fontSize: 14, color: DUO.textMuted, fontWeight: '700' },
  explanationBox: { backgroundColor: DUO.green + '15', padding: 14, borderRadius: 12, marginBottom: 12 },
  explanationText: { fontSize: 14, color: DUO.green, lineHeight: 22, fontWeight: '600' },
  finalAnswer: { backgroundColor: DUO.green, padding: 20, borderRadius: DUO.radius, alignItems: 'center', borderBottomWidth: 4, borderBottomColor: DUO.greenDark },
  finalAnswerLabel: { fontSize: 11, fontWeight: '800', color: 'rgba(255,255,255,0.8)', marginBottom: 6 },
  finalAnswerText: { fontSize: 28, color: DUO.white, fontWeight: '800' },
});
