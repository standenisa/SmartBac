import { useState, useRef } from 'react';
import { StyleSheet, View, Text, Dimensions, FlatList, ViewToken } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Animated, { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';
import { router } from 'expo-router';
import { DUO } from '@/constants/duo';
import DuoButton from '@/components/DuoButton';

const { width, height } = Dimensions.get('window');

const SLIDES = [
  {
    emoji: '🎓',
    title: 'Pregateste-te pentru BAC',
    subtitle: 'Exercitii personalizate, AI solver si spaced repetition pentru matematica.',
    color: DUO.green,
  },
  {
    emoji: '📚',
    title: 'Invata pas cu pas',
    subtitle: 'Rezolvari detaliate, hints progresive si provocari zilnice te ghideaza.',
    color: DUO.blue,
  },
  {
    emoji: '🏆',
    title: 'Alege profilul tau',
    subtitle: 'Selecteaza M1 (Mate-Info) sau M2 (Tehnologic) pentru a incepe.',
    color: DUO.purple,
    hasProfile: true,
  },
];

export default function OnboardingScreen() {
  const insets = useSafeAreaInsets();
  const [currentSlide, setCurrentSlide] = useState(0);
  const [selectedProfile, setSelectedProfile] = useState<'M1' | 'M2' | null>(null);
  const flatListRef = useRef<FlatList>(null);
  const scale = useSharedValue(1);

  const onViewableItemsChanged = useRef(({ viewableItems }: { viewableItems: ViewToken[] }) => {
    if (viewableItems[0]) {
      setCurrentSlide(viewableItems[0].index ?? 0);
    }
  }).current;

  const animStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const handleNext = () => {
    if (currentSlide < SLIDES.length - 1) {
      flatListRef.current?.scrollToIndex({ index: currentSlide + 1 });
    }
  };

  const handleStart = async () => {
    if (!selectedProfile) return;
    await AsyncStorage.setItem('hasOnboarded', 'true');
    // Citit la inregistrare, ca profilul ales aici sa ajunga pe contul nou
    await AsyncStorage.setItem('pendingProfile', selectedProfile);
    router.replace('/login' as any);
  };

  const isLastSlide = currentSlide === SLIDES.length - 1;

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <FlatList
        ref={flatListRef}
        data={SLIDES}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        onViewableItemsChanged={onViewableItemsChanged}
        viewabilityConfig={{ viewAreaCoveragePercentThreshold: 50 }}
        keyExtractor={(_, i) => String(i)}
        renderItem={({ item }) => (
          <View style={styles.slide}>
            <Animated.View style={[styles.emojiContainer, animStyle]}>
              <LinearGradient colors={[item.color + '20', 'transparent']} style={styles.emojiGlow}>
                <Text style={styles.emoji}>{item.emoji}</Text>
              </LinearGradient>
            </Animated.View>
            <Text style={styles.title}>{item.title}</Text>
            <Text style={styles.subtitle}>{item.subtitle}</Text>

            {item.hasProfile && (
              <View style={styles.profileRow}>
                {(['M1', 'M2'] as const).map(p => (
                  <DuoButton
                    key={p}
                    title={`${p} - ${p === 'M1' ? 'Mate-Info' : 'Tehnologic'}`}
                    onPress={() => { setSelectedProfile(p); scale.value = withSpring(1.05, {}, () => { scale.value = withSpring(1); }); }}
                    color={selectedProfile === p ? DUO.purple : DUO.surface}
                    textColor={selectedProfile === p ? DUO.white : DUO.textSecondary}
                    size="medium"
                    style={{ flex: 1 }}
                  />
                ))}
              </View>
            )}
          </View>
        )}
      />

      {/* Dots */}
      <View style={styles.dotsRow}>
        {SLIDES.map((_, i) => (
          <View key={i} style={[styles.dot, i === currentSlide && styles.dotActive]} />
        ))}
      </View>

      {/* Button */}
      <View style={[styles.buttonContainer, { paddingBottom: insets.bottom + 20 }]}>
        {isLastSlide ? (
          <DuoButton
            title="INCEPE!"
            onPress={handleStart}
            color={DUO.green}
            glow
            disabled={!selectedProfile}
          />
        ) : (
          <DuoButton title="CONTINUA" onPress={handleNext} color={DUO.blue} />
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  slide: { width, paddingHorizontal: 40, justifyContent: 'center', alignItems: 'center', paddingTop: height * 0.1 },
  emojiContainer: { marginBottom: 32 },
  emojiGlow: { width: 140, height: 140, borderRadius: 70, justifyContent: 'center', alignItems: 'center' },
  emoji: { fontSize: 72 },
  title: { fontSize: 28, fontWeight: '800', color: DUO.textPrimary, textAlign: 'center', marginBottom: 12 },
  subtitle: { fontSize: 16, fontWeight: '600', color: DUO.textSecondary, textAlign: 'center', lineHeight: 24 },
  profileRow: { flexDirection: 'row', gap: 10, marginTop: 32, width: '100%' },
  dotsRow: { flexDirection: 'row', justifyContent: 'center', gap: 8, paddingVertical: 16 },
  dot: { width: 8, height: 8, borderRadius: 4, backgroundColor: DUO.surface },
  dotActive: { backgroundColor: DUO.green, width: 24 },
  buttonContainer: { paddingHorizontal: 20 },
});
