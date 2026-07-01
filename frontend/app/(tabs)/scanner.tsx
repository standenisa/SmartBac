import { useState } from 'react';
import {
  StyleSheet, View, Text, TextInput, ScrollView, Image,
  ActivityIndicator, Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import Animated, { FadeInDown } from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as ImagePicker from 'expo-image-picker';
import { apiUpload, apiPost } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import { TYPO } from '@/constants/typography';
import AnimatedPressable from '@/components/AnimatedPressable';
import StructuredSolutionView, { StructuredSolution } from '@/components/SolutionView';

type Phase = 'capture' | 'review' | 'solution';

interface SolverResponse {
  answer: string;
  steps: string[];
  model_used: string;
  structured?: StructuredSolution | null;
}

export default function ScannerScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const [phase, setPhase] = useState<Phase>('capture');
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [extractedText, setExtractedText] = useState('');
  const [ocrConfidence, setOcrConfidence] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [solution, setSolution] = useState<SolverResponse | null>(null);
  const [error, setError] = useState('');

  const pickImage = async (useCamera: boolean) => {
    try {
      const permissionFn = useCamera
        ? ImagePicker.requestCameraPermissionsAsync
        : ImagePicker.requestMediaLibraryPermissionsAsync;

      const { status } = await permissionFn();
      if (status !== 'granted') {
        Alert.alert('Permisiune necesara', 'Permite accesul pentru a putea scana exercitii.');
        return;
      }

      const launchFn = useCamera
        ? ImagePicker.launchCameraAsync
        : ImagePicker.launchImageLibraryAsync;

      const result = await launchFn({
        mediaTypes: ['images'],
        quality: 0.8,
        allowsEditing: true,
      });

      if (!result.canceled && result.assets[0]) {
        const uri = result.assets[0].uri;
        setImageUri(uri);
        setError('');
        await runOCR(uri);
      }
    } catch {
      setError('Eroare la selectarea imaginii.');
    }
  };

  const runOCR = async (uri: string) => {
    setIsLoading(true);
    setLoadingMessage('Se extrage textul din imagine...');
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', {
        uri,
        type: 'image/jpeg',
        name: 'exercise.jpg',
      } as any);

      const data = await apiUpload<any>('/api/scanner/ocr', formData);

      if (data.success) {
        setExtractedText(data.extracted_text);
        setOcrConfidence(data.confidence);
        setPhase('review');
      } else {
        setError(data.message || 'Nu am detectat text. Incearca o poza mai clara.');
      }
    } catch (e: any) {
      setError(e.message || 'Eroare la conectarea cu serverul.');
    }

    setIsLoading(false);
    setLoadingMessage('');
  };

  const solveExercise = async () => {
    if (!extractedText.trim()) return;

    setIsLoading(true);
    setLoadingMessage('Se rezolvă cu DeepSeek R1...');
    setError('');

    try {
      const data = await apiPost<any>('/api/scanner/solve-text', {
        question: extractedText.trim(),
        user_id: user?.id,
      });

      if (data.success) {
        setSolution({
          answer: data.answer || '',
          steps: data.steps || [],
          model_used: data.model_used || 'smartbac',
          structured: data.structured || null,
        });
        setPhase('solution');
      } else {
        setError('Nu am putut rezolva exercițiul.');
      }
    } catch (e: any) {
      setError(e.message || 'Eroare la rezolvarea exercitiului.');
    }

    setIsLoading(false);
    setLoadingMessage('');
  };

  const reset = () => {
    setPhase('capture');
    setImageUri(null);
    setExtractedText('');
    setSolution(null);
    setError('');
    setOcrConfidence(0);
  };

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      {/* Header */}
      <LinearGradient colors={[DUO.card, DUO.bg]} style={styles.header}>
        <Text style={styles.headerEmoji}>📷</Text>
        <View>
          <Text style={[styles.headerTitle, TYPO.heading3]}>Photo Scanner</Text>
          <Text style={[styles.headerSub, TYPO.label]}>Scaneaza si rezolva exercitii</Text>
        </View>
      </LinearGradient>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentInner}>
        {/* ── CAPTURE PHASE ── */}
        {phase === 'capture' && (
          <Animated.View entering={FadeInDown.duration(400)} style={styles.captureContainer}>
            <View style={styles.instructionCard}>
              <Text style={styles.instructionEmoji}>🎯</Text>
              <Text style={styles.instructionTitle}>Cum functioneaza</Text>
              <Text style={styles.instructionText}>
                1. Fotografiaza un exercitiu de matematica{'\n'}
                2. Textul este extras automat (OCR){'\n'}
                3. Editezi daca e nevoie{'\n'}
                4. AI-ul rezolva pas cu pas
              </Text>
            </View>

            <AnimatedPressable style={styles.captureButton} onPress={() => pickImage(true)}>
              <LinearGradient
                colors={[DUO.cyan, DUO.cyanDark]}
                style={styles.captureButtonInner}
              >
                <Text style={styles.captureButtonEmoji}>📷</Text>
                <Text style={styles.captureButtonText}>Fotografiaza exercitiu</Text>
              </LinearGradient>
            </AnimatedPressable>

            <AnimatedPressable style={styles.galleryButton} onPress={() => pickImage(false)}>
              <Text style={styles.galleryButtonEmoji}>🖼️</Text>
              <Text style={styles.galleryButtonText}>Alege din galerie</Text>
            </AnimatedPressable>

            {error ? (
              <Animated.View entering={FadeInDown.duration(300)} style={styles.errorCard}>
                <Text style={styles.errorText}>{error}</Text>
              </Animated.View>
            ) : null}
          </Animated.View>
        )}

        {/* ── REVIEW PHASE ── */}
        {phase === 'review' && (
          <Animated.View entering={FadeInDown.duration(400)} style={styles.reviewContainer}>
            {imageUri && (
              <View style={styles.previewCard}>
                <Image source={{ uri: imageUri }} style={styles.previewImage} resizeMode="contain" />
              </View>
            )}

            <View style={styles.ocrResultCard}>
              <View style={styles.ocrHeader}>
                <Text style={styles.ocrLabel}>Text extras</Text>
                {ocrConfidence > 0 && (
                  <View style={[
                    styles.confidenceBadge,
                    { backgroundColor: ocrConfidence > 0.8 ? DUO.green + '20' : DUO.orange + '20' },
                  ]}>
                    <Text style={[
                      styles.confidenceText,
                      { color: ocrConfidence > 0.8 ? DUO.green : DUO.orange },
                    ]}>
                      {Math.round(ocrConfidence * 100)}% acuratete
                    </Text>
                  </View>
                )}
              </View>

              <TextInput
                style={styles.ocrTextInput}
                value={extractedText}
                onChangeText={setExtractedText}
                multiline
                placeholder="Textul extras va aparea aici..."
                placeholderTextColor={DUO.textMuted}
              />

              <Text style={styles.editHint}>Editeaza textul daca OCR-ul a gresit ceva</Text>
            </View>

            <AnimatedPressable style={styles.solveButton} onPress={solveExercise}>
              <LinearGradient
                colors={[DUO.green, DUO.greenDark]}
                style={styles.solveButtonInner}
              >
                <Text style={styles.solveButtonEmoji}>🧠</Text>
                <Text style={styles.solveButtonText}>Rezolvă cu DeepSeek R1</Text>
              </LinearGradient>
            </AnimatedPressable>

            <AnimatedPressable style={styles.backButton} onPress={reset}>
              <Text style={styles.backButtonText}>← Inapoi la camera</Text>
            </AnimatedPressable>

            {error ? (
              <Animated.View entering={FadeInDown.duration(300)} style={styles.errorCard}>
                <Text style={styles.errorText}>{error}</Text>
              </Animated.View>
            ) : null}
          </Animated.View>
        )}

        {/* ── SOLUTION PHASE ── */}
        {phase === 'solution' && solution && (
          <Animated.View entering={FadeInDown.duration(400)} style={styles.solutionContainer}>
            <View style={styles.questionCard}>
              <Text style={styles.questionLabel}>Exercitiu</Text>
              <Text style={styles.questionText}>{extractedText}</Text>
            </View>

            <View style={styles.solutionCard}>
              <View style={styles.solutionHeader}>
                <Text style={styles.solutionHeaderEmoji}>✅</Text>
                <Text style={styles.solutionHeaderText}>Solutie</Text>
                <View style={styles.modelBadge}>
                  <Text style={styles.modelBadgeText}>{solution.model_used}</Text>
                </View>
              </View>

              {solution.structured && solution.structured.tip && solution.structured.tip !== 'Nerecunoscut' ? (
                <StructuredSolutionView sol={solution.structured} />
              ) : (
                <View style={styles.plainSolution}>
                  {solution.answer ? (
                    <View style={styles.answerBox}>
                      <Text style={styles.answerLabel}>Raspuns</Text>
                      <Text style={styles.answerText}>{solution.answer}</Text>
                    </View>
                  ) : null}

                  {solution.steps && solution.steps.length > 0 && (
                    <View style={styles.stepsBox}>
                      <Text style={styles.stepsLabel}>Pasi</Text>
                      {solution.steps.map((step, i) => (
                        <View key={i} style={styles.stepRow}>
                          <View style={styles.stepNumber}>
                            <Text style={styles.stepNumberText}>{i + 1}</Text>
                          </View>
                          <Text style={styles.stepText}>{step}</Text>
                        </View>
                      ))}
                    </View>
                  )}
                </View>
              )}
            </View>

            <AnimatedPressable style={styles.newScanButton} onPress={reset}>
              <LinearGradient
                colors={[DUO.cyan, DUO.cyanDark]}
                style={styles.newScanButtonInner}
              >
                <Text style={styles.newScanButtonEmoji}>📷</Text>
                <Text style={styles.newScanButtonText}>Scaneaza alt exercitiu</Text>
              </LinearGradient>
            </AnimatedPressable>
          </Animated.View>
        )}
      </ScrollView>

      {/* Loading overlay */}
      {isLoading && (
        <View style={styles.loadingOverlay}>
          <View style={styles.loadingCard}>
            <ActivityIndicator size="large" color={DUO.cyan} />
            <Text style={styles.loadingText}>{loadingMessage}</Text>
          </View>
        </View>
      )}
    </View>
  );
}

