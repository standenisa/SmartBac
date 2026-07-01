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

export default function LoginScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const { login } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setError('');
    if (!email.trim() || !password.trim()) {
      setError('Completeaza toate campurile');
      return;
    }
    setLoading(true);
    try {
      await login(email.trim(), password);
    } catch (e: any) {
      setError(e.message || 'Eroare la autentificare');
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
          {/* Logo */}
          <View style={styles.logoContainer}>
            <View style={styles.logoRow}>
              <View style={styles.logoDot} />
              <Text style={styles.title}>smart</Text>
              <View style={styles.logoPill}>
                <Text style={styles.logoPillText}>BAC</Text>
              </View>
            </View>
            <View style={styles.accentLine} />
            <Text style={styles.subtitle}>Pregatire inteligenta pentru Bacalaureat</Text>
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
                placeholder="Email sau username"
                placeholderTextColor={DUO.textMuted}
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
                autoCorrect={false}
              />
            </View>

            {/* Password */}
            <View style={styles.inputWrapper}>
              <Text style={styles.inputIcon}>🔒</Text>
              <TextInput
                style={[styles.input, { flex: 1 }]}
                placeholder="Parola"
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

            {/* Forgot password */}
            <Pressable style={styles.forgotBtn}>
              <Text style={styles.forgotText}>Ai uitat parola?</Text>
            </Pressable>

            {/* Login button */}
            <DuoButton
              title={loading ? 'SE INCARCA...' : 'LOGARE'}
              onPress={handleLogin}
              disabled={loading}
              color={DUO.green}
              glow
              style={styles.mainBtn}
            />

            {loading && <ActivityIndicator color={DUO.green} style={{ marginTop: 12 }} />}
          </View>

          {/* Separator */}
          <View style={styles.separator}>
            <View style={styles.separatorLine} />
            <Text style={styles.separatorText}>SAU</Text>
            <View style={styles.separatorLine} />
          </View>

          {/* Register link */}
          <Pressable onPress={() => router.push('/register')} style={styles.switchBtn}>
            <Text style={styles.switchText}>
              Nu ai un cont? <Text style={styles.switchLink}>Inregistreaza-te →</Text>
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
    marginBottom: 32,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  logoDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: DUO.green,
    shadowColor: DUO.green,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 8,
    elevation: 6,
  },
  title: {
    fontSize: 34,
    fontFamily: DUO.fontBold,
    color: DUO.textSecondary,
    letterSpacing: -0.5,
  },
  logoPill: {
    backgroundColor: DUO.green,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 4,
    shadowColor: DUO.green,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  logoPillText: {
    fontSize: 28,
    fontFamily: DUO.fontBlack,
    color: DUO.bg,
    letterSpacing: 2,
  },
  accentLine: {
    width: 40,
    height: 3,
    borderRadius: 2,
    backgroundColor: DUO.green,
    marginTop: 10,
    marginBottom: 8,
    opacity: 0.5,
  },
  subtitle: {
    fontSize: 14,
    fontFamily: DUO.fontMedium,
    color: DUO.textSecondary,
    marginTop: 6,
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
  forgotBtn: {
    alignSelf: 'flex-end',
    marginBottom: 18,
  },
  forgotText: {
    color: DUO.textMuted,
    fontFamily: DUO.fontMedium,
    fontSize: 13,
  },
  mainBtn: {
    width: '100%',
  },
  separator: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 20,
  },
  separatorLine: {
    flex: 1,
    height: 1,
    backgroundColor: 'rgba(51, 65, 85, 0.5)',
  },
  separatorText: {
    color: DUO.textMuted,
    fontFamily: DUO.fontSemiBold,
    fontSize: 13,
    marginHorizontal: 16,
  },
  switchBtn: {
    alignItems: 'center',
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
