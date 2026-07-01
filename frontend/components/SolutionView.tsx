import { View, Text, StyleSheet, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { DUO } from '@/constants/duo';
import MathText from './MathText';

// ── Types ──

export interface Step {
  pas: number;
  actiune: string;
  rezultat: string;
}

export interface StructuredSolution {
  tip?: string;
  ce_avem?: string;
  ce_aplicam?: string;
  pasi?: Step[];
  raspuns?: string;
  verificare?: string;
  greseli_frecvente?: string[];
}

// ── Sub-components ──

export function MathFormula({ text }: { text: string }) {
  return (
    <View style={styles.formulaBox}>
      <MathText text={text} style={styles.formulaText} block />
    </View>
  );
}

interface SectionHeaderProps {
  icon: keyof typeof Ionicons.glyphMap;
  label: string;
  color: string;
}
function SectionHeader({ icon, label, color }: SectionHeaderProps) {
  return (
    <View style={styles.sectionHeader}>
      <View style={[styles.sectionIconWrap, { backgroundColor: color + '20' }]}>
        <Ionicons name={icon} size={13} color={color} />
      </View>
      <Text style={[styles.sectionLabel, { color }]}>{label}</Text>
    </View>
  );
}

export function StepCard({ step, isLast }: { step: Step; isLast: boolean }) {
  return (
    <View style={styles.stepRow}>
      <View style={styles.stepGutter}>
        <LinearGradient
          colors={[DUO.blue, DUO.blueDark]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.stepBullet}
        >
          <Text style={styles.stepBulletText}>{step.pas}</Text>
        </LinearGradient>
        {!isLast && <View style={styles.stepConnector} />}
      </View>
      <View style={styles.stepContent}>
        <MathText text={step.actiune} style={styles.stepAction} />
        {step.rezultat ? <MathFormula text={step.rezultat} /> : null}
      </View>
    </View>
  );
}

export function MistakesCard({ mistakes }: { mistakes: string[] }) {
  return (
    <View style={styles.mistakesCard}>
      <View style={styles.mistakesHeader}>
        <Ionicons name="warning" size={14} color={DUO.orangeDark} />
        <Text style={styles.mistakesTitle}>Greșeli frecvente</Text>
      </View>
      {mistakes.map((m, i) => (
        <View key={i} style={styles.mistakeRow}>
          <View style={styles.mistakeDot} />
          <Text style={styles.mistakeText}>{m}</Text>
        </View>
      ))}
    </View>
  );
}

// ── Main Component ──

export default function StructuredSolutionView({ sol }: { sol: StructuredSolution }) {
  const showTip = sol.tip && sol.tip !== 'Nerecunoscut' && sol.tip !== 'Eroare la rezolvare';
  return (
    <View style={styles.solutionContainer}>
      {showTip && (
        <LinearGradient
          colors={[DUO.purpleDark, DUO.blueDark]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0 }}
          style={styles.tipBadge}
        >
          <Ionicons name="sparkles" size={12} color={DUO.white} />
          <Text style={styles.tipBadgeText}>{sol.tip}</Text>
        </LinearGradient>
      )}

      {sol.ce_avem ? (
        <View style={styles.section}>
          <SectionHeader icon="document-text" label="CE AVEM" color={DUO.cyan} />
          <MathFormula text={sol.ce_avem} />
        </View>
      ) : null}

      {sol.ce_aplicam ? (
        <View style={styles.section}>
          <SectionHeader icon="bulb" label="METODĂ" color={DUO.yellow} />
          <View style={styles.methodCard}>
            <MathText text={sol.ce_aplicam} style={styles.methodText} />
          </View>
        </View>
      ) : null}

      {sol.pasi && sol.pasi.length > 0 ? (
        <View style={styles.section}>
          <SectionHeader icon="layers" label="REZOLVARE" color={DUO.blue} />
          <View style={styles.stepsContainer}>
            {sol.pasi.map((step, i) => (
              <StepCard key={step.pas ?? i} step={step} isLast={i === sol.pasi!.length - 1} />
            ))}
          </View>
        </View>
      ) : null}

      {sol.raspuns ? (
        <LinearGradient
          colors={[DUO.green + '25', DUO.green + '10']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.answerCard}
        >
          <View style={styles.answerHeader}>
            <View style={styles.answerBadge}>
              <Ionicons name="checkmark-circle" size={14} color={DUO.white} />
            </View>
            <Text style={styles.answerLabel}>RĂSPUNS</Text>
          </View>
          <View style={styles.answerBody}>
            <MathText text={sol.raspuns} style={styles.answerText} block />
          </View>
        </LinearGradient>
      ) : null}

      {sol.verificare ? (
        <View style={styles.verifyCard}>
          <View style={styles.verifyHeader}>
            <Ionicons name="shield-checkmark" size={13} color={DUO.cyan} />
            <Text style={styles.verifyLabel}>VERIFICARE</Text>
          </View>
          <MathText text={sol.verificare} style={styles.verifyText} />
        </View>
      ) : null}

      {sol.greseli_frecvente && sol.greseli_frecvente.length > 0 ? (
        <MistakesCard mistakes={sol.greseli_frecvente} />
      ) : null}
    </View>
  );
}

