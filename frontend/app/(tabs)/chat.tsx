import { useState, useRef, useCallback, useEffect } from 'react';
import {
  StyleSheet, View, Text, TextInput, TouchableOpacity,
  ScrollView, KeyboardAvoidingView, Platform, Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import Animated, { useSharedValue, useAnimatedStyle, withRepeat, withTiming, withDelay, withSequence, FadeInDown, type SharedValue } from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { apiPost } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { DUO } from '@/constants/duo';
import { TYPO } from '@/constants/typography';
import AnimatedPressable from '@/components/AnimatedPressable';
import StructuredSolutionView, { StructuredSolution, MathFormula, MistakesCard } from '@/components/SolutionView';
import MathText from '@/components/MathText';

interface ConceptData {
  concept?: string;
  ce_este?: string;
  analogie?: string;
  formula?: string;
  reguli?: string[];
  exemple?: { problema: string; rezolvare: string; explicatie?: string }[];
  greseli_frecvente?: string[];
}

interface ChatAPIResponse {
  response: string;
  structured?: StructuredSolution | null;
  concept?: ConceptData | null;
  latex?: string | null;
  model_used: string;
  suggestions: string[];
}

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  structured?: StructuredSolution | null;
  concept?: ConceptData | null;
}

// ── Typing Indicator ──

function TypingDots() {
  const dot1 = useSharedValue(0);
  const dot2 = useSharedValue(0);
  const dot3 = useSharedValue(0);

  useEffect(() => {
    const bounce = (sv: SharedValue<number>, delay: number) => {
      sv.value = withDelay(delay, withRepeat(
        withSequence(
          withTiming(-6, { duration: 300 }),
          withTiming(0, { duration: 300 }),
        ),
        -1,
        false,
      ));
    };
    bounce(dot1, 0);
    bounce(dot2, 150);
    bounce(dot3, 300);
  }, []);

  const style1 = useAnimatedStyle(() => ({ transform: [{ translateY: dot1.value }] }));
  const style2 = useAnimatedStyle(() => ({ transform: [{ translateY: dot2.value }] }));
  const style3 = useAnimatedStyle(() => ({ transform: [{ translateY: dot3.value }] }));

  return (
    <View style={styles.typingRow}>
      {[style1, style2, style3].map((s, i) => (
        <Animated.View key={i} style={[styles.typingDot, s]} />
      ))}
    </View>
  );
}

// ── Initial suggestions ──

const INITIAL_SUGGESTIONS = [
  'Rezolva: 2x + 3 = 7',
  'Ce e derivata?',
  'Calculeaza det [[3,1],[2,4]]',
  'C(10,3) = ?',
  'Reguli integrale',
  'Formule trigonometrie',
];

// ── Formatted AI Message Components ──

function ConceptSection({
  icon, label, color, children,
}: { icon: keyof typeof Ionicons.glyphMap; label: string; color: string; children: React.ReactNode }) {
  return (
    <View style={styles.conceptSection}>
      <View style={styles.conceptHeader}>
        <View style={[styles.conceptIconWrap, { backgroundColor: color + '20' }]}>
          <Ionicons name={icon} size={13} color={color} />
        </View>
        <Text style={[styles.conceptLabel, { color }]}>{label}</Text>
      </View>
      {children}
    </View>
  );
}

