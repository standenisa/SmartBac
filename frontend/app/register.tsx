import { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Pressable,
  ActivityIndicator,
  ImageBackground,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { DUO } from '@/constants/duo';
import DuoButton from '@/components/DuoButton';
import { useAuth } from '@/contexts/AuthContext';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function RegisterScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const { register } = useAuth();

  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const validate = (): string | null => {
    if (!email.trim() || !username.trim() || !password || !confirmPassword) {
      return 'Completeaza toate campurile';
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      return 'Adresa de email nu este valida';
    }
    if (username.trim().length < 3) {
      return 'Username-ul trebuie sa aiba minim 3 caractere';
    }
    if (password.length < 6) {
      return 'Parola trebuie sa aiba minim 6 caractere';
    }
    if (password !== confirmPassword) {
      return 'Parolele nu coincid';
    }
    return null;
  };

  const handleRegister = async () => {
    setError('');
    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }
    setLoading(true);
    try {
      const profile = (await AsyncStorage.getItem('pendingProfile')) || 'M1';
      await register(email.trim(), username.trim(), password, profile);
    } catch (e: any) {
      setError(e.message || 'Eroare la inregistrare');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ImageBackground
      source={require('@/assets/images/bg-circuit.jpeg')}
      style={styles.bgWrap}
      imageStyle={styles.bgImage}
    >
      <View style={styles.overlay} />
      <KeyboardAvoidingView
        style={[styles.container, { paddingTop: insets.top }]}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <ScrollView
          contentContainerStyle={styles.scroll}
          keyboardShouldPersistTaps="handled"
        >
          {/* Header */}
          <View style={styles.logoContainer}>
            <View style={styles.logoRow}>
              <View style={styles.logoDot} />
              <Text style={styles.logoText}>smart</Text>
              <View style={styles.logoPill}>
                <Text style={styles.logoPillText}>BAC</Text>
              </View>
            </View>
            <View style={styles.accentLine} />
            <Text style={styles.title}>Creeaza Cont</Text>
          </View>

          {/* Error */}
          {error ? (
            <View style={styles.errorCard}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          ) : null}

          {/* Form card */}
          <View style={styles.formCard}>
            {/* Email */}
            <View style={styles.inputWrapper}>
              <Text style={styles.inputIcon}>✉️</Text>
              <TextInput
                style={styles.input}
                placeholder="Email"
                placeholderTextColor={DUO.textMuted}
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
                autoCorrect={false}
              />
            </View>

            {/* Username */}
            <View style={styles.inputWrapper}>
              <Text style={styles.inputIcon}>👤</Text>
              <TextInput
                style={styles.input}
                placeholder="Username"
                placeholderTextColor={DUO.textMuted}
                value={username}
                onChangeText={setUsername}
                autoCapitalize="none"
                autoCorrect={false}
              />
            </View>

            {/* Password */}
            <View style={styles.inputWrapper}>
              <Text style={styles.inputIcon}>🔒</Text>
              <TextInput
                style={[styles.input, { flex: 1 }]}
                placeholder="Parola (min. 6 caractere)"
                placeholderTextColor={DUO.textMuted}
                value={password}
                onChangeText={setPassword}
                secureTextEntry={!showPassword}
                autoCapitalize="none"
              />
              <Pressable onPress={() => setShowPassword(!showPassword)} style={styles.eyeBtn}>
                <Text style={styles.eyeIcon}>{showPassword ? '👁️' : '👁️‍🗨️'}</Text>
              </Pressable>
            </View>

            {/* Confirm Password */}
            <View style={styles.inputWrapper}>
              <Text style={styles.inputIcon}>🔒</Text>
              <TextInput
                style={styles.input}
                placeholder="Confirma parola"
                placeholderTextColor={DUO.textMuted}
                value={confirmPassword}
                onChangeText={setConfirmPassword}
                secureTextEntry={!showPassword}
                autoCapitalize="none"
              />
            </View>

            {/* Register button */}
            <DuoButton
              title={loading ? 'SE CREEAZA...' : 'CREEAZA CONT'}
              onPress={handleRegister}
              disabled={loading}
              color={DUO.green}
              glow
              style={styles.mainBtn}
            />

            {loading && <ActivityIndicator color={DUO.green} style={{ marginTop: 12 }} />}
          </View>

          {/* Login link */}
          <Pressable onPress={() => router.back()} style={styles.switchBtn}>
            <Text style={styles.switchText}>
              Ai deja cont? <Text style={styles.switchLink}>Logare →</Text>
            </Text>
          </Pressable>
        </ScrollView>

      </KeyboardAvoidingView>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  bgWrap: {
    flex: 1,
    backgroundColor: DUO.bg,
  },
  bgImage: {
    resizeMode: 'cover',
  },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(15, 23, 42, 0.82)',
  },
  container: {
    flex: 1,
  },
  scroll: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingHorizontal: 28,
    paddingBottom: 120,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 24,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
    marginBottom: 8,
  },
  logoDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: DUO.green,
    shadowColor: DUO.green,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 6,
    elevation: 6,
  },
  logoText: {
    fontSize: 26,
    fontFamily: DUO.fontBold,
    color: DUO.textSecondary,
    letterSpacing: -0.5,
  },
  logoPill: {
    backgroundColor: DUO.green,
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 3,
  },
  logoPillText: {
    fontSize: 22,
    fontFamily: DUO.fontBlack,
    color: DUO.bg,
    letterSpacing: 2,
  },
  accentLine: {
    width: 30,
    height: 3,
    borderRadius: 2,
    backgroundColor: DUO.green,
    marginBottom: 10,
    opacity: 0.5,
  },
  title: {
    fontSize: 22,
    fontFamily: DUO.fontExtraBold,
    color: DUO.textPrimary,
    letterSpacing: 0.5,
  },
  formCard: {
    backgroundColor: 'rgba(30, 41, 59, 0.8)',
    borderRadius: DUO.radiusLg,
    borderWidth: 1,
    borderColor: 'rgba(51, 65, 85, 0.6)',
    padding: 20,
  },
  errorCard: {
    backgroundColor: 'rgba(248, 113, 113, 0.15)',
    borderWidth: 1,
    borderColor: DUO.red,
    borderRadius: DUO.radius,
    padding: 14,
    marginBottom: 16,
  },
  errorText: {
    color: DUO.red,
    fontFamily: DUO.fontSemiBold,
    fontSize: 14,
    textAlign: 'center',
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(15, 23, 42, 0.6)',
    borderRadius: DUO.radius,
    borderWidth: 1,
    borderColor: 'rgba(51, 65, 85, 0.5)',
    paddingHorizontal: 14,
    marginBottom: 14,
    height: 54,
  },
  inputIcon: {
    fontSize: 18,
    marginRight: 10,
  },
  input: {
    flex: 1,
    color: DUO.textPrimary,
    fontFamily: DUO.fontMedium,
    fontSize: 16,
  },
  eyeBtn: {
    padding: 6,
  },
  eyeIcon: {
    fontSize: 18,
  },
  mainBtn: {
    width: '100%',
  },
  switchBtn: {
    alignItems: 'center',
    marginTop: 20,
  },
  switchText: {
    color: DUO.textSecondary,
    fontFamily: DUO.fontMedium,
    fontSize: 15,
  },
  switchLink: {
    color: DUO.green,
    fontFamily: DUO.fontBold,
  },
});