// ── Styles ──

const styles = StyleSheet.create({
  solutionContainer: { gap: 14 },

  // Tip badge
  tipBadge: {
    alignSelf: 'flex-start',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 999,
  },
  tipBadgeText: {
    fontSize: 11,
    fontWeight: '800',
    color: DUO.white,
    letterSpacing: 0.5,
    textTransform: 'uppercase',
  },

  // Section
  section: { gap: 6 },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 2,
  },
  sectionIconWrap: {
    width: 22,
    height: 22,
    borderRadius: 6,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sectionLabel: {
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 1,
  },

  // Method card
  methodCard: {
    backgroundColor: DUO.yellow + '0E',
    borderLeftWidth: 3,
    borderLeftColor: DUO.yellow,
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 10,
  },
  methodText: {
    fontSize: 14,
    color: DUO.textPrimary,
    lineHeight: 21,
    fontWeight: '500',
  },

  // Formula (ce_avem, step result)
  formulaBox: {
    backgroundColor: DUO.cardDark,
    borderWidth: 1,
    borderColor: DUO.surface,
    borderLeftWidth: 3,
    borderLeftColor: DUO.cyan,
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 10,
  },
  formulaText: {
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    fontSize: 14,
    color: DUO.textPrimary,
    lineHeight: 22,
  },

  // Steps
  stepsContainer: { gap: 0, paddingLeft: 2 },
  stepRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    paddingBottom: 14,
  },
  stepGutter: {
    alignItems: 'center',
    width: 28,
  },
  stepBullet: {
    width: 28,
    height: 28,
    borderRadius: 14,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: DUO.blue,
    shadowOpacity: 0.4,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
    elevation: 3,
  },
  stepBulletText: { fontSize: 12, fontWeight: '800', color: DUO.white },
  stepConnector: {
    flex: 1,
    width: 2,
    backgroundColor: DUO.surface,
    marginTop: 4,
    minHeight: 20,
  },
  stepContent: { flex: 1, gap: 6, paddingTop: 2 },
  stepAction: {
    fontSize: 14,
    fontWeight: '600',
    color: DUO.textPrimary,
    lineHeight: 21,
  },

  // Answer hero
  answerCard: {
    borderRadius: 16,
    padding: 14,
    borderWidth: 1,
    borderColor: DUO.green + '40',
    gap: 8,
  },
  answerHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  answerBadge: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: DUO.green,
    justifyContent: 'center',
    alignItems: 'center',
  },
  answerLabel: {
    fontSize: 11,
    fontWeight: '800',
    color: DUO.green,
    letterSpacing: 1.2,
  },
  answerBody: {
    paddingLeft: 2,
  },
  answerText: {
    fontSize: 17,
    fontWeight: '800',
    color: DUO.greenLight,
    lineHeight: 26,
  },

  // Verify
  verifyCard: {
    backgroundColor: DUO.cyan + '0D',
    borderWidth: 1,
    borderColor: DUO.cyan + '25',
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 12,
    gap: 4,
  },
  verifyHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 2,
  },
  verifyLabel: {
    fontSize: 10,
    fontWeight: '800',
    color: DUO.cyan,
    letterSpacing: 1,
  },
  verifyText: {
    fontSize: 13,
    fontWeight: '500',
    color: DUO.textSecondary,
    lineHeight: 19,
  },

  // Mistakes
  mistakesCard: {
    backgroundColor: DUO.orange + '0E',
    borderWidth: 1,
    borderColor: DUO.orange + '30',
    borderRadius: 12,
    paddingHorizontal: 12,
    paddingVertical: 10,
    gap: 6,
  },
  mistakesHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 4,
  },
  mistakesTitle: {
    fontSize: 11,
    fontWeight: '800',
    color: DUO.orangeDark,
    letterSpacing: 1,
  },
  mistakeRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 10,
    paddingLeft: 2,
  },
  mistakeDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: DUO.orangeDark,
    marginTop: 7,
  },
  mistakeText: {
    flex: 1,
    fontSize: 13,
    color: DUO.textPrimary,
    lineHeight: 19,
    fontWeight: '500',
  },
});
