import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, TextInput, ScrollView, Alert, Modal } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

// Tipuri pentru soluție
interface SolutionStep {
  step: number;
  action: string;
  result: string;
}

interface Solution {
  id: number;
  question: string;
  answer: string;
  solution_steps: SolutionStep[];
  hints: string[];
  explanation: string;
  formula: string | null;
}

interface Exercise {
  id: number;
  question: string;
  topic: string;
  difficulty: number;
  subject: number;
}

interface Feedback {
  correct: boolean;
  message: string;
  correct_answer?: string;
}

export default function ExercisesScreen() {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [currentExercise, setCurrentExercise] = useState<Exercise | null>(null);
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [selectedSubject, setSelectedSubject] = useState<number | null>(null);

  // State pentru soluții
  const [showSolution, setShowSolution] = useState(false);
  const [solution, setSolution] = useState<Solution | null>(null);
  const [loadingSolution, setLoadingSolution] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [showHints, setShowHints] = useState(false);
  const [hints, setHints] = useState<string[]>([]);

  useEffect(() => {
    fetchExercises();
  }, []);

  useEffect(() => {
    if (!loading) {
      setLoading(true);
      fetchExercises();
    }
  }, [selectedSubject]);

  const fetchExercises = async () => {
    try {
      const profileResponse = await fetch('http://localhost:5000/api/get-profile');
      const profileData = await profileResponse.json();
      const userProfile = profileData.profile;

      if (!userProfile) {
        Alert.alert(
          'Alege profilul!',
          'Te rog alege mai intai profilul (M1 sau M2) de pe pagina Acasa!'
        );
        setLoading(false);
        return;
      }

      let url = `http://localhost:5000/api/exercises?profile=${userProfile}`;
      if (selectedSubject !== null) {
        url += `&subject=${selectedSubject}`;
      }

      const response = await fetch(url);
      const data = await response.json();

      setExercises(data);
      if (data.length > 0) {
        setCurrentExercise(data[0]);
      } else {
        Alert.alert('Info', 'Nu exista exercitii pentru acest filtru.');
      }
      setLoading(false);
      setFeedback(null);
      setAnswer('');
      setShowSolution(false);
      setSolution(null);
      setShowHints(false);
    } catch (error) {
      Alert.alert('Eroare', 'Nu pot incarca exercitiile!');
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!answer.trim()) {
      Alert.alert('Atentie', 'Te rog introdu un raspuns!');
      return;
    }

    if (!currentExercise) return;

    try {
      const response = await fetch('http://localhost:5000/api/submit-answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          exercise_id: currentExercise.id,
          answer: answer,
        }),
      });

      const result = await response.json();
      setFeedback(result);

      if (result.correct) {
        setTimeout(() => {
          nextExercise();
        }, 2000);
      }
    } catch (error) {
      Alert.alert('Eroare', 'Nu pot trimite raspunsul!');
    }
  };

  const fetchSolution = async () => {
    if (!currentExercise) return;

    setLoadingSolution(true);
    try {
      const response = await fetch(
        `http://localhost:5000/api/exercises/${currentExercise.id}/solution`
      );
      const data = await response.json();

      if (data.success && data.solution) {
        setSolution(data.solution);
        setCurrentStep(0);
        setShowSolution(true);
      } else {
        Alert.alert('Info', 'Rezolvarea nu este disponibila pentru acest exercitiu.');
      }
    } catch (error) {
      Alert.alert('Eroare', 'Nu pot incarca rezolvarea!');
    }
    setLoadingSolution(false);
  };

  const fetchHints = async () => {
    if (!currentExercise) return;

    try {
      const response = await fetch(
        `http://localhost:5000/api/exercises/${currentExercise.id}/hints`
      );
      const data = await response.json();

      if (data.success) {
        setHints(data.hints || []);
        setShowHints(true);
      }
    } catch (error) {
      // Fallback hints
      setHints(['Gandeste-te la formulele invatate']);
      setShowHints(true);
    }
  };

  const nextExercise = () => {
    if (!currentExercise) return;
    const currentIndex = exercises.findIndex(ex => ex.id === currentExercise.id);
    if (currentIndex < exercises.length - 1) {
      setCurrentExercise(exercises[currentIndex + 1]);
      setAnswer('');
      setFeedback(null);
      setShowSolution(false);
      setSolution(null);
      setShowHints(false);
      setCurrentStep(0);
    } else {
      Alert.alert('Felicitari!', 'Ai terminat toate exercitiile disponibile!');
    }
  };

  const renderSolutionModal = () => (
    <Modal
      visible={showSolution}
      animationType="slide"
      transparent={true}
      onRequestClose={() => setShowSolution(false)}
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <ScrollView showsVerticalScrollIndicator={false}>
            {/* Header */}
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Rezolvare pas cu pas</Text>
              <TouchableOpacity
                style={styles.closeButton}
                onPress={() => setShowSolution(false)}
              >
                <Text style={styles.closeButtonText}>×</Text>
              </TouchableOpacity>
            </View>

            {solution && (
              <>
                {/* Formula (daca exista) */}
                {solution.formula && (
                  <View style={styles.formulaBox}>
                    <Text style={styles.formulaLabel}>Formula</Text>
                    <Text style={styles.formulaText}>{solution.formula}</Text>
                  </View>
                )}

                {/* Pasi de rezolvare */}
                <View style={styles.stepsContainer}>
                  <Text style={styles.stepsTitle}>Pasi:</Text>

                  {solution.solution_steps.map((step, index) => (
                    <View
                      key={index}
                      style={[
                        styles.stepCard,
                        index <= currentStep ? styles.stepCardVisible : styles.stepCardHidden
                      ]}
                    >
                      <View style={styles.stepHeader}>
                        <View style={styles.stepNumber}>
                          <Text style={styles.stepNumberText}>{step.step}</Text>
                        </View>
                        <Text style={styles.stepAction}>{step.action}</Text>
                      </View>
                      <View style={styles.stepResultBox}>
                        <Text style={styles.stepResult}>{step.result}</Text>
                      </View>
                    </View>
                  ))}

                  {/* Butoane navigare pasi */}
                  {solution.solution_steps.length > 0 && (
                    <View style={styles.stepNavigation}>
                      <TouchableOpacity
                        style={[
                          styles.stepNavButton,
                          currentStep === 0 && styles.stepNavButtonDisabled
                        ]}
                        onPress={() => setCurrentStep(Math.max(0, currentStep - 1))}
                        disabled={currentStep === 0}
                      >
                        <Text style={styles.stepNavButtonText}>← Pasul anterior</Text>
                      </TouchableOpacity>

                      <Text style={styles.stepCounter}>
                        {currentStep + 1} / {solution.solution_steps.length}
                      </Text>

                      <TouchableOpacity
                        style={[
                          styles.stepNavButton,
                          currentStep >= solution.solution_steps.length - 1 && styles.stepNavButtonDisabled
                        ]}
                        onPress={() => setCurrentStep(Math.min(solution.solution_steps.length - 1, currentStep + 1))}
                        disabled={currentStep >= solution.solution_steps.length - 1}
                      >
                        <Text style={styles.stepNavButtonText}>Pasul urmator →</Text>
                      </TouchableOpacity>
                    </View>
                  )}

                  {/* Buton arata toti pasii */}
                  {currentStep < solution.solution_steps.length - 1 && (
                    <TouchableOpacity
                      style={styles.showAllButton}
                      onPress={() => setCurrentStep(solution.solution_steps.length - 1)}
                    >
                      <Text style={styles.showAllButtonText}>Arata toti pasii</Text>
                    </TouchableOpacity>
                  )}
                </View>

                {/* Explicatie */}
                {solution.explanation && (
                  <View style={styles.explanationBox}>
                    <Text style={styles.explanationLabel}>Explicatie</Text>
                    <Text style={styles.explanationText}>{solution.explanation}</Text>
                  </View>
                )}

                {/* Raspuns final */}
                <View style={styles.finalAnswerBox}>
                  <Text style={styles.finalAnswerLabel}>Raspuns final</Text>
                  <Text style={styles.finalAnswerText}>{solution.answer}</Text>
                </View>
              </>
            )}
          </ScrollView>
        </View>
      </View>
    </Modal>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Se incarca exercitiile...</Text>
      </View>
    );
  }

  if (!currentExercise) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Nu exista exercitii disponibile</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {renderSolutionModal()}

      {/* Header cu gradient */}
      <LinearGradient
        colors={['#f093fb', '#f5576c']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <Text style={styles.headerTitle}>Exerseaza</Text>
        <Text style={styles.headerProgress}>
          {exercises.findIndex(ex => ex.id === currentExercise.id) + 1} / {exercises.length}
        </Text>
      </LinearGradient>

      {/* Filtre subiecte */}
      <View style={styles.filterContainer}>
        <Text style={styles.filterTitle}>Filtreaza pe subiect:</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
          <TouchableOpacity
            style={[styles.filterChip, selectedSubject === null && styles.filterChipActive]}
            onPress={() => setSelectedSubject(null)}
          >
            <Text style={[styles.filterChipText, selectedSubject === null && styles.filterChipTextActive]}>
              Toate
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.filterChip, selectedSubject === 1 && styles.filterChipActive]}
            onPress={() => setSelectedSubject(1)}
          >
            <Text style={[styles.filterChipText, selectedSubject === 1 && styles.filterChipTextActive]}>
              Subiectul I
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.filterChip, selectedSubject === 2 && styles.filterChipActive]}
            onPress={() => setSelectedSubject(2)}
          >
            <Text style={[styles.filterChipText, selectedSubject === 2 && styles.filterChipTextActive]}>
              Subiectul II
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.filterChip, selectedSubject === 3 && styles.filterChipActive]}
            onPress={() => setSelectedSubject(3)}
          >
            <Text style={[styles.filterChipText, selectedSubject === 3 && styles.filterChipTextActive]}>
              Subiectul III
            </Text>
          </TouchableOpacity>
        </ScrollView>
      </View>

      {/* Exercise Card */}
      <View style={styles.exerciseCard}>
        <View style={styles.badgeContainer}>
          <View style={[styles.badge, { backgroundColor: '#fff3e0' }]}>
            <Text style={styles.badgeText}>{currentExercise.topic}</Text>
          </View>
          <View style={[styles.badge, { backgroundColor: '#e3f2fd' }]}>
            <Text style={styles.badgeText}>Nivel {currentExercise.difficulty}</Text>
          </View>
        </View>

        <Text style={styles.question}>{currentExercise.question}</Text>

        {/* Hints (daca sunt afisate) */}
        {showHints && hints.length > 0 && (
          <View style={styles.hintsBox}>
            <Text style={styles.hintsTitle}>Indicii:</Text>
            {hints.map((hint, index) => (
              <Text key={index} style={styles.hintText}>• {hint}</Text>
            ))}
          </View>
        )}

        <TextInput
          style={styles.input}
          value={answer}
          onChangeText={setAnswer}
          placeholder="Scrie raspunsul tau aici..."
          placeholderTextColor="#9ca3af"
          editable={!feedback}
        />

        {/* Butoane actiune */}
        {!feedback && (
          <View style={styles.actionButtons}>
            {/* Buton indicii */}
            {!showHints && (
              <TouchableOpacity
                style={styles.hintButton}
                onPress={fetchHints}
              >
                <Text style={styles.hintButtonText}>Vreau un indiciu</Text>
              </TouchableOpacity>
            )}

            {/* Buton verificare */}
            <TouchableOpacity style={styles.submitButton} onPress={submitAnswer}>
              <LinearGradient
                colors={['#667eea', '#764ba2']}
                style={styles.submitGradient}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
              >
                <Text style={styles.submitButtonText}>Verifica raspunsul</Text>
              </LinearGradient>
            </TouchableOpacity>
          </View>
        )}

        {feedback && (
          <View style={[
            styles.feedbackCard,
            feedback.correct ? styles.feedbackCorrect : styles.feedbackWrong
          ]}>
            <Text style={styles.feedbackEmoji}>
              {feedback.correct ? '🎉' : '💡'}
            </Text>
            <Text style={styles.feedbackText}>{feedback.message}</Text>
            {!feedback.correct && feedback.correct_answer && (
              <View style={styles.correctAnswerBox}>
                <Text style={styles.correctAnswerLabel}>Raspuns corect:</Text>
                <Text style={styles.correctAnswerText}>{feedback.correct_answer}</Text>
              </View>
            )}

            {/* Buton rezolvare completa */}
            <TouchableOpacity
              style={styles.solutionButton}
              onPress={fetchSolution}
              disabled={loadingSolution}
            >
              <LinearGradient
                colors={['#10b981', '#059669']}
                style={styles.solutionGradient}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
              >
                <Text style={styles.solutionButtonText}>
                  {loadingSolution ? 'Se incarca...' : 'Vezi rezolvarea completa'}
                </Text>
              </LinearGradient>
            </TouchableOpacity>

            <TouchableOpacity style={styles.nextButton} onPress={nextExercise}>
              <Text style={styles.nextButtonText}>Urmatorul exercitiu →</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>

      {/* Navigation */}
      <View style={styles.navigationButtons}>
        <TouchableOpacity
          style={[
            styles.navButton,
            exercises.findIndex(ex => ex.id === currentExercise.id) === 0 && styles.navButtonDisabled
          ]}
          onPress={() => {
            const currentIndex = exercises.findIndex(ex => ex.id === currentExercise.id);
            if (currentIndex > 0) {
              setCurrentExercise(exercises[currentIndex - 1]);
              setAnswer('');
              setFeedback(null);
              setShowSolution(false);
              setSolution(null);
              setShowHints(false);
            }
          }}
          disabled={exercises.findIndex(ex => ex.id === currentExercise.id) === 0}
        >
          <Text style={styles.navButtonText}>← Anterior</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.navButton}
          onPress={nextExercise}
        >
          <Text style={styles.navButtonText}>Urmatorul →</Text>
        </TouchableOpacity>
      </View>

      <View style={{ height: 40 }} />
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
    backgroundColor: '#f5f7fa',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 18,
    color: '#6b7280',
    fontWeight: '600',
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
  headerProgress: {
    fontSize: 18,
    color: 'rgba(255,255,255,0.9)',
    fontWeight: '600',
  },
  filterContainer: {
    backgroundColor: 'white',
    padding: 20,
    marginTop: 20,
    marginHorizontal: 20,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  filterTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#6b7280',
    marginBottom: 12,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  filterScroll: {
    flexDirection: 'row',
  },
  filterChip: {
    backgroundColor: '#f3f4f6',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
    marginRight: 8,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  filterChipActive: {
    backgroundColor: '#eff6ff',
    borderColor: '#667eea',
  },
  filterChipText: {
    fontSize: 14,
    color: '#6b7280',
    fontWeight: '600',
  },
  filterChipTextActive: {
    color: '#667eea',
  },
  exerciseCard: {
    backgroundColor: 'white',
    margin: 20,
    padding: 24,
    borderRadius: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.08,
    shadowRadius: 12,
    elevation: 3,
  },
  badgeContainer: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 16,
  },
  badge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  badgeText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#6b7280',
  },
  question: {
    fontSize: 19,
    color: '#1f2937',
    lineHeight: 28,
    marginBottom: 20,
    fontWeight: '600',
  },
  hintsBox: {
    backgroundColor: '#fef3c7',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  hintsTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#92400e',
    marginBottom: 8,
  },
  hintText: {
    fontSize: 14,
    color: '#78350f',
    lineHeight: 22,
  },
  input: {
    backgroundColor: '#f9fafb',
    borderWidth: 2,
    borderColor: '#e5e7eb',
    borderRadius: 16,
    padding: 16,
    fontSize: 16,
    marginBottom: 16,
    color: '#1f2937',
  },
  actionButtons: {
    gap: 12,
  },
  hintButton: {
    backgroundColor: '#fef3c7',
    padding: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  hintButtonText: {
    color: '#92400e',
    fontSize: 15,
    fontWeight: '600',
  },
  submitButton: {
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#667eea',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  submitGradient: {
    padding: 18,
    alignItems: 'center',
  },
  submitButtonText: {
    color: 'white',
    fontSize: 17,
    fontWeight: '700',
  },
  feedbackCard: {
    padding: 20,
    borderRadius: 16,
    marginTop: 16,
    alignItems: 'center',
  },
  feedbackCorrect: {
    backgroundColor: '#d1fae5',
  },
  feedbackWrong: {
    backgroundColor: '#fee2e2',
  },
  feedbackEmoji: {
    fontSize: 40,
    marginBottom: 12,
  },
  feedbackText: {
    fontSize: 17,
    fontWeight: '700',
    marginBottom: 12,
    textAlign: 'center',
    color: '#1f2937',
  },
  correctAnswerBox: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginTop: 8,
    width: '100%',
  },
  correctAnswerLabel: {
    fontSize: 13,
    color: '#6b7280',
    fontWeight: '600',
    marginBottom: 4,
  },
  correctAnswerText: {
    fontSize: 16,
    color: '#1f2937',
    fontWeight: '700',
  },
  solutionButton: {
    borderRadius: 12,
    overflow: 'hidden',
    marginTop: 16,
    width: '100%',
  },
  solutionGradient: {
    padding: 14,
    alignItems: 'center',
  },
  solutionButtonText: {
    color: 'white',
    fontSize: 15,
    fontWeight: '700',
  },
  nextButton: {
    backgroundColor: '#667eea',
    padding: 14,
    borderRadius: 12,
    marginTop: 12,
    width: '100%',
    alignItems: 'center',
  },
  nextButtonText: {
    color: 'white',
    fontSize: 15,
    fontWeight: '700',
  },
  navigationButtons: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    gap: 12,
  },
  navButton: {
    flex: 1,
    backgroundColor: 'white',
    padding: 18,
    borderRadius: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  navButtonDisabled: {
    opacity: 0.4,
  },
  navButtonText: {
    color: '#667eea',
    fontSize: 16,
    fontWeight: '700',
  },

  // Modal styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: 'white',
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
    maxHeight: '90%',
    padding: 24,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: '800',
    color: '#1f2937',
  },
  closeButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeButtonText: {
    fontSize: 24,
    color: '#6b7280',
    lineHeight: 26,
  },
  formulaBox: {
    backgroundColor: '#eff6ff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 20,
    borderLeftWidth: 4,
    borderLeftColor: '#3b82f6',
  },
  formulaLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: '#3b82f6',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  formulaText: {
    fontSize: 16,
    color: '#1e40af',
    fontWeight: '600',
    fontFamily: 'monospace',
  },
  stepsContainer: {
    marginBottom: 20,
  },
  stepsTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#1f2937',
    marginBottom: 16,
  },
  stepCard: {
    marginBottom: 16,
    backgroundColor: '#f9fafb',
    borderRadius: 12,
    padding: 16,
    borderLeftWidth: 3,
    borderLeftColor: '#667eea',
  },
  stepCardVisible: {
    opacity: 1,
  },
  stepCardHidden: {
    opacity: 0.3,
  },
  stepHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  stepNumber: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#667eea',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  stepNumberText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '700',
  },
  stepAction: {
    flex: 1,
    fontSize: 15,
    color: '#4b5563',
    fontWeight: '600',
  },
  stepResultBox: {
    backgroundColor: 'white',
    padding: 12,
    borderRadius: 8,
    marginLeft: 40,
  },
  stepResult: {
    fontSize: 16,
    color: '#1f2937',
    fontWeight: '700',
    fontFamily: 'monospace',
  },
  stepNavigation: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  stepNavButton: {
    padding: 10,
  },
  stepNavButtonDisabled: {
    opacity: 0.3,
  },
  stepNavButtonText: {
    color: '#667eea',
    fontSize: 14,
    fontWeight: '600',
  },
  stepCounter: {
    fontSize: 14,
    color: '#6b7280',
    fontWeight: '600',
  },
  showAllButton: {
    backgroundColor: '#f3f4f6',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 8,
  },
  showAllButtonText: {
    color: '#6b7280',
    fontSize: 14,
    fontWeight: '600',
  },
  explanationBox: {
    backgroundColor: '#f0fdf4',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#22c55e',
  },
  explanationLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: '#16a34a',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  explanationText: {
    fontSize: 15,
    color: '#166534',
    lineHeight: 22,
  },
  finalAnswerBox: {
    backgroundColor: '#667eea',
    padding: 20,
    borderRadius: 16,
    alignItems: 'center',
  },
  finalAnswerLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: 'rgba(255,255,255,0.8)',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  finalAnswerText: {
    fontSize: 28,
    color: 'white',
    fontWeight: '800',
  },
});