function ConceptCard({ concept }: { concept: ConceptData }) {
  return (
    <View style={styles.conceptContainer}>
      {concept.concept && (
        <LinearGradient
          colors={[DUO.purpleDark, DUO.blueDark]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0 }}
          style={styles.conceptTitleBadge}
        >
          <Ionicons name="book" size={13} color={DUO.white} />
          <Text style={styles.conceptTitle}>{concept.concept}</Text>
        </LinearGradient>
      )}
      {concept.ce_este && (
        <ConceptSection icon="information-circle" label="CE ESTE" color={DUO.cyan}>
          <MathText text={concept.ce_este} style={styles.conceptText} />
        </ConceptSection>
      )}
      {concept.analogie && (
        <ConceptSection icon="bulb" label="ANALOGIE" color={DUO.yellow}>
          <View style={styles.analogyCard}>
            <MathText text={concept.analogie} style={styles.conceptText} />
          </View>
        </ConceptSection>
      )}
      {concept.formula && (
        <ConceptSection icon="calculator" label="FORMULĂ" color={DUO.blue}>
          <MathFormula text={concept.formula} />
        </ConceptSection>
      )}
      {concept.reguli && concept.reguli.length > 0 && (
        <ConceptSection icon="list" label="REGULI" color={DUO.green}>
          {concept.reguli.map((r, i) => (
            <View key={i} style={styles.ruleRow}>
              <View style={styles.ruleDot} />
              <MathText text={r} style={styles.ruleText} />
            </View>
          ))}
        </ConceptSection>
      )}
      {concept.exemple && concept.exemple.length > 0 && (
        <ConceptSection icon="school" label="EXEMPLE" color={DUO.pink}>
          {concept.exemple.slice(0, 3).map((ex, i) => (
            <View key={i} style={styles.exampleItem}>
              <View style={styles.exampleBadge}>
                <Text style={styles.exampleBadgeText}>{i + 1}</Text>
              </View>
              <View style={styles.exampleBody}>
                <MathText text={ex.problema} style={styles.exampleProblem} />
                <MathFormula text={ex.rezolvare} />
                {ex.explicatie && (
                  <Text style={styles.exampleExplanation}>{ex.explicatie}</Text>
                )}
              </View>
            </View>
          ))}
        </ConceptSection>
      )}
      {concept.greseli_frecvente && concept.greseli_frecvente.length > 0 && (
        <MistakesCard mistakes={concept.greseli_frecvente} />
      )}
    </View>
  );
}

function AIMessageContent({ message }: { message: Message }) {
  // If we have structured data, render rich UI
  if (message.structured && message.structured.tip && message.structured.tip !== 'Nerecunoscut') {
    return <StructuredSolutionView sol={message.structured} />;
  }
  if (message.concept && message.concept.concept) {
    return <ConceptCard concept={message.concept} />;
  }
  // Plain text fallback
  return <MathText text={message.text} style={styles.aiText} />;
}

// ── Main Screen ──

export default function ChatScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Salut! Sunt tutorul tau de matematica pentru BAC.\n\nPot sa te ajut cu:\n  Rezolvarea exercitiilor pas cu pas\n  Explicatii concepte (derivate, integrale, limite...)\n  Analiza greselilor tale\n  Formule si reguli\n\nScrie un exercitiu sau o intrebare!',
      isUser: false,
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeSuggestions, setActiveSuggestions] = useState<string[]>(INITIAL_SUGGESTIONS);
  const scrollViewRef = useRef<ScrollView>(null);

  const scrollToBottom = useCallback(() => {
    setTimeout(() => scrollViewRef.current?.scrollToEnd({ animated: true }), 100);
  }, []);

  const sendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: text.trim(),
      isUser: true,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    setActiveSuggestions([]);
    scrollToBottom();

    try {
      const data = await apiPost<ChatAPIResponse>('/api/chat', {
        message: text.trim(),
        user_id: user?.id,
      });

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response || 'Nu am putut procesa intrebarea.',
        isUser: false,
        timestamp: new Date(),
        structured: data.structured,
        concept: data.concept,
      };
      setMessages(prev => [...prev, aiMessage]);
      setActiveSuggestions(data.suggestions || []);
    } catch {
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        text: 'Eroare de conexiune. Verifica daca backend-ul ruleaza.',
        isUser: false,
        timestamp: new Date(),
      }]);
      setActiveSuggestions([]);
    }
    setIsLoading(false);
    scrollToBottom();
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={90}
    >
      {/* Header */}
      <LinearGradient colors={[DUO.card, DUO.bg]} style={[styles.header, { paddingTop: insets.top + 8 }]}>
        <View style={styles.avatarRing}>
          <Image source={require('@/assets/images/hero-brain.jpeg')} style={styles.headerBrainImg} />
          <View style={styles.onlineDot} />
        </View>
        <View>
          <Text style={[styles.headerTitle, TYPO.heading3]}>SmartBAC Tutor</Text>
          <Text style={[styles.headerSubtitle, TYPO.label]}>Rezolv exercitii pas cu pas</Text>
        </View>
      </LinearGradient>

      {/* Messages */}
      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
        onContentSizeChange={scrollToBottom}
        keyboardShouldPersistTaps="handled"
      >
        {messages.map((msg) => (
          <Animated.View
            key={msg.id}
            entering={FadeInDown.duration(260).springify().damping(16)}
            style={[styles.messageBubble, msg.isUser ? styles.userBubble : styles.aiBubble]}
          >
            {!msg.isUser && (
              <LinearGradient
                colors={[DUO.purpleDark, DUO.blueDark]}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={styles.aiAvatar}
              >
                <Image source={require('@/assets/images/hero-brain.jpeg')} style={styles.aiAvatarImg} />
              </LinearGradient>
            )}
            {msg.isUser ? (
              <LinearGradient
                colors={[DUO.green, DUO.greenDark]}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={[styles.messageContent, styles.userContent]}
              >
                <Text style={styles.userText}>{msg.text}</Text>
              </LinearGradient>
            ) : (
              <View style={[styles.messageContent, styles.aiContent]}>
                <AIMessageContent message={msg} />
              </View>
            )}
          </Animated.View>
        ))}

        {isLoading && (
          <Animated.View
            entering={FadeInDown.duration(200)}
            style={[styles.messageBubble, styles.aiBubble]}
          >
            <LinearGradient
              colors={[DUO.purpleDark, DUO.blueDark]}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.aiAvatar}
            >
              <Image source={require('@/assets/images/hero-brain.jpeg')} style={styles.aiAvatarImg} />
            </LinearGradient>
            <View style={[styles.messageContent, styles.aiContent]}>
              <TypingDots />
            </View>
          </Animated.View>
        )}
      </ScrollView>

      {/* Contextual Quick Buttons */}
      {activeSuggestions.length > 0 && !isLoading && (
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.suggestionsBar}
          contentContainerStyle={styles.suggestionsContent}
        >
          {activeSuggestions.map((s, i) => (
            <AnimatedPressable
              key={i}
              style={styles.suggestionChip}
              onPress={() => sendMessage(s)}
            >
              <Text style={styles.suggestionText}>{s}</Text>
            </AnimatedPressable>
          ))}
        </ScrollView>
      )}

      {/* Input */}
      <View style={[styles.inputContainer, { paddingBottom: insets.bottom + 8 }]}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Scrie exercitiul sau intrebarea..."
          placeholderTextColor={DUO.textMuted}
          multiline
          maxLength={500}
          onSubmitEditing={() => sendMessage(inputText)}
        />
        <TouchableOpacity
          style={[styles.sendButton, (!inputText.trim() || isLoading) && styles.sendButtonDisabled]}
          onPress={() => sendMessage(inputText)}
          disabled={!inputText.trim() || isLoading}
        >
          <Text style={styles.sendButtonText}>↑</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