// ── Styles ──

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },

  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingBottom: 14,
    paddingHorizontal: 20,
    gap: 12,
    borderBottomWidth: 1,
    borderBottomColor: DUO.surface,
  },
  headerEmoji: { fontSize: 32 },
  headerTitle: { color: DUO.textPrimary },
  headerSub: { color: DUO.textSecondary },

  content: { flex: 1 },
  contentInner: { padding: 20, paddingBottom: 40 },

  // ── Capture ──
  captureContainer: { gap: 16 },
  instructionCard: {
    backgroundColor: DUO.card,
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: DUO.surface,
    alignItems: 'center',
    gap: 8,
  },
  instructionEmoji: { fontSize: 36 },
  instructionTitle: { fontSize: 18, fontWeight: '800', color: DUO.textPrimary },
  instructionText: { fontSize: 14, fontWeight: '600', color: DUO.textSecondary, lineHeight: 22, textAlign: 'center' },

  captureButton: { borderRadius: 16, overflow: 'hidden' },
  captureButtonInner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 18,
    gap: 10,
    borderRadius: 16,
  },
  captureButtonEmoji: { fontSize: 24 },
  captureButtonText: { fontSize: 17, fontWeight: '800', color: DUO.white },

  galleryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    gap: 10,
    backgroundColor: DUO.card,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: DUO.surface,
  },
  galleryButtonEmoji: { fontSize: 20 },
  galleryButtonText: { fontSize: 15, fontWeight: '700', color: DUO.textPrimary },

  // ── Review ──
  reviewContainer: { gap: 16 },
  previewCard: {
    backgroundColor: DUO.card,
    borderRadius: 16,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: DUO.surface,
  },
  previewImage: { width: '100%', height: 200 },

  ocrResultCard: {
    backgroundColor: DUO.card,
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: DUO.surface,
    gap: 8,
  },
  ocrHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  ocrLabel: { fontSize: 14, fontWeight: '800', color: DUO.textPrimary },
  confidenceBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 999 },
  confidenceText: { fontSize: 12, fontWeight: '700' },
  ocrTextInput: {
    backgroundColor: DUO.surface,
    borderRadius: 12,
    padding: 14,
    fontSize: 15,
    fontWeight: '600',
    color: DUO.textPrimary,
    minHeight: 100,
    textAlignVertical: 'top',
    borderWidth: 1,
    borderColor: DUO.surfaceLight,
  },
  editHint: { fontSize: 12, fontWeight: '600', color: DUO.textMuted, textAlign: 'center' },

  solveButton: { borderRadius: 16, overflow: 'hidden' },
  solveButtonInner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 18,
    gap: 10,
    borderRadius: 16,
  },
  solveButtonEmoji: { fontSize: 22 },
  solveButtonText: { fontSize: 17, fontWeight: '800', color: DUO.white },

  backButton: { alignItems: 'center', padding: 12 },
  backButtonText: { fontSize: 14, fontWeight: '700', color: DUO.textMuted },

  // ── Solution ──
  solutionContainer: { gap: 16 },
  questionCard: {
    backgroundColor: DUO.cyan + '12',
    borderRadius: 14,
    padding: 14,
    borderWidth: 1,
    borderColor: DUO.cyan + '25',
  },
  questionLabel: { fontSize: 11, fontWeight: '800', color: DUO.cyan, marginBottom: 4 },
  questionText: { fontSize: 14, fontWeight: '600', color: DUO.textPrimary, lineHeight: 20 },

  solutionCard: {
    backgroundColor: DUO.card,
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: DUO.surface,
    gap: 12,
  },
  solutionHeader: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  solutionHeaderEmoji: { fontSize: 20 },
  solutionHeaderText: { fontSize: 16, fontWeight: '800', color: DUO.textPrimary, flex: 1 },
  modelBadge: {
    backgroundColor: DUO.purple + '20',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 999,
  },
  modelBadgeText: { fontSize: 10, fontWeight: '800', color: DUO.purple },

  plainSolution: { gap: 12 },
  answerBox: {
    backgroundColor: DUO.green + '15',
    borderRadius: 12,
    padding: 12,
    borderWidth: 1,
    borderColor: DUO.green + '30',
  },
  answerLabel: { fontSize: 11, fontWeight: '800', color: DUO.green, marginBottom: 4 },
  answerText: { fontSize: 16, fontWeight: '800', color: DUO.green },

  stepsBox: { gap: 8 },
  stepsLabel: { fontSize: 12, fontWeight: '800', color: DUO.textSecondary },
  stepRow: { flexDirection: 'row', alignItems: 'flex-start', gap: 10 },
  stepNumber: {
    width: 24, height: 24, borderRadius: 12,
    backgroundColor: DUO.cyan, justifyContent: 'center', alignItems: 'center',
    marginTop: 1,
  },
  stepNumberText: { fontSize: 12, fontWeight: '800', color: DUO.white },
  stepText: { flex: 1, fontSize: 14, fontWeight: '600', color: DUO.textPrimary, lineHeight: 20 },

  newScanButton: { borderRadius: 16, overflow: 'hidden' },
  newScanButtonInner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 18,
    gap: 10,
    borderRadius: 16,
  },
  newScanButtonEmoji: { fontSize: 22 },
  newScanButtonText: { fontSize: 16, fontWeight: '800', color: DUO.white },

  // ── Error ──
  errorCard: {
    backgroundColor: DUO.red + '12',
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    borderColor: DUO.red + '25',
  },
  errorText: { fontSize: 14, fontWeight: '600', color: DUO.red, textAlign: 'center' },

  // ── Loading ──
  loadingOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(15, 23, 42, 0.85)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingCard: {
    backgroundColor: DUO.card,
    borderRadius: 20,
    padding: 30,
    alignItems: 'center',
    gap: 16,
    borderWidth: 1,
    borderColor: DUO.surface,
  },
  loadingText: { fontSize: 14, fontWeight: '700', color: DUO.textSecondary },
});
