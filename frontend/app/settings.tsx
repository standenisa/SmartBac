import { useState } from 'react';
import {
  StyleSheet, View, Text, ScrollView, Alert, Switch,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { DUO } from '@/constants/duo';
import { TYPO } from '@/constants/typography';
import { useAuth } from '@/contexts/AuthContext';
import { useSettings } from '@/contexts/SoundContext';
import AnimatedPressable from '@/components/AnimatedPressable';

export default function SettingsScreen() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { user, logout } = useAuth();
  const { settings, toggleSound, toggleHaptics } = useSettings();
  const [selectedProfile, setSelectedProfile] = useState(user?.profile || 'M1');

  const handleLogout = () => {
    Alert.alert(
      'Deconectare',
      'Esti sigur ca vrei sa te deconectezi?',
      [
        { text: 'Anuleaza', style: 'cancel' },
        {
          text: 'Deconecteaza-te',
          style: 'destructive',
          onPress: async () => {
            await logout();
            router.replace('/login');
          },
        },
      ],
    );
  };

  const profiles = [
    { id: 'M1', name: 'Mate-Info', emoji: '💻', desc: 'Informatica & Matematica' },
    { id: 'M2', name: 'Stiinte', emoji: '🔬', desc: 'Stiinte ale naturii' },
    { id: 'M3', name: 'Pedagogic', emoji: '📚', desc: 'Pedagogic' },
    { id: 'M4', name: 'Tehnic', emoji: '⚙️', desc: 'Tehnic' },
  ];

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      {/* Header */}
      <LinearGradient colors={[DUO.card, DUO.bg]} style={styles.header}>
        <AnimatedPressable onPress={() => router.back()} style={styles.backBtn}>
          <Text style={styles.backText}>← Inapoi</Text>
        </AnimatedPressable>
        <Text style={[TYPO.heading2, { color: DUO.textPrimary }]}>Setari</Text>
      </LinearGradient>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentInner}>
        {/* Profile Card */}
        <View style={styles.profileCard}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>
              {user?.username?.charAt(0)?.toUpperCase() || '?'}
            </Text>
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.profileName}>{user?.username || 'Utilizator'}</Text>
            <Text style={styles.profileEmail}>{user?.email || ''}</Text>
            <View style={styles.levelBadge}>
              <Text style={styles.levelText}>Nivel {user?.level || 1}</Text>
            </View>
          </View>
        </View>

        {/* Profil BAC */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Profil BAC</Text>
          <View style={styles.profileGrid}>
            {profiles.map((p) => (
              <AnimatedPressable
                key={p.id}
                style={[
                  styles.profileOption,
                  selectedProfile === p.id && styles.profileOptionActive,
                ]}
                onPress={() => setSelectedProfile(p.id)}
              >
                <Text style={styles.profileEmoji}>{p.emoji}</Text>
                <Text style={[
                  styles.profileOptionName,
                  selectedProfile === p.id && { color: DUO.green },
                ]}>{p.name}</Text>
                <Text style={styles.profileOptionDesc}>{p.desc}</Text>
              </AnimatedPressable>
            ))}
          </View>
        </View>

        {/* Preferences */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Preferinte</Text>

          <View style={styles.settingRow}>
            <View style={{ flex: 1 }}>
              <Text style={styles.settingLabel}>Sunete</Text>
              <Text style={styles.settingDesc}>Efecte sonore la raspuns corect/gresit</Text>
            </View>
            <Switch
              value={settings.soundEnabled}
              onValueChange={toggleSound}
              trackColor={{ false: DUO.surface, true: DUO.green + '60' }}
              thumbColor={settings.soundEnabled ? DUO.green : DUO.textMuted}
            />
          </View>

          <View style={styles.settingRow}>
            <View style={{ flex: 1 }}>
              <Text style={styles.settingLabel}>Vibratii</Text>
              <Text style={styles.settingDesc}>Feedback haptic la interactiuni</Text>
            </View>
            <Switch
              value={settings.hapticsEnabled}
              onValueChange={toggleHaptics}
              trackColor={{ false: DUO.surface, true: DUO.green + '60' }}
              thumbColor={settings.hapticsEnabled ? DUO.green : DUO.textMuted}
            />
          </View>
        </View>

        {/* About */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Despre aplicatie</Text>
          <View style={styles.aboutCard}>
            <Text style={styles.aboutTitle}>SmartBAC</Text>
            <Text style={styles.aboutVersion}>Versiunea 1.0.0</Text>
            <Text style={styles.aboutDesc}>
              Aplicatie de pregatire pentru Bacalaureat la Matematica.{'\n'}
              Foloseste inteligenta artificiala pentru rezolvarea exercitiilor si invatare personalizata.
            </Text>
          </View>
        </View>

        {/* Logout */}
        <AnimatedPressable style={styles.logoutButton} onPress={handleLogout}>
          <Text style={styles.logoutText}>Deconecteaza-te</Text>
        </AnimatedPressable>

        <View style={{ height: 40 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: DUO.bg },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingBottom: 14,
    paddingHorizontal: 20,
    gap: 16,
    borderBottomWidth: 1,
    borderBottomColor: DUO.surface,
  },
  backBtn: { padding: 4 },
  backText: { fontSize: 15, fontWeight: '700', color: DUO.textSecondary },
  content: { flex: 1 },
  contentInner: { padding: 20, gap: 20 },

  profileCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: DUO.card,
    borderRadius: 18,
    padding: 18,
    gap: 16,
    borderWidth: 1,
    borderColor: DUO.surface,
  },
  avatar: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: DUO.green + '20',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: DUO.green,
  },
  avatarText: { fontSize: 24, fontWeight: '800', color: DUO.green },
  profileName: { fontSize: 18, fontWeight: '800', color: DUO.textPrimary },
  profileEmail: { fontSize: 13, fontWeight: '600', color: DUO.textSecondary, marginTop: 2 },
  levelBadge: {
    backgroundColor: DUO.yellow + '20',
    paddingHorizontal: 10,
    paddingVertical: 3,
    borderRadius: 999,
    alignSelf: 'flex-start',
    marginTop: 6,
  },
  levelText: { fontSize: 11, fontWeight: '800', color: DUO.yellow },

  section: { gap: 12 },
  sectionTitle: { fontSize: 13, fontWeight: '800', color: DUO.textMuted, letterSpacing: 1, textTransform: 'uppercase' },

  profileGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  profileOption: {
    width: '48%' as any,
    backgroundColor: DUO.card,
    borderRadius: 14,
    padding: 14,
    borderWidth: 1.5,
    borderColor: DUO.surface,
    alignItems: 'center',
    gap: 4,
  },
  profileOptionActive: {
    borderColor: DUO.green,
    backgroundColor: DUO.green + '10',
  },
  profileEmoji: { fontSize: 28 },
  profileOptionName: { fontSize: 14, fontWeight: '800', color: DUO.textPrimary },
  profileOptionDesc: { fontSize: 11, fontWeight: '600', color: DUO.textMuted, textAlign: 'center' },

  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: DUO.card,
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: DUO.surface,
  },
  settingLabel: { fontSize: 15, fontWeight: '700', color: DUO.textPrimary },
  settingDesc: { fontSize: 12, fontWeight: '500', color: DUO.textMuted, marginTop: 2 },

  aboutCard: {
    backgroundColor: DUO.card,
    borderRadius: 14,
    padding: 18,
    alignItems: 'center',
    gap: 4,
    borderWidth: 1,
    borderColor: DUO.surface,
  },
  aboutTitle: { fontSize: 20, fontWeight: '900', color: DUO.green },
  aboutVersion: { fontSize: 12, fontWeight: '700', color: DUO.textMuted },
  aboutDesc: { fontSize: 13, fontWeight: '500', color: DUO.textSecondary, textAlign: 'center', marginTop: 8, lineHeight: 20 },

  logoutButton: {
    backgroundColor: DUO.red + '15',
    borderRadius: 14,
    padding: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: DUO.red + '30',
  },
  logoutText: { fontSize: 16, fontWeight: '800', color: DUO.red },
});