// ── Styles ──

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },

  // Header
  header: {
    flexDirection: 'row', alignItems: 'center',
    paddingBottom: 14, paddingHorizontal: 20, gap: 12,
    borderBottomWidth: 1, borderBottomColor: DUO.surface,
  },
  avatarRing: {
    width: 48, height: 48, borderRadius: 24,
    backgroundColor: DUO.card, justifyContent: 'center', alignItems: 'center',
    borderWidth: 2, borderColor: DUO.purple + '40',
    overflow: 'hidden',
  },
  headerBrainImg: { width: 34, height: 34 },
  onlineDot: {
    position: 'absolute', bottom: -1, right: -1,
    width: 14, height: 14, borderRadius: 7,
    backgroundColor: DUO.green,
    borderWidth: 2, borderColor: DUO.card,
  },
  headerTitle: { color: DUO.textPrimary },
  headerSubtitle: { color: DUO.textSecondary },

  // Messages
  messagesContainer: { flex: 1 },
  messagesContent: { padding: 16, paddingBottom: 8 },
  messageBubble: { flexDirection: 'row', marginBottom: 14, alignItems: 'flex-start' },
  userBubble: { justifyContent: 'flex-end' },
  aiBubble: { justifyContent: 'flex-start' },
  aiAvatar: {
    width: 36, height: 36, borderRadius: 18,
    justifyContent: 'center', alignItems: 'center',
    marginRight: 10, marginTop: 2,
    shadowColor: DUO.purple, shadowOpacity: 0.4,
    shadowRadius: 8, shadowOffset: { width: 0, height: 2 }, elevation: 4,
  },
  aiAvatarImg: { width: 24, height: 24, borderRadius: 4 },
  messageContent: { maxWidth: '86%', padding: 14, borderRadius: 18 },
  userContent: {
    borderBottomRightRadius: 4, marginLeft: 'auto',
    shadowColor: DUO.green, shadowOpacity: 0.25,
    shadowRadius: 6, shadowOffset: { width: 0, height: 2 }, elevation: 3,
  },
  aiContent: {
    backgroundColor: DUO.card, borderBottomLeftRadius: 4,
    borderWidth: 1, borderColor: DUO.surface,
  },
  userText: { fontSize: 15, lineHeight: 22, fontWeight: '600', color: DUO.white },
  aiText: { fontSize: 15, lineHeight: 22, fontWeight: '600', color: DUO.textPrimary },

  // Typing indicator
  typingRow: { flexDirection: 'row', alignItems: 'center', gap: 5, paddingVertical: 4, paddingHorizontal: 4 },
  typingDot: {
    width: 8, height: 8, borderRadius: 4,
    backgroundColor: DUO.textMuted,
  },

  // Suggestions bar
  suggestionsBar: {
    maxHeight: 50, borderTopWidth: 1, borderTopColor: DUO.surface,
    backgroundColor: DUO.bg,
  },
  suggestionsContent: { paddingHorizontal: 12, paddingVertical: 8, gap: 8 },
  suggestionChip: {
    backgroundColor: DUO.blue + '15', paddingHorizontal: 14, paddingVertical: 8,
    borderRadius: 999, borderWidth: 1, borderColor: DUO.blue + '60',
    marginRight: 8,
  },
  suggestionText: { fontSize: 13, color: DUO.blue, fontWeight: '700' },

  // Input
  inputContainer: {
    flexDirection: 'row', padding: 12, paddingHorizontal: 16,
    backgroundColor: DUO.card, borderTopWidth: 1, borderTopColor: DUO.surface,
    alignItems: 'flex-end',
  },
  input: {
    flex: 1, backgroundColor: DUO.surface, borderRadius: 999,
    paddingHorizontal: 20, paddingVertical: 12,
    fontSize: 15, maxHeight: 100, color: DUO.textPrimary,
    borderWidth: 1, borderColor: DUO.surfaceLight, fontWeight: '600',
  },
  sendButton: {
    marginLeft: 10, width: 46, height: 46, borderRadius: 23,
    backgroundColor: DUO.green, justifyContent: 'center', alignItems: 'center',
    borderBottomWidth: 3, borderBottomColor: DUO.greenDark,
  },
  sendButtonDisabled: {
    backgroundColor: DUO.surface, borderBottomColor: DUO.cardDark,
  },
  sendButtonText: { fontSize: 22, color: DUO.white, fontWeight: '800' },

  // ── Concept Styles ──
  conceptContainer: { gap: 12 },
  conceptTitleBadge: {
    alignSelf: 'flex-start',
    flexDirection: 'row', alignItems: 'center', gap: 6,
    paddingHorizontal: 12, paddingVertical: 6,
    borderRadius: 999,
  },
  conceptTitle: {
    fontSize: 13, fontWeight: '800', color: DUO.white,
    letterSpacing: 0.3,
  },
  conceptSection: { gap: 6 },
  conceptHeader: {
    flexDirection: 'row', alignItems: 'center', gap: 6, marginBottom: 2,
  },
  conceptIconWrap: {
    width: 22, height: 22, borderRadius: 6,
    justifyContent: 'center', alignItems: 'center',
  },
  conceptLabel: { fontSize: 11, fontWeight: '800', letterSpacing: 1 },
  conceptText: { fontSize: 14, fontWeight: '500', color: DUO.textPrimary, lineHeight: 21 },
  analogyCard: {
    backgroundColor: DUO.yellow + '0E',
    borderLeftWidth: 3, borderLeftColor: DUO.yellow,
    paddingHorizontal: 12, paddingVertical: 10, borderRadius: 10,
  },
  ruleRow: {
    flexDirection: 'row', alignItems: 'flex-start', gap: 10, paddingLeft: 2,
    marginBottom: 4,
  },
  ruleDot: {
    width: 6, height: 6, borderRadius: 3,
    backgroundColor: DUO.green, marginTop: 7,
  },
  ruleText: { flex: 1, fontSize: 13, fontWeight: '500', color: DUO.textPrimary, lineHeight: 20 },
  exampleItem: {
    flexDirection: 'row', gap: 10, marginBottom: 10,
  },
  exampleBadge: {
    width: 22, height: 22, borderRadius: 11,
    backgroundColor: DUO.pink + '30',
    borderWidth: 1, borderColor: DUO.pink + '60',
    justifyContent: 'center', alignItems: 'center',
    marginTop: 1,
  },
  exampleBadgeText: { fontSize: 11, fontWeight: '800', color: DUO.pink },
  exampleBody: { flex: 1, gap: 4 },
  exampleProblem: { fontSize: 13, fontWeight: '700', color: DUO.textPrimary },
  exampleExplanation: {
    fontSize: 12, fontWeight: '500', color: DUO.textSecondary,
    fontStyle: 'italic', marginTop: 2,
  },
});
