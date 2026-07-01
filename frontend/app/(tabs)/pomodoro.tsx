import { useState, useEffect, useRef } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  Vibration,
  Animated,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { DUO } from '@/constants/duo';

type TimerMode = 'work' | 'shortBreak' | 'longBreak';

interface TimerConfig {
  work: number;
  shortBreak: number;
  longBreak: number;
}

const DEFAULT_TIMES: TimerConfig = {
  work: 25 * 60,
  shortBreak: 5 * 60,
  longBreak: 15 * 60,
};

const MODE_COLORS: Record<TimerMode, [string, string]> = {
  work: [DUO.red, DUO.redDark],
  shortBreak: [DUO.green, DUO.greenDark],
  longBreak: [DUO.blue, DUO.blueDark],
};

const MODE_LABELS: Record<TimerMode, string> = {
  work: 'Focus Time',
  shortBreak: 'Short Break',
  longBreak: 'Long Break',
};

export default function PomodoroScreen() {
  const [mode, setMode] = useState<TimerMode>('work');
  const [timeLeft, setTimeLeft] = useState(DEFAULT_TIMES.work);
  const [isRunning, setIsRunning] = useState(false);
  const [sessionsCompleted, setSessionsCompleted] = useState(0);
  const [totalFocusTime, setTotalFocusTime] = useState(0);

  const pulseAnim = useRef(new Animated.Value(1)).current;
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (isRunning) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.05,
            duration: 1000,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 1000,
            useNativeDriver: true,
          }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1);
    }
  }, [isRunning]);

  useEffect(() => {
    if (isRunning && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleTimerComplete();
            return 0;
          }
          if (mode === 'work') {
            setTotalFocusTime(t => t + 1);
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isRunning, mode]);

  const handleTimerComplete = () => {
    setIsRunning(false);
    Vibration.vibrate([0, 500, 200, 500]);

    if (mode === 'work') {
      const newSessions = sessionsCompleted + 1;
      setSessionsCompleted(newSessions);

      if (newSessions % 4 === 0) {
        setMode('longBreak');
        setTimeLeft(DEFAULT_TIMES.longBreak);
      } else {
        setMode('shortBreak');
        setTimeLeft(DEFAULT_TIMES.shortBreak);
      }
    } else {
      setMode('work');
      setTimeLeft(DEFAULT_TIMES.work);
    }
  };

  const toggleTimer = () => {
    setIsRunning(!isRunning);
  };

  const resetTimer = () => {
    setIsRunning(false);
    setTimeLeft(DEFAULT_TIMES[mode]);
  };

  const switchMode = (newMode: TimerMode) => {
    setIsRunning(false);
    setMode(newMode);
    setTimeLeft(DEFAULT_TIMES[newMode]);
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const formatTotalTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[DUO.bgLight, DUO.bg]}
        style={styles.gradient}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Pomodoro Timer</Text>
          <Text style={styles.headerSubtitle}>Stay focused, take breaks</Text>
        </View>

        {/* Mode Selector */}
        <View style={styles.modeSelector}>
          {(['work', 'shortBreak', 'longBreak'] as TimerMode[]).map((m) => (
            <TouchableOpacity
              key={m}
              style={[
                styles.modeButton,
                mode === m && { backgroundColor: MODE_COLORS[m][0] + '30', borderColor: MODE_COLORS[m][0] + '50' }
              ]}
              onPress={() => switchMode(m)}
            >
              <Text style={[
                styles.modeButtonText,
                mode === m && { color: MODE_COLORS[m][0] }
              ]}>
                {m === 'work' ? 'Focus' : m === 'shortBreak' ? 'Short' : 'Long'}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Timer Circle */}
        <View style={styles.timerContainer}>
          <Animated.View
            style={[
              styles.timerCircleOuter,
              { transform: [{ scale: pulseAnim }] }
            ]}
          >
            <LinearGradient
              colors={MODE_COLORS[mode]}
              style={styles.timerCircleGradient}
            >
              <View style={styles.timerCircleInner}>
                <Text style={styles.modeLabel}>{MODE_LABELS[mode]}</Text>
                <Text style={styles.timerText}>{formatTime(timeLeft)}</Text>
                <Text style={styles.sessionLabel}>
                  Session {sessionsCompleted + 1}
                </Text>
              </View>
            </LinearGradient>
          </Animated.View>
        </View>

        {/* Controls */}
        <View style={styles.controls}>
          <TouchableOpacity
            style={styles.resetButton}
            onPress={resetTimer}
          >
            <Text style={styles.resetButtonText}>Reset</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.mainButton, { shadowColor: MODE_COLORS[mode][0] }]}
            onPress={toggleTimer}
          >
            <LinearGradient
              colors={isRunning ? [DUO.surface, DUO.surfaceLight] : MODE_COLORS[mode]}
              style={styles.mainButtonGradient}
            >
              <Text style={styles.mainButtonText}>
                {isRunning ? 'PAUSE' : 'START'}
              </Text>
            </LinearGradient>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.skipButton}
            onPress={handleTimerComplete}
          >
            <Text style={styles.skipButtonText}>Skip</Text>
          </TouchableOpacity>
        </View>

        {/* Stats */}
        <View style={styles.statsContainer}>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{sessionsCompleted}</Text>
            <Text style={styles.statLabel}>Sessions</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{formatTotalTime(totalFocusTime)}</Text>
            <Text style={styles.statLabel}>Focus Time</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{4 - (sessionsCompleted % 4)}</Text>
            <Text style={styles.statLabel}>Until Long Break</Text>
          </View>
        </View>

        {/* Tips */}
        <View style={styles.tipsCard}>
          <Text style={styles.tipsTitle}>Pomodoro Technique</Text>
          <Text style={styles.tipsText}>
            1. Focus for 25 minutes{'\n'}
            2. Take a 5-minute break{'\n'}
            3. After 4 sessions, take a 15-minute break{'\n'}
            4. Repeat and stay productive!
          </Text>
        </View>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
    paddingTop: 60,
  },
  header: {
    alignItems: 'center',
    marginBottom: 20,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: DUO.textPrimary,
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 14,
    color: DUO.textSecondary,
  },
  modeSelector: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 12,
    marginBottom: 30,
    paddingHorizontal: 20,
  },
  modeButton: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: DUO.radiusFull,
    backgroundColor: DUO.card,
    borderWidth: 1,
    borderColor: DUO.surface,
  },
  modeButtonText: {
    fontSize: 14,
    fontWeight: '700',
    color: DUO.textMuted,
  },
  timerContainer: {
    alignItems: 'center',
    marginBottom: 30,
  },
  timerCircleOuter: {
    width: 280,
    height: 280,
    borderRadius: 140,
    padding: 8,
  },
  timerCircleGradient: {
    flex: 1,
    borderRadius: 140,
    justifyContent: 'center',
    alignItems: 'center',
  },
  timerCircleInner: {
    width: 220,
    height: 220,
    borderRadius: 110,
    backgroundColor: DUO.bg,
    justifyContent: 'center',
    alignItems: 'center',
  },
  modeLabel: {
    fontSize: 14,
    color: DUO.textSecondary,
    fontWeight: '600',
    marginBottom: 8,
  },
  timerText: {
    fontSize: 56,
    fontWeight: '800',
    color: DUO.textPrimary,
    fontVariant: ['tabular-nums'],
  },
  sessionLabel: {
    fontSize: 12,
    color: DUO.textMuted,
    marginTop: 8,
    fontWeight: '600',
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 20,
    marginBottom: 30,
  },
  resetButton: {
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  resetButtonText: {
    fontSize: 16,
    color: DUO.textSecondary,
    fontWeight: '700',
  },
  mainButton: {
    borderRadius: 30,
    overflow: 'hidden',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  mainButtonGradient: {
    paddingHorizontal: 50,
    paddingVertical: 18,
  },
  mainButtonText: {
    fontSize: 18,
    fontWeight: '800',
    color: DUO.textPrimary,
    letterSpacing: 2,
  },
  skipButton: {
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  skipButtonText: {
    fontSize: 16,
    color: DUO.textSecondary,
    fontWeight: '700',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 12,
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  statCard: {
    flex: 1,
    backgroundColor: DUO.card,
    borderRadius: DUO.radius,
    padding: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: DUO.surface,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: '800',
    color: DUO.textPrimary,
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 11,
    color: DUO.textMuted,
    textAlign: 'center',
    fontWeight: '600',
  },
  tipsCard: {
    marginHorizontal: 20,
    backgroundColor: DUO.card,
    borderRadius: DUO.radius,
    padding: 16,
    borderWidth: 1,
    borderColor: DUO.yellow + '20',
  },
  tipsTitle: {
    fontSize: 14,
    fontWeight: '800',
    color: DUO.yellow,
    marginBottom: 8,
  },
  tipsText: {
    fontSize: 13,
    color: DUO.textSecondary,
    lineHeight: 22,
    fontWeight: '600',
  },
});
