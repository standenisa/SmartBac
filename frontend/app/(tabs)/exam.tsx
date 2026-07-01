import { useState, useEffect, useRef } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, TextInput, ScrollView, Alert, Modal } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as Haptics from 'expo-haptics';
import { apiGet, apiPost } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import DuoButton from '@/components/DuoButton';
import ProgressRing from '@/components/ProgressRing';

interface Exercise { id: number; question: string; answer: string; difficulty: number; topic: string; subject: number; points: number; }
interface ExamResult {
  totalPoints: number; maxPoints: number; grade: number;
  subjectScores: { subject1: { correct: number; total: number; points: number }; subject2: { correct: number; total: number; points: number }; subject3: { correct: number; total: number; points: number }; };
  timeSpent: number; answers: { exerciseId: number; userAnswer: string; correct: boolean }[];
}
type ExamMode = 'selection' | 'exam' | 'results';

export default function ExamScreen() {
  const { user } = useAuth();
  const [mode, setMode] = useState<ExamMode>('selection');
  const [examType, setExamType] = useState<'full' | 'quick' | 'focus'>('full');
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: string }>({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [examStartTime, setExamStartTime] = useState<Date | null>(null);
  const [result, setResult] = useState<ExamResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [showExitModal, setShowExitModal] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (mode === 'exam' && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => Math.max(0, prev - 1));
      }, 1000);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [mode, timeLeft > 0]);

  useEffect(() => {
    if (mode === 'exam' && timeLeft === 0) finishExam();
  }, [mode, timeLeft]);

  const formatTime = (s: number) => {
    const h = Math.floor(s / 3600); const m = Math.floor((s % 3600) / 60); const sec = s % 60;
    if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
    return `${m}:${sec.toString().padStart(2, '0')}`;
  };

  const startExam = async (type: 'full' | 'quick' | 'focus') => {
    setLoading(true); setExamType(type);
    try {
      const profile = user?.profile;
      if (!profile) { Alert.alert('Atentie', 'Selecteaza profilul M1/M2!'); setLoading(false); return; }
      const all: Exercise[] = await apiGet<Exercise[]>(`/api/exercises?profile=${profile}`);
      let sel: Exercise[] = []; let dur = 0;
      if (type === 'full') { sel = [...all.filter(e => e.subject === 1).slice(0, 10), ...all.filter(e => e.subject === 2).slice(0, 10), ...all.filter(e => e.subject === 3).slice(0, 10)]; dur = 10800; }
      else if (type === 'quick') { sel = [...all].sort(() => Math.random() - 0.5).slice(0, 10); dur = 600; }
      else { const h = all.filter(e => e.difficulty >= 3); sel = (h.length > 0 ? h : all).sort(() => Math.random() - 0.5).slice(0, 15); dur = 1800; }
      if (sel.length === 0) { Alert.alert('Eroare', 'Nu sunt exercitii.'); setLoading(false); return; }
      setExercises(sel); setTimeLeft(dur); setExamStartTime(new Date()); setAnswers({}); setCurrentIndex(0); setMode('exam');
    } catch (e) { Alert.alert('Eroare', 'Nu pot incarca exercitiile.'); }
    setLoading(false);
  };

  const finishExam = async () => {
    if (timerRef.current) clearInterval(timerRef.current);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    const timeSpent = examStartTime ? Math.floor((new Date().getTime() - examStartTime.getTime()) / 1000) : 0;
    const scores = { subject1: { correct: 0, total: 0, points: 0 }, subject2: { correct: 0, total: 0, points: 0 }, subject3: { correct: 0, total: 0, points: 0 } };
    const ansRes: { exerciseId: number; userAnswer: string; correct: boolean }[] = [];
    exercises.forEach(ex => {
      const ua = answers[ex.id] || ''; const ok = ua.trim().toLowerCase() === ex.answer.toLowerCase();
      ansRes.push({ exerciseId: ex.id, userAnswer: ua, correct: ok });
      const k = `subject${ex.subject}` as keyof typeof scores;
      scores[k].total += 1; if (ok) { scores[k].correct += 1; scores[k].points += ex.points || 5; }
    });
    const tp = scores.subject1.points + scores.subject2.points + scores.subject3.points;
    const mp = exercises.reduce((s, e) => s + (e.points || 5), 0);
    const grade = Math.max(1, Math.min(10, 1 + (tp / mp) * 9));
    try { for (const a of ansRes) { await apiPost('/api/exercises/submit-answer', { exercise_id: a.exerciseId, answer: a.userAnswer, user_id: user?.id }); } } catch (e) { console.log('Error:', e); }
    setResult({ totalPoints: tp, maxPoints: mp, grade: Math.round(grade * 100) / 100, subjectScores: scores, timeSpent, answers: ansRes }); setMode('results');
  };

  const renderSelection = () => (
    <ScrollView style={styles.container}>
      <LinearGradient colors={[DUO.card, DUO.bg]} style={styles.header}>
        <Text style={styles.headerTitle}>🎓 Mod Examen</Text>
        <Text style={styles.headerSubtitle}>Alege tipul de simulare</Text>
      </LinearGradient>
      <View style={styles.cards}>
        {[
          { type: 'full' as const, emoji: '🎓', title: 'Simulare BAC', desc: '30 exercitii, toate subiectele', time: '3 ore', count: '30 ex.', colors: [DUO.red, DUO.redDark] as [string, string] },
          { type: 'quick' as const, emoji: '⚡', title: 'Mod Rapid', desc: 'Test rapid de verificare', time: '10 min', count: '10 ex.', colors: [DUO.orange, DUO.orangeDark] as [string, string] },
          { type: 'focus' as const, emoji: '🎯', title: 'Mod Focus', desc: 'Exercitii dificile', time: '30 min', count: '15 ex.', colors: [DUO.green, DUO.greenDark] as [string, string] },
        ].map((item) => (
          <TouchableOpacity key={item.type} style={styles.examCard} onPress={() => startExam(item.type)} disabled={loading}>
            <LinearGradient colors={item.colors} style={styles.examCardGradient}>
              <Text style={styles.examEmoji}>{item.emoji}</Text>
              <Text style={styles.examTitle}>{item.title}</Text>
              <Text style={styles.examDesc}>{item.desc}</Text>
              <View style={styles.examBadges}>
                <View style={styles.examBadge}><Text style={styles.examBadgeText}>⏱️ {item.time}</Text></View>
                <View style={styles.examBadge}><Text style={styles.examBadgeText}>📝 {item.count}</Text></View>
              </View>
            </LinearGradient>
          </TouchableOpacity>
        ))}
      </View>
      {loading && <View style={styles.loadingOverlay}><Text style={styles.loadingText}>Se pregateste... 🦉</Text></View>}
    </ScrollView>
  );

  const renderExam = () => {
    const ex = exercises[currentIndex]; const answered = Object.keys(answers).length;
    const prog = ((currentIndex + 1) / exercises.length) * 100;
    return (
      <View style={styles.container}>
        <Modal visible={showExitModal} transparent animationType="fade">
          <View style={styles.modalOverlay}>
            <View style={styles.exitModal}>
              <Text style={styles.exitTitle}>Iesi din examen?</Text>
              <Text style={styles.exitText}>Progresul va fi pierdut.</Text>
              <View style={styles.exitBtns}>
                <DuoButton title="CONTINUA" onPress={() => setShowExitModal(false)} color={DUO.green} darkColor={DUO.greenDark} size="medium" style={{ flex: 1 }} />
                <DuoButton title="IESI" onPress={() => { setShowExitModal(false); setMode('selection'); if (timerRef.current) clearInterval(timerRef.current); }} color={DUO.red} darkColor={DUO.redDark} size="medium" style={{ flex: 1 }} />
              </View>
            </View>
          </View>
        </Modal>

        <View style={[styles.timerHeader, timeLeft < 300 && { backgroundColor: DUO.red + '15', borderBottomColor: DUO.red + '30' }]}>
          <TouchableOpacity onPress={() => setShowExitModal(true)}><Text style={styles.exitBtn}>✕</Text></TouchableOpacity>
          <View style={{ alignItems: 'center' }}>
            <Text style={[styles.timerText, timeLeft < 300 && { color: DUO.red }]}>{formatTime(timeLeft)}</Text>
          </View>
          <View style={styles.answeredBadge}><Text style={styles.answeredText}>{answered}/{exercises.length}</Text></View>
        </View>
        <View style={styles.progBarBg}><View style={[styles.progBarFill, { width: `${prog}%` }]} /></View>

        <ScrollView style={{ flex: 1, padding: 20 }}>
          <View style={styles.exBadges}>
            <View style={[styles.exBadge, { backgroundColor: DUO.blue + '20', borderColor: DUO.blue + '30' }]}><Text style={[styles.exBadgeText, { color: DUO.blue }]}>Sub. {ex.subject}</Text></View>
            <View style={[styles.exBadge, { backgroundColor: DUO.orange + '20', borderColor: DUO.orange + '30' }]}><Text style={[styles.exBadgeText, { color: DUO.orange }]}>Nivel {ex.difficulty}</Text></View>
            <Text style={styles.exCount}>Ex. {currentIndex + 1}/{exercises.length}</Text>
          </View>
          <View style={styles.questionCard}>
            <Text style={styles.questionText}>{ex.question}</Text>
            <TextInput style={styles.answerInput} value={answers[ex.id] || ''} onChangeText={(t) => setAnswers(prev => ({ ...prev, [ex.id]: t }))} placeholder="Scrie raspunsul..." placeholderTextColor={DUO.textMuted} multiline />
          </View>
          <View style={styles.examNav}>
            <TouchableOpacity style={[styles.navBtn, currentIndex === 0 && { opacity: 0.4 }]} onPress={() => setCurrentIndex(p => Math.max(0, p - 1))} disabled={currentIndex === 0}>
              <Text style={styles.navBtnText}>← Anterior</Text>
            </TouchableOpacity>
            {currentIndex < exercises.length - 1 ? (
              <TouchableOpacity style={styles.navBtn} onPress={() => setCurrentIndex(p => p + 1)}><Text style={styles.navBtnText}>Urmator →</Text></TouchableOpacity>
            ) : (
              <View style={{ flex: 1 }}><DuoButton title="FINALIZEAZA" onPress={finishExam} color={DUO.green} darkColor={DUO.greenDark} glow /></View>
            )}
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop: 16 }}>
            {exercises.map((_, i) => (
              <TouchableOpacity key={i} style={[styles.quickDot, i === currentIndex && { backgroundColor: DUO.blue, borderColor: DUO.blueDark }, answers[exercises[i].id] && { backgroundColor: DUO.green + '30', borderColor: DUO.green }]} onPress={() => setCurrentIndex(i)}>
                <Text style={[styles.quickDotText, i === currentIndex && { color: DUO.white }]}>{i + 1}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </ScrollView>
      </View>
    );
  };

  const renderResults = () => {
    if (!result) return null;
    const getGradeColor = (g: number) => { if (g >= 9) return DUO.green; if (g >= 7) return DUO.yellow; if (g >= 5) return DUO.orange; return DUO.red; };
    const getEmoji = (g: number) => { if (g >= 9) return '🏆'; if (g >= 7) return '👏'; if (g >= 5) return '💪'; return '📚'; };
    const gradeColor = getGradeColor(result.grade);
    return (
      <ScrollView style={styles.container}>
        <View style={styles.resultsHeader}>
          <Text style={{ fontSize: 64 }}>{getEmoji(result.grade)}</Text>
          <ProgressRing progress={result.grade / 10} size={120} strokeWidth={8} color={gradeColor}>
            <Text style={[styles.gradeText, { color: gradeColor }]}>{result.grade.toFixed(2)}</Text>
          </ProgressRing>
          <Text style={styles.gradeLabel}>Nota ta</Text>
        </View>
        <View style={{ padding: 20 }}>
          <View style={styles.summaryCard}>
            <Text style={styles.summaryTitle}>Rezumat</Text>
            {[
              ['Puncte', `${result.totalPoints}/${result.maxPoints}`],
              ['Timp', formatTime(result.timeSpent)],
              ['Corecte', `${result.answers.filter(a => a.correct).length}/${result.answers.length}`],
            ].map(([l, v], i) => (
              <View key={i} style={styles.summaryRow}><Text style={styles.summaryLabel}>{l}</Text><Text style={styles.summaryValue}>{v}</Text></View>
            ))}
          </View>
          <View style={styles.summaryCard}>
            <Text style={styles.summaryTitle}>Pe subiecte</Text>
            {[1, 2, 3].map(s => {
              const k = `subject${s}` as keyof typeof result.subjectScores;
              const sc = result.subjectScores[k]; const pct = sc.total > 0 ? (sc.correct / sc.total) * 100 : 0;
              return (
                <View key={s} style={styles.subjRow}>
                  <Text style={styles.subjLabel}>Sub. {s}</Text>
                  <View style={styles.subjBarBg}><View style={[styles.subjBarFill, { width: `${pct}%`, backgroundColor: getGradeColor(pct / 10) }]} /></View>
                  <Text style={styles.subjScore}>{sc.correct}/{sc.total}</Text>
                </View>
              );
            })}
          </View>
          <View style={{ gap: 10 }}>
            <DuoButton title="INCEARCA DIN NOU" onPress={() => startExam(examType)} color={DUO.blue} darkColor={DUO.blueDark} glow />
            <DuoButton title="INAPOI" onPress={() => setMode('selection')} color={DUO.surface} darkColor={DUO.cardDark} textColor={DUO.textSecondary} />
          </View>
        </View>
      </ScrollView>
    );
  };

  if (mode === 'selection') return renderSelection();
  if (mode === 'exam') return renderExam();
  return renderResults();
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  header: { paddingTop: 60, paddingBottom: 20, paddingHorizontal: 20, borderBottomWidth: 1, borderBottomColor: DUO.surface },
  headerTitle: { fontSize: 28, fontWeight: '800', color: DUO.textPrimary, marginBottom: 4 },
  headerSubtitle: { fontSize: 14, color: DUO.textSecondary, fontWeight: '600' },
  cards: { padding: 20, gap: 12 },
  examCard: { borderRadius: DUO.radiusLg, overflow: 'hidden' },
  examCardGradient: { padding: 24, alignItems: 'center', borderRadius: DUO.radiusLg },
  examEmoji: { fontSize: 48, marginBottom: 8 },
  examTitle: { fontSize: 20, fontWeight: '800', color: DUO.white, marginBottom: 4 },
  examDesc: { fontSize: 14, color: 'rgba(255,255,255,0.8)', fontWeight: '600', marginBottom: 12 },
  examBadges: { flexDirection: 'row', gap: 8 },
  examBadge: { backgroundColor: 'rgba(255,255,255,0.2)', paddingHorizontal: 12, paddingVertical: 6, borderRadius: DUO.radiusFull },
  examBadgeText: { fontWeight: '700', fontSize: 13, color: DUO.white },
  loadingOverlay: { position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.7)', justifyContent: 'center', alignItems: 'center' },
  loadingText: { color: DUO.white, fontSize: 18, fontWeight: '700' },
  timerHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingTop: 52, paddingBottom: 12, paddingHorizontal: 20, backgroundColor: DUO.card, borderBottomWidth: 1, borderBottomColor: DUO.surface },
  exitBtn: { fontSize: 22, color: DUO.textMuted, fontWeight: '800' },
  timerText: { fontSize: 28, fontWeight: '800', color: DUO.textPrimary },
  answeredBadge: { backgroundColor: DUO.green + '20', paddingHorizontal: 10, paddingVertical: 4, borderRadius: DUO.radiusFull, borderWidth: 1, borderColor: DUO.green + '30' },
  answeredText: { color: DUO.green, fontWeight: '800', fontSize: 14 },
  progBarBg: { height: 4, backgroundColor: DUO.surface },
  progBarFill: { height: '100%', backgroundColor: DUO.green },
  exBadges: { flexDirection: 'row', gap: 8, marginBottom: 12, alignItems: 'center' },
  exBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: DUO.radiusFull, borderWidth: 1 },
  exBadgeText: { fontSize: 12, fontWeight: '800' },
  exCount: { fontSize: 13, fontWeight: '700', color: DUO.textMuted, marginLeft: 'auto' },
  questionCard: { backgroundColor: DUO.card, padding: 20, borderRadius: DUO.radiusLg, borderWidth: 1, borderColor: DUO.surface },
  questionText: { fontSize: 18, color: DUO.textPrimary, lineHeight: 26, marginBottom: 16, fontWeight: '700' },
  answerInput: { backgroundColor: DUO.surface, borderWidth: 1, borderColor: DUO.surfaceLight, borderRadius: DUO.radius, padding: 16, fontSize: 16, minHeight: 60, color: DUO.textPrimary, fontWeight: '600', borderBottomWidth: 4, borderBottomColor: DUO.cardDark },
  examNav: { flexDirection: 'row', marginTop: 16, gap: 10 },
  navBtn: { flex: 1, backgroundColor: DUO.card, padding: 16, borderRadius: DUO.radius, alignItems: 'center', borderWidth: 1, borderColor: DUO.surface, borderBottomWidth: 4, borderBottomColor: DUO.cardDark },
  navBtnText: { fontSize: 15, fontWeight: '800', color: DUO.textSecondary },
  quickDot: { width: 38, height: 38, borderRadius: 19, backgroundColor: DUO.surface, justifyContent: 'center', alignItems: 'center', marginRight: 8, borderWidth: 1, borderColor: DUO.surfaceLight },
  quickDotText: { fontSize: 13, fontWeight: '700', color: DUO.textSecondary },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.7)', justifyContent: 'center', alignItems: 'center' },
  exitModal: { backgroundColor: DUO.card, padding: 24, borderRadius: 20, width: '80%', alignItems: 'center', borderWidth: 1, borderColor: DUO.surface },
  exitTitle: { fontSize: 20, fontWeight: '800', color: DUO.textPrimary, marginBottom: 8 },
  exitText: { fontSize: 14, color: DUO.textSecondary, marginBottom: 20, fontWeight: '600' },
  exitBtns: { flexDirection: 'row', gap: 10, width: '100%' },
  resultsHeader: { paddingTop: 60, paddingBottom: 30, alignItems: 'center', backgroundColor: DUO.card, borderBottomWidth: 1, borderBottomColor: DUO.surface },
  gradeText: { fontSize: 36, fontWeight: '800' },
  gradeLabel: { fontSize: 16, color: DUO.textSecondary, fontWeight: '700', marginTop: 12 },
  summaryCard: { backgroundColor: DUO.card, padding: 20, borderRadius: DUO.radiusLg, marginBottom: 16, borderWidth: 1, borderColor: DUO.surface },
  summaryTitle: { fontSize: 18, fontWeight: '800', marginBottom: 14, color: DUO.textPrimary },
  summaryRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 10 },
  summaryLabel: { fontSize: 14, color: DUO.textSecondary, fontWeight: '600' },
  summaryValue: { fontSize: 14, fontWeight: '800', color: DUO.textPrimary },
  subjRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  subjLabel: { width: 50, fontSize: 13, color: DUO.textSecondary, fontWeight: '600' },
  subjBarBg: { flex: 1, height: 8, backgroundColor: DUO.surface, borderRadius: 4, marginHorizontal: 10, overflow: 'hidden' },
  subjBarFill: { height: '100%', borderRadius: 4 },
  subjScore: { width: 40, fontSize: 13, fontWeight: '800', color: DUO.textPrimary, textAlign: 'right' },
});
