import { View, Text, StyleSheet } from 'react-native';
import { DUO } from '@/constants/duo';
import DuoButton from '@/components/DuoButton';

type ErrorPreset = 'network' | 'server' | 'not_found' | 'generic';

const PRESETS: Record<ErrorPreset, { emoji: string; title: string; subtitle: string }> = {
  network: { emoji: '📡', title: 'Fara conexiune', subtitle: 'Verifica conexiunea la internet si incearca din nou.' },
  server: { emoji: '🔧', title: 'Eroare server', subtitle: 'Serverul nu raspunde. Incearca mai tarziu.' },
  not_found: { emoji: '🔍', title: 'Nu am gasit nimic', subtitle: 'Continutul cautat nu exista sau a fost sters.' },
  generic: { emoji: '😕', title: 'Ceva nu a mers', subtitle: 'A aparut o eroare neasteptata. Incearca din nou.' },
};

interface ErrorStateProps {
  preset?: ErrorPreset;
  emoji?: string;
  title?: string;
  subtitle?: string;
  onRetry?: () => void;
}

export default function ErrorState({ preset = 'generic', emoji, title, subtitle, onRetry }: ErrorStateProps) {
  const p = PRESETS[preset];
  return (
    <View style={styles.container}>
      <Text style={styles.emoji}>{emoji || p.emoji}</Text>
      <Text style={styles.title}>{title || p.title}</Text>
      <Text style={styles.subtitle}>{subtitle || p.subtitle}</Text>
      {onRetry && (
        <DuoButton title="Reincearca" onPress={onRetry} color={DUO.red} size="medium" style={{ marginTop: 20 }} />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 40, backgroundColor: DUO.bg },
  emoji: { fontSize: 64, marginBottom: 16 },
  title: { fontSize: 20, fontWeight: '800', color: DUO.textPrimary, textAlign: 'center', marginBottom: 8 },
  subtitle: { fontSize: 14, fontWeight: '600', color: DUO.textSecondary, textAlign: 'center', lineHeight: 20 },
});
