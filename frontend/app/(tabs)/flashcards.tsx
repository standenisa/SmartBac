import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, ScrollView, Dimensions, Modal } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Animated, { useSharedValue, useAnimatedStyle, withSpring, interpolate } from 'react-native-reanimated';
import { Ionicons } from '@expo/vector-icons';
import { DUO } from '@/constants/duo';
import { TYPO } from '@/constants/typography';
import AnimatedPressable from '@/components/AnimatedPressable';

const { width } = Dimensions.get('window');

interface Flashcard {
  id: string; front: string; back: string; category: string;
  nextReview: number; interval: number; easeFactor: number; reviewCount: number;
}
interface Category { id: string; name: string; icon: keyof typeof Ionicons.glyphMap; color: [string, string]; }

const CATEGORIES: Category[] = [
  { id: 'algebra', name: 'Algebra', icon: 'grid', color: [DUO.purple, DUO.purpleDark] },
  { id: 'analysis', name: 'Analiza', icon: 'trending-up', color: [DUO.blue, DUO.blueDark] },
  { id: 'geometry', name: 'Geometrie', icon: 'triangle', color: [DUO.green, DUO.greenDark] },
  { id: 'trigonometry', name: 'Trigonometrie', icon: 'pulse', color: [DUO.orange, DUO.orangeDark] },
];

