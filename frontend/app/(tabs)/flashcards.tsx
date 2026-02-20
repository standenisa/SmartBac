import { useState, useEffect, useRef } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Animated,
  Dimensions,
  Modal
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import AsyncStorage from '@react-native-async-storage/async-storage';

const { width, height } = Dimensions.get('window');

interface Flashcard {
  id: string;
  front: string;
  back: string;
  category: string;
  difficulty: 'easy' | 'medium' | 'hard';
  nextReview: number;
  interval: number;
  easeFactor: number;
  reviewCount: number;
}

interface Category {
  id: string;
  name: string;
  emoji: string;
  color: [string, string];
  cardCount: number;
}

const CATEGORIES: Category[] = [
  { id: 'algebra', name: 'Algebră', emoji: '🔢', color: ['#8b5cf6', '#7c3aed'], cardCount: 0 },
  { id: 'analysis', name: 'Analiză', emoji: '📈', color: ['#3b82f6', '#2563eb'], cardCount: 0 },
  { id: 'geometry', name: 'Geometrie', emoji: '📐', color: ['#10b981', '#059669'], cardCount: 0 },
  { id: 'trigonometry', name: 'Trigonometrie', emoji: '📊', color: ['#f59e0b', '#d97706'], cardCount: 0 },
];

const DEFAULT_FLASHCARDS: Flashcard[] = [
  // Algebra
  { id: '1', front: 'Formula pentru ecuația de gradul 2', back: 'x = (-b ± √(b²-4ac)) / 2a\n\nUnde ax² + bx + c = 0', category: 'algebra', difficulty: 'medium', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '2', front: 'Suma soluțiilor ecuației de gradul 2', back: 'x₁ + x₂ = -b/a\n\n(Relațiile lui Viète)', category: 'algebra', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '3', front: 'Produsul soluțiilor ecuației de gradul 2', back: 'x₁ · x₂ = c/a\n\n(Relațiile lui Viète)', category: 'algebra', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '4', front: 'Progresia aritmetică - termenul general', back: 'aₙ = a₁ + (n-1)·r\n\nUnde r este rația', category: 'algebra', difficulty: 'medium', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '5', front: 'Progresia geometrică - termenul general', back: 'bₙ = b₁ · qⁿ⁻¹\n\nUnde q este rația', category: 'algebra', difficulty: 'medium', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },

  // Analysis
  { id: '6', front: 'Derivata funcției xⁿ', back: '(xⁿ)\' = n·xⁿ⁻¹', category: 'analysis', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '7', front: 'Derivata funcției sin(x)', back: '(sin x)\' = cos x', category: 'analysis', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '8', front: 'Derivata funcției cos(x)', back: '(cos x)\' = -sin x', category: 'analysis', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '9', front: 'Derivata funcției eˣ', back: '(eˣ)\' = eˣ', category: 'analysis', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '10', front: 'Derivata funcției ln(x)', back: '(ln x)\' = 1/x', category: 'analysis', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '11', front: 'Integrala funcției xⁿ', back: '∫xⁿdx = xⁿ⁺¹/(n+1) + C\n\n(pentru n ≠ -1)', category: 'analysis', difficulty: 'medium', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '12', front: 'Integrala funcției 1/x', back: '∫(1/x)dx = ln|x| + C', category: 'analysis', difficulty: 'medium', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '13', front: 'Integrala funcției eˣ', back: '∫eˣdx = eˣ + C', category: 'analysis', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '14', front: 'Formula lui Leibniz-Newton', back: '∫ₐᵇf(x)dx = F(b) - F(a)\n\nUnde F este primitiva lui f', category: 'analysis', difficulty: 'hard', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },

  // Geometry
  { id: '15', front: 'Teorema lui Pitagora', back: 'a² + b² = c²\n\nUnde c este ipotenuza', category: 'geometry', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '16', front: 'Aria triunghiului', back: 'A = (b·h)/2\n\nsau A = (a·b·sin C)/2', category: 'geometry', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '17', front: 'Volumul sferei', back: 'V = (4/3)·π·r³', category: 'geometry', difficulty: 'medium', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '18', front: 'Aria sferei', back: 'A = 4·π·r²', category: 'geometry', difficulty: 'medium', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '19', front: 'Distanța dintre două puncte', back: 'd = √[(x₂-x₁)² + (y₂-y₁)²]', category: 'geometry', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },

  // Trigonometry
  { id: '20', front: 'Identitatea fundamentală', back: 'sin²x + cos²x = 1', category: 'trigonometry', difficulty: 'easy', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '21', front: 'sin(2x) =', back: 'sin(2x) = 2·sin(x)·cos(x)', category: 'trigonometry', difficulty: 'medium', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '22', front: 'cos(2x) =', back: 'cos(2x) = cos²x - sin²x\n= 2cos²x - 1\n= 1 - 2sin²x', category: 'trigonometry', difficulty: 'medium', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '23', front: 'Teorema sinusurilor', back: 'a/sin A = b/sin B = c/sin C = 2R', category: 'trigonometry', difficulty: 'hard', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
  { id: '24', front: 'Teorema cosinusului', back: 'c² = a² + b² - 2ab·cos C', category: 'trigonometry', difficulty: 'hard', nextReview: 0, interval: 1, easeFactor: 2.5, reviewCount: 0 },
];

export default function FlashcardsScreen() {
  const [flashcards, setFlashcards] = useState<Flashcard[]>(DEFAULT_FLASHCARDS);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [isStudying, setIsStudying] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [studyCards, setStudyCards] = useState<Flashcard[]>([]);
  const [cardsReviewed, setCardsReviewed] = useState(0);
  const [showStats, setShowStats] = useState(false);

  const flipAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    loadFlashcards();
  }, []);

  const loadFlashcards = async () => {
    try {
      const stored = await AsyncStorage.getItem('flashcards');
      if (stored) {
        setFlashcards(JSON.parse(stored));
      }
    } catch (error) {
      console.log('Error loading flashcards:', error);
    }
  };

  const saveFlashcards = async (cards: Flashcard[]) => {
    try {
      await AsyncStorage.setItem('flashcards', JSON.stringify(cards));
    } catch (error) {
      console.log('Error saving flashcards:', error);
    }
  };

  const getCategoryCards = (categoryId: string): Flashcard[] => {
    return flashcards.filter(c => c.category === categoryId);
  };

  const getDueCards = (categoryId?: string): Flashcard[] => {
    const now = Date.now();
    let cards = flashcards.filter(c => c.nextReview <= now);
    if (categoryId) {
      cards = cards.filter(c => c.category === categoryId);
    }
    return cards.sort((a, b) => a.nextReview - b.nextReview);
  };

  const startStudySession = (categoryId?: string) => {
    const dueCards = getDueCards(categoryId);
    if (dueCards.length === 0) {
      // If no cards due, get all cards from category
      const allCards = categoryId ? getCategoryCards(categoryId) : flashcards;
      setStudyCards(allCards);
    } else {
      setStudyCards(dueCards);
    }
    setSelectedCategory(categoryId || null);
    setCurrentIndex(0);
    setCardsReviewed(0);
    setIsFlipped(false);
    setIsStudying(true);
  };

  const flipCard = () => {
    const toValue = isFlipped ? 0 : 1;

    Animated.spring(flipAnim, {
      toValue,
      friction: 8,
      tension: 10,
      useNativeDriver: true,
    }).start();

    setIsFlipped(!isFlipped);
  };

  // Spaced Repetition Algorithm (SM-2)
  const rateCard = (quality: number) => {
    // quality: 0-5 (0-1 = forgot, 2-3 = hard, 4-5 = easy)
    const card = studyCards[currentIndex];

    let { easeFactor, interval, reviewCount } = card;

    if (quality < 3) {
      // Card was difficult - reset interval
      interval = 1;
    } else {
      // Card was easy enough
      if (reviewCount === 0) {
        interval = 1;
      } else if (reviewCount === 1) {
        interval = 6;
      } else {
        interval = Math.round(interval * easeFactor);
      }

      // Update ease factor
      easeFactor = easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
      if (easeFactor < 1.3) easeFactor = 1.3;
    }

    const nextReview = Date.now() + interval * 24 * 60 * 60 * 1000;

    const updatedCard: Flashcard = {
      ...card,
      easeFactor,
      interval,
      nextReview,
      reviewCount: reviewCount + 1,
    };

    const updatedFlashcards = flashcards.map(c =>
      c.id === card.id ? updatedCard : c
    );

    setFlashcards(updatedFlashcards);
    saveFlashcards(updatedFlashcards);
    setCardsReviewed(cardsReviewed + 1);

    // Move to next card
    if (currentIndex < studyCards.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setIsFlipped(false);
      flipAnim.setValue(0);
    } else {
      setShowStats(true);
    }
  };

  const finishSession = () => {
    setIsStudying(false);
    setShowStats(false);
    setCurrentIndex(0);
    setCardsReviewed(0);
  };

  const frontInterpolate = flipAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '180deg'],
  });

  const backInterpolate = flipAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['180deg', '360deg'],
  });

  const categories = CATEGORIES.map(cat => ({
    ...cat,
    cardCount: getCategoryCards(cat.id).length,
    dueCount: getDueCards(cat.id).length,
  }));

  const totalDue = getDueCards().length;

  if (isStudying && studyCards.length > 0) {
    const currentCard = studyCards[currentIndex];

    return (
      <View style={styles.container}>
        <LinearGradient
          colors={['#1f2937', '#111827']}
          style={styles.studyGradient}
        >
          {/* Header */}
          <View style={styles.studyHeader}>
            <TouchableOpacity onPress={finishSession}>
              <Text style={styles.closeButton}>✕</Text>
            </TouchableOpacity>
            <Text style={styles.progressText}>
              {currentIndex + 1} / {studyCards.length}
            </Text>
            <View style={styles.placeholder} />
          </View>

          {/* Progress Bar */}
          <View style={styles.studyProgressBar}>
            <LinearGradient
              colors={['#8b5cf6', '#7c3aed']}
              style={[
                styles.studyProgressFill,
                { width: `${((currentIndex + 1) / studyCards.length) * 100}%` }
              ]}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
            />
          </View>

          {/* Flashcard */}
          <TouchableOpacity
            style={styles.cardContainer}
            onPress={flipCard}
            activeOpacity={0.9}
          >
            <Animated.View
              style={[
                styles.card,
                styles.cardFront,
                { transform: [{ rotateY: frontInterpolate }] }
              ]}
            >
              <LinearGradient
                colors={['#374151', '#1f2937']}
                style={styles.cardGradient}
              >
                <Text style={styles.cardLabel}>ÎNTREBARE</Text>
                <Text style={styles.cardText}>{currentCard.front}</Text>
                <Text style={styles.tapHint}>Atinge pentru a vedea răspunsul</Text>
              </LinearGradient>
            </Animated.View>

            <Animated.View
              style={[
                styles.card,
                styles.cardBack,
                { transform: [{ rotateY: backInterpolate }] }
              ]}
            >
              <LinearGradient
                colors={['#8b5cf6', '#7c3aed']}
                style={styles.cardGradient}
              >
                <Text style={styles.cardLabel}>RĂSPUNS</Text>
                <Text style={styles.cardText}>{currentCard.back}</Text>
              </LinearGradient>
            </Animated.View>
          </TouchableOpacity>

          {/* Rating Buttons */}
          {isFlipped && (
            <View style={styles.ratingContainer}>
              <Text style={styles.ratingLabel}>Cât de bine ai știut?</Text>
              <View style={styles.ratingButtons}>
                <TouchableOpacity
                  style={[styles.ratingButton, styles.ratingHard]}
                  onPress={() => rateCard(1)}
                >
                  <Text style={styles.ratingEmoji}>😓</Text>
                  <Text style={styles.ratingText}>Greu</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.ratingButton, styles.ratingMedium]}
                  onPress={() => rateCard(3)}
                >
                  <Text style={styles.ratingEmoji}>🤔</Text>
                  <Text style={styles.ratingText}>OK</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.ratingButton, styles.ratingEasy]}
                  onPress={() => rateCard(5)}
                >
                  <Text style={styles.ratingEmoji}>😎</Text>
                  <Text style={styles.ratingText}>Ușor</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
        </LinearGradient>

        {/* Stats Modal */}
        <Modal visible={showStats} animationType="fade" transparent>
          <View style={styles.modalOverlay}>
            <View style={styles.statsModal}>
              <Text style={styles.statsEmoji}>🎉</Text>
              <Text style={styles.statsTitle}>Sesiune Completă!</Text>
              <Text style={styles.statsText}>
                Ai revizuit {cardsReviewed} carduri
              </Text>
              <TouchableOpacity
                style={styles.statsButton}
                onPress={finishSession}
              >
                <LinearGradient
                  colors={['#8b5cf6', '#7c3aed']}
                  style={styles.statsButtonGradient}
                >
                  <Text style={styles.statsButtonText}>Înapoi</Text>
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
        <LinearGradient
          colors={['#8b5cf6', '#7c3aed']}
          style={styles.header}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <Text style={styles.headerTitle}>Flashcards</Text>
          <Text style={styles.headerSubtitle}>Spaced repetition learning</Text>
        </LinearGradient>

        {/* Due Cards Banner */}
        {totalDue > 0 && (
          <TouchableOpacity
            style={styles.dueBanner}
            onPress={() => startStudySession()}
          >
            <LinearGradient
              colors={['#fef3c7', '#fde68a']}
              style={styles.dueBannerGradient}
            >
              <View style={styles.dueContent}>
                <Text style={styles.dueEmoji}>📚</Text>
                <View>
                  <Text style={styles.dueTitle}>{totalDue} carduri de revizuit</Text>
                  <Text style={styles.dueSubtitle}>Începe sesiunea acum!</Text>
                </View>
              </View>
              <Text style={styles.dueArrow}>→</Text>
            </LinearGradient>
          </TouchableOpacity>
        )}

        {/* Quick Start */}
        <TouchableOpacity
          style={styles.quickStartButton}
          onPress={() => startStudySession()}
        >
          <LinearGradient
            colors={['#22c55e', '#16a34a']}
            style={styles.quickStartGradient}
          >
            <Text style={styles.quickStartEmoji}>🚀</Text>
            <Text style={styles.quickStartText}>Start Quick Review</Text>
          </LinearGradient>
        </TouchableOpacity>

        {/* Categories */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Categorii</Text>
          <View style={styles.categoriesGrid}>
            {categories.map((category) => (
              <TouchableOpacity
                key={category.id}
                style={styles.categoryCard}
                onPress={() => startStudySession(category.id)}
              >
                <LinearGradient
                  colors={category.color}
                  style={styles.categoryGradient}
                >
                  <Text style={styles.categoryEmoji}>{category.emoji}</Text>
                  <Text style={styles.categoryName}>{category.name}</Text>
                  <Text style={styles.categoryCount}>
                    {category.cardCount} carduri
                  </Text>
                  {category.dueCount > 0 && (
                    <View style={styles.dueBadge}>
                      <Text style={styles.dueBadgeText}>{category.dueCount}</Text>
                    </View>
                  )}
                </LinearGradient>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* How it works */}
        <View style={styles.infoCard}>
          <Text style={styles.infoTitle}>Cum funcționează?</Text>
          <Text style={styles.infoText}>
            1. Cardurile apar în funcție de cât de bine le știi{'\n'}
            2. Cele dificile apar mai des{'\n'}
            3. Cele ușoare apar mai rar{'\n'}
            4. Sistemul se adaptează la tine!
          </Text>
        </View>

        <View style={{ height: 100 }} />
      </ScrollView>
    </View>
  );
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
    fontSize: 28,
    fontWeight: '800',
    color: 'white',
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
  },
  dueBanner: {
    marginHorizontal: 20,
    marginTop: -15,
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#f59e0b',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  dueBannerGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
  },
  dueContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  dueEmoji: {
    fontSize: 32,
  },
  dueTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#92400e',
  },
  dueSubtitle: {
    fontSize: 12,
    color: '#b45309',
  },
  dueArrow: {
    fontSize: 24,
    color: '#92400e',
  },
  quickStartButton: {
    marginHorizontal: 20,
    marginTop: 16,
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#22c55e',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  quickStartGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 18,
    gap: 12,
  },
  quickStartEmoji: {
    fontSize: 24,
  },
  quickStartText: {
    fontSize: 18,
    fontWeight: '700',
    color: 'white',
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1f2937',
    marginBottom: 16,
  },
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  categoryCard: {
    width: (width - 52) / 2,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  categoryGradient: {
    padding: 20,
    minHeight: 120,
  },
  categoryEmoji: {
    fontSize: 32,
    marginBottom: 8,
  },
  categoryName: {
    fontSize: 16,
    fontWeight: '700',
    color: 'white',
    marginBottom: 4,
  },
  categoryCount: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
  },
  dueBadge: {
    position: 'absolute',
    top: 12,
    right: 12,
    backgroundColor: '#ef4444',
    width: 24,
    height: 24,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  dueBadgeText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '700',
  },
  infoCard: {
    marginHorizontal: 20,
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#1f2937',
    marginBottom: 12,
  },
  infoText: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 24,
  },
  // Study Mode Styles
  studyGradient: {
    flex: 1,
    paddingTop: 60,
  },
  studyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    marginBottom: 16,
  },
  closeButton: {
    fontSize: 24,
    color: 'white',
    padding: 8,
  },
  progressText: {
    fontSize: 16,
    fontWeight: '600',
    color: 'white',
  },
  placeholder: {
    width: 40,
  },
  studyProgressBar: {
    height: 4,
    backgroundColor: '#374151',
    marginHorizontal: 20,
    borderRadius: 2,
    overflow: 'hidden',
    marginBottom: 30,
  },
  studyProgressFill: {
    height: '100%',
    borderRadius: 2,
  },
  cardContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  card: {
    width: width - 40,
    height: 300,
    borderRadius: 24,
    backfaceVisibility: 'hidden',
  },
  cardFront: {
    position: 'absolute',
  },
  cardBack: {
    position: 'absolute',
  },
  cardGradient: {
    flex: 1,
    borderRadius: 24,
    padding: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  cardLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: 'rgba(255,255,255,0.6)',
    letterSpacing: 2,
    marginBottom: 16,
  },
  cardText: {
    fontSize: 22,
    fontWeight: '600',
    color: 'white',
    textAlign: 'center',
    lineHeight: 32,
  },
  tapHint: {
    position: 'absolute',
    bottom: 24,
    fontSize: 12,
    color: 'rgba(255,255,255,0.5)',
  },
  ratingContainer: {
    padding: 20,
    alignItems: 'center',
  },
  ratingLabel: {
    fontSize: 14,
    color: '#9ca3af',
    marginBottom: 16,
  },
  ratingButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  ratingButton: {
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 16,
    alignItems: 'center',
    minWidth: 90,
  },
  ratingHard: {
    backgroundColor: '#ef4444',
  },
  ratingMedium: {
    backgroundColor: '#f59e0b',
  },
  ratingEasy: {
    backgroundColor: '#22c55e',
  },
  ratingEmoji: {
    fontSize: 24,
    marginBottom: 4,
  },
  ratingText: {
    fontSize: 14,
    fontWeight: '600',
    color: 'white',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.8)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  statsModal: {
    backgroundColor: 'white',
    borderRadius: 24,
    padding: 32,
    alignItems: 'center',
    marginHorizontal: 40,
  },
  statsEmoji: {
    fontSize: 64,
    marginBottom: 16,
  },
  statsTitle: {
    fontSize: 24,
    fontWeight: '800',
    color: '#1f2937',
    marginBottom: 8,
  },
  statsText: {
    fontSize: 16,
    color: '#6b7280',
    marginBottom: 24,
  },
  statsButton: {
    borderRadius: 16,
    overflow: 'hidden',
  },
  statsButtonGradient: {
    paddingHorizontal: 40,
    paddingVertical: 14,
  },
  statsButtonText: {
    fontSize: 16,
    fontWeight: '700',
    color: 'white',
  },
});
