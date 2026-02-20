import { useState, useEffect, useRef } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, TextInput, ScrollView, Alert, Modal } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

interface Exercise {
  id: number;
  question: string;
  answer: string;
  difficulty: number;
  topic: string;
  subject: number;
  points: number;
}

interface ExamResult {
  totalPoints: number;
  maxPoints: number;
  grade: number;
  subjectScores: {
    subject1: { correct: number; total: number; points: number };
    subject2: { correct: number; total: number; points: number };
    subject3: { correct: number; total: number; points: number };
  };
  timeSpent: number;
  answers: { exerciseId: number; userAnswer: string; correct: boolean }[];
}

type ExamMode = 'selection' | 'exam' | 'results';

export default function ExamScreen() {
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

  // Timer
  useEffect(() => {
    if (mode === 'exam' && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            clearInterval(timerRef.current!);
            finishExam();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [mode, timeLeft > 0]);

  const formatTime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    if (hrs > 0) {
      return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const startExam = async (type: 'full' | 'quick' | 'focus') => {
    setLoading(true);
    setExamType(type);

    try {
      // Get user profile
      const profileResponse = await fetch('http://localhost:5000/api/get-profile');
      const profileData = await profileResponse.json();
      const userProfile = profileData.profile;

      if (!userProfile) {
        Alert.alert('Atentie', 'Selecteaza mai intai profilul (M1 sau M2) de pe pagina Acasa!');
        setLoading(false);
        return;
      }

      // Fetch exercises
      const response = await fetch(`http://localhost:5000/api/exercises?profile=${userProfile}`);
      const allExercises: Exercise[] = await response.json();

      let selectedExercises: Exercise[] = [];
      let duration = 0;

      if (type === 'full') {
        // Full BAC simulation: 30 exercises, 3 hours
        // 10 from each subject
        const subj1 = allExercises.filter(e => e.subject === 1).slice(0, 10);
        const subj2 = allExercises.filter(e => e.subject === 2).slice(0, 10);
        const subj3 = allExercises.filter(e => e.subject === 3).slice(0, 10);
        selectedExercises = [...subj1, ...subj2, ...subj3];
        duration = 3 * 60 * 60; // 3 hours
      } else if (type === 'quick') {
        // Quick mode: 10 random exercises, 10 minutes
        const shuffled = [...allExercises].sort(() => Math.random() - 0.5);
        selectedExercises = shuffled.slice(0, 10);
        duration = 10 * 60; // 10 minutes
      } else if (type === 'focus') {
        // Focus mode: exercises from weak topics (harder ones)
        const harder = allExercises.filter(e => e.difficulty >= 3);
        const shuffled = harder.length > 0 ? harder : allExercises;
        selectedExercises = shuffled.sort(() => Math.random() - 0.5).slice(0, 15);
        duration = 30 * 60; // 30 minutes
      }

      if (selectedExercises.length === 0) {
        Alert.alert('Eroare', 'Nu sunt suficiente exercitii disponibile.');
        setLoading(false);
        return;
      }

      setExercises(selectedExercises);
      setTimeLeft(duration);
      setExamStartTime(new Date());
      setAnswers({});
      setCurrentIndex(0);
      setMode('exam');
    } catch (error) {
      Alert.alert('Eroare', 'Nu pot incarca exercitiile pentru examen.');
    }
    setLoading(false);
  };

  const finishExam = async () => {
    if (timerRef.current) clearInterval(timerRef.current);

    const endTime = new Date();
    const timeSpent = examStartTime
      ? Math.floor((endTime.getTime() - examStartTime.getTime()) / 1000)
      : 0;

    // Calculate results
    const subjectScores = {
      subject1: { correct: 0, total: 0, points: 0 },
      subject2: { correct: 0, total: 0, points: 0 },
      subject3: { correct: 0, total: 0, points: 0 },
    };

    const answerResults: { exerciseId: number; userAnswer: string; correct: boolean }[] = [];

    exercises.forEach(exercise => {
      const userAnswer = answers[exercise.id] || '';
      const isCorrect = userAnswer.trim().toLowerCase() === exercise.answer.toLowerCase();

      answerResults.push({
        exerciseId: exercise.id,
        userAnswer,
        correct: isCorrect,
      });

      const subjectKey = `subject${exercise.subject}` as keyof typeof subjectScores;
      subjectScores[subjectKey].total += 1;
      if (isCorrect) {
        subjectScores[subjectKey].correct += 1;
        subjectScores[subjectKey].points += exercise.points || 5;
      }
    });

    const totalPoints = subjectScores.subject1.points + subjectScores.subject2.points + subjectScores.subject3.points;
    const maxPoints = exercises.reduce((sum, ex) => sum + (ex.points || 5), 0);

    // Calculate grade (1-10 scale)
    const grade = Math.max(1, Math.min(10, 1 + (totalPoints / maxPoints) * 9));

    // Send results to backend
    try {
      for (const answer of answerResults) {
        const exercise = exercises.find(e => e.id === answer.exerciseId);
        if (exercise) {
          await fetch('http://localhost:5000/api/submit-answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              exercise_id: answer.exerciseId,
              answer: answer.userAnswer,
              exam_mode: true,
            }),
          });
        }
      }
    } catch (error) {
      console.log('Error saving exam results:', error);
    }

    setResult({
      totalPoints,
      maxPoints,
      grade: Math.round(grade * 100) / 100,
      subjectScores,
      timeSpent,
      answers: answerResults,
    });
    setMode('results');
  };

  const renderSelection = () => (
    <ScrollView style={styles.container}>
      <LinearGradient
        colors={['#8b5cf6', '#6366f1']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <Text style={styles.headerTitle}>Mod Examen</Text>
        <Text style={styles.headerSubtitle}>Alege tipul de simulare</Text>
      </LinearGradient>

      <View style={styles.cardsContainer}>
        {/* Full BAC Simulation */}
        <TouchableOpacity
          style={styles.examCard}
          onPress={() => startExam('full')}
          disabled={loading}
        >
          <LinearGradient
            colors={['#ef4444', '#dc2626']}
            style={styles.examCardGradient}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
          >
            <Text style={styles.examCardEmoji}>🎓</Text>
            <Text style={styles.examCardTitle}>Simulare BAC Completa</Text>
            <Text style={styles.examCardDescription}>
              30 exercitii din toate subiectele
            </Text>
            <View style={styles.examCardDetails}>
              <View style={styles.examCardBadge}>
                <Text style={styles.examCardBadgeText}>⏱️ 3 ore</Text>
              </View>
              <View style={styles.examCardBadge}>
                <Text style={styles.examCardBadgeText}>📝 30 ex.</Text>
              </View>
            </View>
          </LinearGradient>
        </TouchableOpacity>

        {/* Quick Mode */}
        <TouchableOpacity
          style={styles.examCard}
          onPress={() => startExam('quick')}
          disabled={loading}
        >
          <LinearGradient
            colors={['#f59e0b', '#d97706']}
            style={styles.examCardGradient}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
          >
            <Text style={styles.examCardEmoji}>⚡</Text>
            <Text style={styles.examCardTitle}>Mod Rapid</Text>
            <Text style={styles.examCardDescription}>
              Test rapid pentru verificare
            </Text>
            <View style={styles.examCardDetails}>
              <View style={styles.examCardBadge}>
                <Text style={styles.examCardBadgeText}>⏱️ 10 min</Text>
              </View>
              <View style={styles.examCardBadge}>
                <Text style={styles.examCardBadgeText}>📝 10 ex.</Text>
              </View>
            </View>
          </LinearGradient>
        </TouchableOpacity>

        {/* Focus Mode */}
        <TouchableOpacity
          style={styles.examCard}
          onPress={() => startExam('focus')}
          disabled={loading}
        >
          <LinearGradient
            colors={['#10b981', '#059669']}
            style={styles.examCardGradient}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
          >
            <Text style={styles.examCardEmoji}>🎯</Text>
            <Text style={styles.examCardTitle}>Mod Focus</Text>
            <Text style={styles.examCardDescription}>
              Exercitii dificile pentru antrenament
            </Text>
            <View style={styles.examCardDetails}>
              <View style={styles.examCardBadge}>
                <Text style={styles.examCardBadgeText}>⏱️ 30 min</Text>
              </View>
              <View style={styles.examCardBadge}>
                <Text style={styles.examCardBadgeText}>📝 15 ex.</Text>
              </View>
            </View>
          </LinearGradient>
        </TouchableOpacity>
      </View>

      {loading && (
        <View style={styles.loadingOverlay}>
          <Text style={styles.loadingText}>Se pregateste examenul...</Text>
        </View>
      )}
    </ScrollView>
  );

  const renderExam = () => {
    const currentExercise = exercises[currentIndex];
    const answeredCount = Object.keys(answers).length;
    const progress = ((currentIndex + 1) / exercises.length) * 100;

    return (
      <View style={styles.container}>
        {/* Exit Modal */}
        <Modal visible={showExitModal} transparent animationType="fade">
          <View style={styles.modalOverlay}>
            <View style={styles.exitModal}>
              <Text style={styles.exitModalTitle}>Iesi din examen?</Text>
              <Text style={styles.exitModalText}>
                Progresul tau va fi pierdut. Esti sigur?
              </Text>
              <View style={styles.exitModalButtons}>
                <TouchableOpacity
                  style={styles.exitModalButtonCancel}
                  onPress={() => setShowExitModal(false)}
                >
                  <Text style={styles.exitModalButtonCancelText}>Continua</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={styles.exitModalButtonConfirm}
                  onPress={() => {
                    setShowExitModal(false);
                    setMode('selection');
                    if (timerRef.current) clearInterval(timerRef.current);
                  }}
                >
                  <Text style={styles.exitModalButtonConfirmText}>Iesi</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </Modal>

        {/* Timer Header */}
        <View style={[
          styles.timerHeader,
          timeLeft < 300 && styles.timerHeaderWarning
        ]}>
          <TouchableOpacity onPress={() => setShowExitModal(true)}>
            <Text style={styles.exitButton}>✕</Text>
          </TouchableOpacity>
          <View style={styles.timerCenter}>
            <Text style={styles.timerText}>{formatTime(timeLeft)}</Text>
            <Text style={styles.timerLabel}>
              {examType === 'full' ? 'Simulare BAC' : examType === 'quick' ? 'Mod Rapid' : 'Mod Focus'}
            </Text>
          </View>
          <View style={styles.progressBadge}>
            <Text style={styles.progressBadgeText}>{answeredCount}/{exercises.length}</Text>
          </View>
        </View>

        {/* Progress Bar */}
        <View style={styles.progressBarContainer}>
          <View style={[styles.progressBar, { width: `${progress}%` }]} />
        </View>

        {/* Exercise */}
        <ScrollView style={styles.examContent}>
          <View style={styles.exerciseHeader}>
            <Text style={styles.exerciseNumber}>
              Exercitiul {currentIndex + 1} din {exercises.length}
            </Text>
            <View style={styles.exerciseBadges}>
              <View style={styles.subjectBadge}>
                <Text style={styles.subjectBadgeText}>Subiectul {currentExercise.subject}</Text>
              </View>
              <View style={styles.difficultyBadge}>
                <Text style={styles.difficultyBadgeText}>Nivel {currentExercise.difficulty}</Text>
              </View>
            </View>
          </View>

          <View style={styles.questionCard}>
            <Text style={styles.questionText}>{currentExercise.question}</Text>

            <TextInput
              style={styles.answerInput}
              value={answers[currentExercise.id] || ''}
              onChangeText={(text) => setAnswers(prev => ({ ...prev, [currentExercise.id]: text }))}
              placeholder="Scrie raspunsul tau..."
              placeholderTextColor="#9ca3af"
              multiline
            />
          </View>

          {/* Navigation */}
          <View style={styles.examNavigation}>
            <TouchableOpacity
              style={[styles.examNavButton, currentIndex === 0 && styles.examNavButtonDisabled]}
              onPress={() => setCurrentIndex(prev => Math.max(0, prev - 1))}
              disabled={currentIndex === 0}
            >
              <Text style={styles.examNavButtonText}>← Anterior</Text>
            </TouchableOpacity>

            {currentIndex < exercises.length - 1 ? (
              <TouchableOpacity
                style={styles.examNavButton}
                onPress={() => setCurrentIndex(prev => prev + 1)}
              >
                <Text style={styles.examNavButtonText}>Urmator →</Text>
              </TouchableOpacity>
            ) : (
              <TouchableOpacity
                style={styles.finishButton}
                onPress={finishExam}
              >
                <LinearGradient
                  colors={['#10b981', '#059669']}
                  style={styles.finishButtonGradient}
                >
                  <Text style={styles.finishButtonText}>Finalizeaza</Text>
                </LinearGradient>
              </TouchableOpacity>
            )}
          </View>

          {/* Quick Navigation */}
          <View style={styles.quickNav}>
            <Text style={styles.quickNavTitle}>Salt rapid:</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {exercises.map((_, index) => (
                <TouchableOpacity
                  key={index}
                  style={[
                    styles.quickNavButton,
                    index === currentIndex && styles.quickNavButtonActive,
                    answers[exercises[index].id] && styles.quickNavButtonAnswered,
                  ]}
                  onPress={() => setCurrentIndex(index)}
                >
                  <Text style={[
                    styles.quickNavButtonText,
                    index === currentIndex && styles.quickNavButtonTextActive,
                  ]}>
                    {index + 1}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        </ScrollView>
      </View>
    );
  };

  const renderResults = () => {
    if (!result) return null;

    const getGradeColor = (grade: number): [string, string] => {
      if (grade >= 9) return ['#10b981', '#059669'];
      if (grade >= 7) return ['#f59e0b', '#d97706'];
      if (grade >= 5) return ['#f97316', '#ea580c'];
      return ['#ef4444', '#dc2626'];
    };

    const getGradeEmoji = (grade: number) => {
      if (grade >= 9) return '🏆';
      if (grade >= 7) return '👏';
      if (grade >= 5) return '💪';
      return '📚';
    };

    return (
      <ScrollView style={styles.container}>
        <LinearGradient
          colors={getGradeColor(result.grade)}
          style={styles.resultsHeader}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <Text style={styles.resultsEmoji}>{getGradeEmoji(result.grade)}</Text>
          <Text style={styles.resultsGrade}>{result.grade.toFixed(2)}</Text>
          <Text style={styles.resultsLabel}>Nota ta</Text>
        </LinearGradient>

        <View style={styles.resultsContent}>
          {/* Summary */}
          <View style={styles.summaryCard}>
            <Text style={styles.summaryTitle}>Rezumat</Text>
            <View style={styles.summaryRow}>
              <Text style={styles.summaryLabel}>Puncte obtinute:</Text>
              <Text style={styles.summaryValue}>{result.totalPoints} / {result.maxPoints}</Text>
            </View>
            <View style={styles.summaryRow}>
              <Text style={styles.summaryLabel}>Timp petrecut:</Text>
              <Text style={styles.summaryValue}>{formatTime(result.timeSpent)}</Text>
            </View>
            <View style={styles.summaryRow}>
              <Text style={styles.summaryLabel}>Raspunsuri corecte:</Text>
              <Text style={styles.summaryValue}>
                {result.answers.filter(a => a.correct).length} / {result.answers.length}
              </Text>
            </View>
          </View>

          {/* Subject Breakdown */}
          <View style={styles.breakdownCard}>
            <Text style={styles.breakdownTitle}>Pe subiecte</Text>

            {[1, 2, 3].map(subj => {
              const key = `subject${subj}` as keyof typeof result.subjectScores;
              const score = result.subjectScores[key];
              const percentage = score.total > 0 ? (score.correct / score.total) * 100 : 0;

              return (
                <View key={subj} style={styles.subjectRow}>
                  <Text style={styles.subjectLabel}>Subiectul {subj}</Text>
                  <View style={styles.subjectBarContainer}>
                    <View style={[styles.subjectBar, { width: `${percentage}%` }]} />
                  </View>
                  <Text style={styles.subjectScore}>{score.correct}/{score.total}</Text>
                </View>
              );
            })}
          </View>

          {/* Actions */}
          <View style={styles.resultsActions}>
            <TouchableOpacity
              style={styles.retryButton}
              onPress={() => startExam(examType)}
            >
              <Text style={styles.retryButtonText}>Incearca din nou</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.backButton}
              onPress={() => setMode('selection')}
            >
              <Text style={styles.backButtonText}>Inapoi la selectie</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    );
  };

  if (mode === 'selection') return renderSelection();
  if (mode === 'exam') return renderExam();
  if (mode === 'results') return renderResults();

  return null;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f7fa',
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
  cardsContainer: {
    padding: 20,
    gap: 16,
  },
  examCard: {
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 5,
  },
  examCardGradient: {
    padding: 24,
    alignItems: 'center',
  },
  examCardEmoji: {
    fontSize: 48,
    marginBottom: 12,
  },
  examCardTitle: {
    fontSize: 22,
    fontWeight: '800',
    color: 'white',
    marginBottom: 8,
  },
  examCardDescription: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
    marginBottom: 16,
    textAlign: 'center',
  },
  examCardDetails: {
    flexDirection: 'row',
    gap: 12,
  },
  examCardBadge: {
    backgroundColor: 'rgba(255,255,255,0.25)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  examCardBadgeText: {
    color: 'white',
    fontWeight: '600',
    fontSize: 13,
  },
  loadingOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
  },
  timerHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#8b5cf6',
    paddingTop: 50,
    paddingBottom: 16,
    paddingHorizontal: 20,
  },
  timerHeaderWarning: {
    backgroundColor: '#ef4444',
  },
  exitButton: {
    fontSize: 24,
    color: 'white',
    fontWeight: '600',
  },
  timerCenter: {
    alignItems: 'center',
  },
  timerText: {
    fontSize: 32,
    fontWeight: '800',
    color: 'white',
  },
  timerLabel: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
    marginTop: 2,
  },
  progressBadge: {
    backgroundColor: 'rgba(255,255,255,0.25)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  progressBadgeText: {
    color: 'white',
    fontWeight: '700',
  },
  progressBarContainer: {
    height: 4,
    backgroundColor: '#e5e7eb',
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#10b981',
  },
  examContent: {
    flex: 1,
    padding: 20,
  },
  exerciseHeader: {
    marginBottom: 16,
  },
  exerciseNumber: {
    fontSize: 14,
    color: '#6b7280',
    fontWeight: '600',
    marginBottom: 8,
  },
  exerciseBadges: {
    flexDirection: 'row',
    gap: 8,
  },
  subjectBadge: {
    backgroundColor: '#eff6ff',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  subjectBadgeText: {
    color: '#3b82f6',
    fontSize: 12,
    fontWeight: '600',
  },
  difficultyBadge: {
    backgroundColor: '#fef3c7',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  difficultyBadgeText: {
    color: '#92400e',
    fontSize: 12,
    fontWeight: '600',
  },
  questionCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  questionText: {
    fontSize: 18,
    color: '#1f2937',
    lineHeight: 26,
    marginBottom: 20,
  },
  answerInput: {
    backgroundColor: '#f9fafb',
    borderWidth: 2,
    borderColor: '#e5e7eb',
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    minHeight: 60,
    color: '#1f2937',
  },
  examNavigation: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 20,
    gap: 12,
  },
  examNavButton: {
    flex: 1,
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#e5e7eb',
  },
  examNavButtonDisabled: {
    opacity: 0.5,
  },
  examNavButtonText: {
    fontSize: 15,
    fontWeight: '600',
    color: '#6b7280',
  },
  finishButton: {
    flex: 1,
    borderRadius: 12,
    overflow: 'hidden',
  },
  finishButtonGradient: {
    padding: 16,
    alignItems: 'center',
  },
  finishButtonText: {
    color: 'white',
    fontSize: 15,
    fontWeight: '700',
  },
  quickNav: {
    marginTop: 24,
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
  },
  quickNavTitle: {
    fontSize: 12,
    color: '#6b7280',
    fontWeight: '600',
    marginBottom: 12,
    textTransform: 'uppercase',
  },
  quickNavButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
  },
  quickNavButtonActive: {
    backgroundColor: '#8b5cf6',
  },
  quickNavButtonAnswered: {
    backgroundColor: '#d1fae5',
  },
  quickNavButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#6b7280',
  },
  quickNavButtonTextActive: {
    color: 'white',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  exitModal: {
    backgroundColor: 'white',
    padding: 24,
    borderRadius: 20,
    width: '80%',
    alignItems: 'center',
  },
  exitModalTitle: {
    fontSize: 20,
    fontWeight: '700',
    marginBottom: 8,
    color: '#1f2937',
  },
  exitModalText: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    marginBottom: 20,
  },
  exitModalButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  exitModalButtonCancel: {
    flex: 1,
    backgroundColor: '#f3f4f6',
    padding: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  exitModalButtonCancelText: {
    color: '#6b7280',
    fontWeight: '600',
  },
  exitModalButtonConfirm: {
    flex: 1,
    backgroundColor: '#ef4444',
    padding: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  exitModalButtonConfirmText: {
    color: 'white',
    fontWeight: '600',
  },
  resultsHeader: {
    paddingTop: 60,
    paddingBottom: 40,
    alignItems: 'center',
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },
  resultsEmoji: {
    fontSize: 64,
    marginBottom: 16,
  },
  resultsGrade: {
    fontSize: 72,
    fontWeight: '800',
    color: 'white',
  },
  resultsLabel: {
    fontSize: 18,
    color: 'rgba(255,255,255,0.9)',
    marginTop: 4,
  },
  resultsContent: {
    padding: 20,
  },
  summaryCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  summaryTitle: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 16,
    color: '#1f2937',
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  summaryLabel: {
    fontSize: 14,
    color: '#6b7280',
  },
  summaryValue: {
    fontSize: 14,
    fontWeight: '700',
    color: '#1f2937',
  },
  breakdownCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  breakdownTitle: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 16,
    color: '#1f2937',
  },
  subjectRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  subjectLabel: {
    width: 90,
    fontSize: 13,
    color: '#6b7280',
  },
  subjectBarContainer: {
    flex: 1,
    height: 8,
    backgroundColor: '#e5e7eb',
    borderRadius: 4,
    marginHorizontal: 12,
    overflow: 'hidden',
  },
  subjectBar: {
    height: '100%',
    backgroundColor: '#8b5cf6',
    borderRadius: 4,
  },
  subjectScore: {
    width: 40,
    fontSize: 13,
    fontWeight: '600',
    color: '#1f2937',
    textAlign: 'right',
  },
  resultsActions: {
    gap: 12,
  },
  retryButton: {
    backgroundColor: '#8b5cf6',
    padding: 18,
    borderRadius: 14,
    alignItems: 'center',
  },
  retryButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '700',
  },
  backButton: {
    backgroundColor: 'white',
    padding: 18,
    borderRadius: 14,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#e5e7eb',
  },
  backButtonText: {
    color: '#6b7280',
    fontSize: 16,
    fontWeight: '600',
  },
});