const DEFAULT_FLASHCARDS: Flashcard[] = [
  { id: '1', front: 'Formula pentru ecuatia de gradul 2', back: 'x = (-b ± √(b²-4ac)) / 2a\n\nUnde ax² + bx + c = 0', category: 'algebra', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '2', front: 'Suma solutiilor ecuatiei de gradul 2', back: 'x₁ + x₂ = -b/a\n\n(Relatiile lui Viete)', category: 'algebra', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '3', front: 'Produsul solutiilor ecuatiei de gradul 2', back: 'x₁ · x₂ = c/a\n\n(Relatiile lui Viete)', category: 'algebra', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '4', front: 'Progresia aritmetica - termenul general', back: 'aₙ = a₁ + (n-1)·r\n\nUnde r este ratia', category: 'algebra', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '5', front: 'Progresia geometrica - termenul general', back: 'bₙ = b₁ · qⁿ⁻¹\n\nUnde q este ratia', category: 'algebra', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '6', front: 'Derivata functiei xⁿ', back: '(xⁿ)\' = n·xⁿ⁻¹', category: 'analysis', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '7', front: 'Derivata functiei sin(x)', back: '(sin x)\' = cos x', category: 'analysis', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '8', front: 'Derivata functiei cos(x)', back: '(cos x)\' = -sin x', category: 'analysis', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '9', front: 'Derivata functiei eˣ', back: '(eˣ)\' = eˣ', category: 'analysis', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '10', front: 'Derivata functiei ln(x)', back: '(ln x)\' = 1/x', category: 'analysis', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '11', front: 'Integrala functiei xⁿ', back: '∫xⁿdx = xⁿ⁺¹/(n+1) + C\n\n(pentru n ≠ -1)', category: 'analysis', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '12', front: 'Integrala functiei 1/x', back: '∫(1/x)dx = ln|x| + C', category: 'analysis', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '13', front: 'Integrala functiei eˣ', back: '∫eˣdx = eˣ + C', category: 'analysis', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '14', front: 'Formula lui Leibniz-Newton', back: '∫ₐᵇf(x)dx = F(b) - F(a)\n\nUnde F este primitiva lui f', category: 'analysis', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '15', front: 'Teorema lui Pitagora', back: 'a² + b² = c²\n\nUnde c este ipotenuza', category: 'geometry', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '16', front: 'Aria triunghiului', back: 'A = (b·h)/2\n\nsau A = (a·b·sin C)/2', category: 'geometry', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '17', front: 'Volumul sferei', back: 'V = (4/3)·π·r³', category: 'geometry', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '18', front: 'Aria sferei', back: 'A = 4·π·r²', category: 'geometry', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '19', front: 'Distanta dintre doua puncte', back: 'd = √[(x₂-x₁)² + (y₂-y₁)²]', category: 'geometry', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '20', front: 'Identitatea fundamentala', back: 'sin²x + cos²x = 1', category: 'trigonometry', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '21', front: 'sin(2x) =', back: 'sin(2x) = 2·sin(x)·cos(x)', category: 'trigonometry', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '22', front: 'cos(2x) =', back: 'cos(2x) = cos²x - sin²x\n= 2cos²x - 1\n= 1 - 2sin²x', category: 'trigonometry', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '23', front: 'Teorema sinusurilor', back: 'a/sin A = b/sin B = c/sin C = 2R', category: 'trigonometry', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '24', front: 'Teorema cosinusului', back: 'c² = a² + b² - 2ab·cos C', category: 'trigonometry', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
];

export default function FlashcardsScreen() {
  const [flashcards, setFlashcards] = useState<Flashcard[]>(DEFAULT_FLASHCARDS);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [isStudying, setIsStudying] = useState(false);
  const [studyCards, setStudyCards] = useState<Flashcard[]>([]);
  const [cardsReviewed, setCardsReviewed] = useState(0);
  const [showStats, setShowStats] = useState(false);
  const flipProgress = useSharedValue(0);

  useEffect(() => { loadFlashcards(); }, []);

  const loadFlashcards = async () => {
    try { const stored = await AsyncStorage.getItem('flashcards'); if (stored) setFlashcards(JSON.parse(stored)); } catch (e) { console.log('Error:', e); }
  };

  const saveFlashcards = async (cards: Flashcard[]) => {
    try { await AsyncStorage.setItem('flashcards', JSON.stringify(cards)); } catch (e) { console.log('Error:', e); }
  };

  const getCategoryCards = (id: string) => flashcards.filter(c => c.category === id);
  const getDueCards = (id?: string) => {
    const now = Date.now();
    let cards = flashcards.filter(c => c.nextReview <= now);
    if (id) cards = cards.filter(c => c.category === id);
    return cards.sort((a, b) => a.nextReview - b.nextReview);
  };

  const startStudySession = (id?: string) => {
    const dueCards = getDueCards(id);
    const allCards = id ? getCategoryCards(id) : flashcards;
    setStudyCards(dueCards.length > 0 ? dueCards : allCards);
    setCurrentIndex(0); setCardsReviewed(0); setIsFlipped(false); setIsStudying(true);
    flipProgress.value = 0;
  };

  const flipCard = () => {
    flipProgress.value = withSpring(isFlipped ? 0 : 1, { damping: 15, stiffness: 120 });
    setIsFlipped(!isFlipped);
  };

  const rateCard = (quality: number) => {
    const card = studyCards[currentIndex];
    let { easeFactor, interval, reviewCount } = card;
    if (quality < 3) { interval = 1; }
    else {
      if (reviewCount === 0) interval = 1;
      else if (reviewCount === 1) interval = 6;
      else interval = Math.round(interval * easeFactor);
      easeFactor = easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
      if (easeFactor < 1.3) easeFactor = 1.3;
    }
    const nextReview = Date.now() + interval * 24 * 60 * 60 * 1000;
    const updatedCard: Flashcard = { ...card, easeFactor, interval, nextReview, reviewCount: reviewCount + 1 };
    const updatedFlashcards = flashcards.map(c => c.id === card.id ? updatedCard : c);
    setFlashcards(updatedFlashcards); saveFlashcards(updatedFlashcards); setCardsReviewed(cardsReviewed + 1);
    if (currentIndex < studyCards.length - 1) {
      setCurrentIndex(currentIndex + 1); setIsFlipped(false);
      flipProgress.value = 0;
    }
    else setShowStats(true);
  };

  const finishSession = () => { setIsStudying(false); setShowStats(false); setCurrentIndex(0); setCardsReviewed(0); flipProgress.value = 0; };

  const frontStyle = useAnimatedStyle(() => ({
    transform: [{ perspective: 1000 }, { rotateY: `${interpolate(flipProgress.value, [0, 1], [0, 180])}deg` }],
    backfaceVisibility: 'hidden' as const,
  }));

  const backStyle = useAnimatedStyle(() => ({
    transform: [{ perspective: 1000 }, { rotateY: `${interpolate(flipProgress.value, [0, 1], [180, 360])}deg` }],
    backfaceVisibility: 'hidden' as const,
  }));

  const categories = CATEGORIES.map(cat => ({ ...cat, cardCount: getCategoryCards(cat.id).length, dueCount: getDueCards(cat.id).length }));
  const totalDue = getDueCards().length;

  if (isStudying && studyCards.length > 0) {
    const currentCard = studyCards[currentIndex];
    return (
      <View style={styles.container}>
        <LinearGradient colors={[DUO.bgLight, DUO.bg]} style={styles.studyGradient}>
          <View style={styles.studyHeader}>
            <TouchableOpacity onPress={finishSession}><Ionicons name="close" size={24} color={DUO.white} /></TouchableOpacity>
            <Text style={styles.progressText}>{currentIndex + 1} / {studyCards.length}</Text>
            <View style={{ width: 40 }} />
          </View>
          <View style={styles.studyProgressBar}>
            <LinearGradient colors={[DUO.purple, DUO.purpleDark]} style={[styles.studyProgressFill, { width: `${((currentIndex + 1) / studyCards.length) * 100}%` }]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} />
          </View>
          <TouchableOpacity style={styles.cardContainer} onPress={flipCard} activeOpacity={0.9}>
            <Animated.View style={[styles.card, styles.cardFront, frontStyle]}>
              <LinearGradient colors={[DUO.card, DUO.cardDark]} style={styles.cardGradient}>
                <Text style={[styles.cardLabel, TYPO.caption]}>INTREBARE</Text>
                <Text style={styles.cardText}>{currentCard.front}</Text>
                <Text style={styles.tapHint}>Atinge pentru a vedea raspunsul</Text>
              </LinearGradient>
            </Animated.View>
            <Animated.View style={[styles.card, styles.cardBack, backStyle]}>
              <LinearGradient colors={[DUO.purple, DUO.purpleDark]} style={styles.cardGradient}>
                <Text style={[styles.cardLabel, TYPO.caption]}>RASPUNS</Text>
                <Text style={styles.cardText}>{currentCard.back}</Text>
              </LinearGradient>
            </Animated.View>
          </TouchableOpacity>
          {isFlipped && (
            <View style={styles.ratingContainer}>
              <Text style={[styles.ratingLabel, TYPO.label]}>Cat de bine ai stiut?</Text>
              <View style={styles.ratingButtons}>
                <TouchableOpacity style={[styles.ratingButton, { backgroundColor: DUO.red }]} onPress={() => rateCard(1)}>
                  <Ionicons name="sad" size={24} color={DUO.white} /><Text style={styles.ratingText}>Greu</Text>
                </TouchableOpacity>
                <TouchableOpacity style={[styles.ratingButton, { backgroundColor: DUO.orange }]} onPress={() => rateCard(3)}>
                  <Ionicons name="help-circle" size={24} color={DUO.white} /><Text style={styles.ratingText}>OK</Text>
                </TouchableOpacity>
                <TouchableOpacity style={[styles.ratingButton, { backgroundColor: DUO.green }]} onPress={() => rateCard(5)}>
                  <Ionicons name="happy" size={24} color={DUO.white} /><Text style={styles.ratingText}>Usor</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
        </LinearGradient>
        <Modal visible={showStats} animationType="fade" transparent>
          <View style={styles.modalOverlay}>
            <View style={styles.statsModal}>
              <Ionicons name="ribbon" size={64} color={DUO.yellow} style={{ marginBottom: 16 }} />
              <Text style={[styles.statsTitle, TYPO.heading2]}>Sesiune Completa!</Text>
              <Text style={styles.statsText}>Ai revizuit {cardsReviewed} carduri</Text>
              <TouchableOpacity style={styles.statsButton} onPress={finishSession}>
                <LinearGradient colors={[DUO.purple, DUO.purpleDark]} style={styles.statsButtonGradient}>
                  <Text style={styles.statsButtonText}>Inapoi</Text>
                </LinearGradient>
              </TouchableOpacity>
            </View>
          </View>
        </Modal>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        <LinearGradient colors={[DUO.purple, DUO.purpleDark]} style={styles.header} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }}>
          <Text style={[styles.headerTitle, TYPO.heading1]}>Flashcards</Text>
          <Text style={styles.headerSubtitle}>Spaced repetition learning</Text>
        </LinearGradient>

        {totalDue > 0 && (
          <AnimatedPressable style={styles.dueBanner} onPress={() => startStudySession()}>
            <View style={styles.dueContent}>
              <Ionicons name="book" size={32} color={DUO.yellow} />
              <View><Text style={styles.dueTitle}>{totalDue} carduri de revizuit</Text><Text style={styles.dueSubtitle}>Incepe sesiunea acum!</Text></View>
            </View>
            <Ionicons name="arrow-forward" size={24} color={DUO.yellow} />
          </AnimatedPressable>
        )}

        <AnimatedPressable style={styles.quickStartButton} onPress={() => startStudySession()}>
          <LinearGradient colors={[DUO.green, DUO.greenDark]} style={styles.quickStartGradient}>
            <Ionicons name="rocket" size={24} color={DUO.white} />
            <Text style={styles.quickStartText}>Start Quick Review</Text>
          </LinearGradient>
        </AnimatedPressable>

        <View style={styles.section}>
          <Text style={[styles.sectionTitle, TYPO.heading3]}>Categorii</Text>
          <View style={styles.categoriesGrid}>
            {categories.map((cat) => (
              <AnimatedPressable key={cat.id} style={styles.categoryCard} onPress={() => startStudySession(cat.id)}>
                <LinearGradient colors={cat.color} style={styles.categoryGradient}>
                  <Ionicons name={cat.icon} size={32} color={DUO.white} />
                  <Text style={styles.categoryName}>{cat.name}</Text>
                  <Text style={styles.categoryCount}>{cat.cardCount} carduri</Text>
                  {cat.dueCount > 0 && (<View style={styles.dueBadge}><Text style={styles.dueBadgeText}>{cat.dueCount}</Text></View>)}
                </LinearGradient>
              </AnimatedPressable>
            ))}
          </View>
        </View>

        <View style={styles.infoCard}>
          <Text style={[styles.infoTitle, TYPO.subheading]}>Cum functioneaza?</Text>
          <Text style={styles.infoText}>
            1. Cardurile apar in functie de cat de bine le stii{'\n'}
            2. Cele dificile apar mai des{'\n'}
            3. Cele usoare apar mai rar{'\n'}
            4. Sistemul se adapteaza la tine!
          </Text>
        </View>
        <View style={{ height: 100 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  header: { paddingTop: 60, paddingBottom: 30, paddingHorizontal: 24, borderBottomLeftRadius: 30, borderBottomRightRadius: 30 },
  headerTitle: { color: DUO.white, marginBottom: 4 },
  headerSubtitle: { fontSize: 14, color: 'rgba(255,255,255,0.9)' },
  dueBanner: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginHorizontal: 20, marginTop: -15, backgroundColor: DUO.yellow + '20', padding: 16, borderRadius: DUO.radiusLg, borderWidth: 1, borderColor: DUO.yellow + '30' },
  dueContent: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  dueTitle: { fontSize: 16, fontWeight: '700', color: DUO.yellow },
  dueSubtitle: { fontSize: 12, color: DUO.textSecondary },
  quickStartButton: { marginHorizontal: 20, marginTop: 16, borderRadius: DUO.radiusLg, overflow: 'hidden' },
  quickStartGradient: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', padding: 18, gap: 12 },
  quickStartText: { fontSize: 18, fontWeight: '700', color: DUO.white },
  section: { padding: 20 },
  sectionTitle: { color: DUO.textPrimary, marginBottom: 16 },
  categoriesGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  categoryCard: { width: (width - 52) / 2, borderRadius: DUO.radiusLg, overflow: 'hidden' },
  categoryGradient: { padding: 20, minHeight: 120 },
  categoryName: { fontSize: 16, fontWeight: '700', color: DUO.white, marginBottom: 4 },
  categoryCount: { fontSize: 12, color: 'rgba(255,255,255,0.8)' },
  dueBadge: { position: 'absolute', top: 12, right: 12, backgroundColor: DUO.red, width: 24, height: 24, borderRadius: 12, justifyContent: 'center', alignItems: 'center' },
  dueBadgeText: { color: DUO.white, fontSize: 12, fontWeight: '700' },
  infoCard: { marginHorizontal: 20, backgroundColor: DUO.card, padding: 20, borderRadius: DUO.radiusLg, borderWidth: 1, borderColor: DUO.surface },
  infoTitle: { color: DUO.textPrimary, marginBottom: 12 },
  infoText: { fontSize: 14, color: DUO.textSecondary, lineHeight: 24 },
  studyGradient: { flex: 1, paddingTop: 60 },
  studyHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 20, marginBottom: 16 },
  progressText: { fontSize: 16, fontWeight: '600', color: DUO.white },
  studyProgressBar: { height: 4, backgroundColor: DUO.surface, marginHorizontal: 20, borderRadius: 2, overflow: 'hidden', marginBottom: 30 },
  studyProgressFill: { height: '100%', borderRadius: 2 },
  cardContainer: { flex: 1, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 20 },
  card: { width: width - 40, height: 300, borderRadius: 24 },
  cardFront: { position: 'absolute' },
  cardBack: { position: 'absolute' },
  cardGradient: { flex: 1, borderRadius: 24, padding: 24, justifyContent: 'center', alignItems: 'center' },
  cardLabel: { color: 'rgba(255,255,255,0.6)', marginBottom: 16 },
  cardText: { fontSize: 22, fontWeight: '600', color: DUO.white, textAlign: 'center', lineHeight: 32 },
  tapHint: { position: 'absolute', bottom: 24, fontSize: 12, color: 'rgba(255,255,255,0.5)' },
  ratingContainer: { padding: 20, alignItems: 'center' },
  ratingLabel: { color: DUO.textSecondary, marginBottom: 16 },
  ratingButtons: { flexDirection: 'row', gap: 12 },
  ratingButton: { paddingVertical: 16, paddingHorizontal: 24, borderRadius: 16, alignItems: 'center', minWidth: 90 },
  ratingText: { fontSize: 14, fontWeight: '600', color: DUO.white },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.8)', justifyContent: 'center', alignItems: 'center' },
  statsModal: { backgroundColor: DUO.card, borderRadius: 24, padding: 32, alignItems: 'center', marginHorizontal: 40, borderWidth: 1, borderColor: DUO.surface },
  statsTitle: { color: DUO.textPrimary, marginBottom: 8 },
  statsText: { fontSize: 16, color: DUO.textSecondary, marginBottom: 24 },
  statsButton: { borderRadius: 16, overflow: 'hidden' },
  statsButtonGradient: { paddingHorizontal: 40, paddingVertical: 14 },
  statsButtonText: { fontSize: 16, fontWeight: '700', color: DUO.white },
});
