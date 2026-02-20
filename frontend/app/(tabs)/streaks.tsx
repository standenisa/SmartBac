import { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Animated,
  Dimensions
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import AsyncStorage from '@react-native-async-storage/async-storage';

const { width } = Dimensions.get('window');

interface StreakData {
  currentStreak: number;
  longestStreak: number;
  totalDaysStudied: number;
  lastStudyDate: string | null;
  weeklyActivity: boolean[];
  achievements: Achievement[];
}

interface Achievement {
  id: string;
  title: string;
  description: string;
  emoji: string;
  unlocked: boolean;
  unlockedDate?: string;
  requirement: number;
}

interface DailyChallenge {
  id: string;
  title: string;
  description: string;
  target: number;
  current: number;
  reward: number;
  emoji: string;
}

const ACHIEVEMENTS: Achievement[] = [
  { id: 'streak_3', title: 'Getting Started', description: '3 day streak', emoji: '🌱', unlocked: false, requirement: 3 },
  { id: 'streak_7', title: 'One Week Warrior', description: '7 day streak', emoji: '🔥', unlocked: false, requirement: 7 },
  { id: 'streak_14', title: 'Two Week Champion', description: '14 day streak', emoji: '⚡', unlocked: false, requirement: 14 },
  { id: 'streak_30', title: 'Monthly Master', description: '30 day streak', emoji: '🏆', unlocked: false, requirement: 30 },
  { id: 'streak_60', title: 'Dedicated Scholar', description: '60 day streak', emoji: '💎', unlocked: false, requirement: 60 },
  { id: 'streak_100', title: 'Legendary Learner', description: '100 day streak', emoji: '👑', unlocked: false, requirement: 100 },
];

export default function StreaksScreen() {
  const [streakData, setStreakData] = useState<StreakData>({
    currentStreak: 0,
    longestStreak: 0,
    totalDaysStudied: 0,
    lastStudyDate: null,
    weeklyActivity: [false, false, false, false, false, false, false],
    achievements: ACHIEVEMENTS,
  });

  const [dailyChallenges, setDailyChallenges] = useState<DailyChallenge[]>([
    { id: '1', title: 'Exercise Master', description: 'Complete 5 exercises', target: 5, current: 0, reward: 10, emoji: '✏️' },
    { id: '2', title: 'Perfect Score', description: 'Get 3 correct in a row', target: 3, current: 0, reward: 15, emoji: '🎯' },
    { id: '3', title: 'Study Session', description: 'Study for 30 minutes', target: 30, current: 0, reward: 20, emoji: '⏰' },
  ]);

  const [todayCompleted, setTodayCompleted] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);

  useEffect(() => {
    loadStreakData();
    loadChallengeProgress();
  }, []);

  const loadStreakData = async () => {
    try {
      const stored = await AsyncStorage.getItem('streakData');
      if (stored) {
        const data = JSON.parse(stored);

        // Check if streak should continue or reset
        const today = new Date().toDateString();
        const yesterday = new Date(Date.now() - 86400000).toDateString();

        if (data.lastStudyDate === today) {
          setTodayCompleted(true);
          setStreakData(data);
        } else if (data.lastStudyDate === yesterday) {
          // Streak can continue
          setStreakData(data);
        } else if (data.lastStudyDate) {
          // Streak broken - reset current streak but keep longest
          setStreakData({
            ...data,
            currentStreak: 0,
            weeklyActivity: [false, false, false, false, false, false, false],
          });
        }
      }

      // Fetch stats from backend
      const response = await fetch('http://localhost:5000/api/stats');
      const stats = await response.json();

      // Update challenges based on actual stats
      setDailyChallenges(prev => prev.map(c => {
        if (c.id === '1') {
          return { ...c, current: Math.min(stats.total_attempts || 0, c.target) };
        }
        return c;
      }));
    } catch (error) {
      console.log('Error loading streak data:', error);
    }
  };

  const loadChallengeProgress = async () => {
    try {
      const stored = await AsyncStorage.getItem('dailyChallenges');
      const today = new Date().toDateString();

      if (stored) {
        const data = JSON.parse(stored);
        if (data.date === today) {
          setDailyChallenges(data.challenges);
        }
      }
    } catch (error) {
      console.log('Error loading challenges:', error);
    }
  };

  const markTodayAsStudied = async () => {
    if (todayCompleted) return;

    const today = new Date();
    const dayOfWeek = today.getDay();

    const newWeeklyActivity = [...streakData.weeklyActivity];
    newWeeklyActivity[dayOfWeek] = true;

    const newStreak = streakData.currentStreak + 1;
    const newLongest = Math.max(newStreak, streakData.longestStreak);

    // Check for new achievements
    const updatedAchievements = streakData.achievements.map(a => {
      if (!a.unlocked && newStreak >= a.requirement) {
        return { ...a, unlocked: true, unlockedDate: today.toISOString() };
      }
      return a;
    });

    const newData: StreakData = {
      currentStreak: newStreak,
      longestStreak: newLongest,
      totalDaysStudied: streakData.totalDaysStudied + 1,
      lastStudyDate: today.toDateString(),
      weeklyActivity: newWeeklyActivity,
      achievements: updatedAchievements,
    };

    setStreakData(newData);
    setTodayCompleted(true);
    setShowCelebration(true);

    await AsyncStorage.setItem('streakData', JSON.stringify(newData));

    setTimeout(() => setShowCelebration(false), 2000);
  };

  const getDayName = (index: number): string => {
    const days = ['D', 'L', 'M', 'M', 'J', 'V', 'S'];
    return days[index];
  };

  const getStreakEmoji = (streak: number): string => {
    if (streak >= 100) return '👑';
    if (streak >= 60) return '💎';
    if (streak >= 30) return '🏆';
    if (streak >= 14) return '⚡';
    if (streak >= 7) return '🔥';
    if (streak >= 3) return '🌱';
    return '✨';
  };

  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        <LinearGradient
          colors={['#f97316', '#ea580c']}
          style={styles.header}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <Text style={styles.headerTitle}>Study Streaks</Text>
          <Text style={styles.headerSubtitle}>Build consistent study habits</Text>
        </LinearGradient>

        {/* Main Streak Card */}
        <View style={styles.streakCard}>
          <LinearGradient
            colors={streakData.currentStreak > 0 ? ['#fef3c7', '#fde68a'] : ['#f3f4f6', '#e5e7eb']}
            style={styles.streakCardGradient}
          >
            <Text style={styles.streakEmoji}>{getStreakEmoji(streakData.currentStreak)}</Text>
            <Text style={styles.streakNumber}>{streakData.currentStreak}</Text>
            <Text style={styles.streakLabel}>Day Streak</Text>

            {!todayCompleted && (
              <TouchableOpacity
                style={styles.checkInButton}
                onPress={markTodayAsStudied}
              >
                <LinearGradient
                  colors={['#22c55e', '#16a34a']}
                  style={styles.checkInGradient}
                >
                  <Text style={styles.checkInText}>Check In Today!</Text>
                </LinearGradient>
              </TouchableOpacity>
            )}

            {todayCompleted && (
              <View style={styles.completedBadge}>
                <Text style={styles.completedText}>✓ Today Complete!</Text>
              </View>
            )}
          </LinearGradient>
        </View>

        {/* Weekly Activity */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>This Week</Text>
          <View style={styles.weekContainer}>
            {streakData.weeklyActivity.map((active, index) => (
              <View key={index} style={styles.dayColumn}>
                <View style={[
                  styles.dayCircle,
                  active && styles.dayCircleActive,
                  index === new Date().getDay() && styles.dayCircleToday
                ]}>
                  {active && <Text style={styles.dayCheck}>✓</Text>}
                </View>
                <Text style={[
                  styles.dayLabel,
                  index === new Date().getDay() && styles.dayLabelToday
                ]}>
                  {getDayName(index)}
                </Text>
              </View>
            ))}
          </View>
        </View>

        {/* Stats Row */}
        <View style={styles.statsRow}>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{streakData.longestStreak}</Text>
            <Text style={styles.statLabel}>Longest Streak</Text>
          </View>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{streakData.totalDaysStudied}</Text>
            <Text style={styles.statLabel}>Total Days</Text>
          </View>
        </View>

        {/* Daily Challenges */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Daily Challenges</Text>
          {dailyChallenges.map((challenge) => {
            const progress = Math.min(challenge.current / challenge.target, 1);
            const completed = challenge.current >= challenge.target;

            return (
              <View key={challenge.id} style={styles.challengeCard}>
                <View style={styles.challengeHeader}>
                  <Text style={styles.challengeEmoji}>{challenge.emoji}</Text>
                  <View style={styles.challengeInfo}>
                    <Text style={styles.challengeTitle}>{challenge.title}</Text>
                    <Text style={styles.challengeDesc}>{challenge.description}</Text>
                  </View>
                  <View style={styles.challengeReward}>
                    <Text style={styles.rewardText}>+{challenge.reward}</Text>
                    <Text style={styles.rewardLabel}>pts</Text>
                  </View>
                </View>
                <View style={styles.progressBarBg}>
                  <LinearGradient
                    colors={completed ? ['#22c55e', '#16a34a'] : ['#f97316', '#ea580c']}
                    style={[styles.progressBarFill, { width: `${progress * 100}%` }]}
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 0 }}
                  />
                </View>
                <Text style={styles.progressText}>
                  {challenge.current}/{challenge.target} {completed ? '✓' : ''}
                </Text>
              </View>
            );
          })}
        </View>

        {/* Achievements */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Achievements</Text>
          <View style={styles.achievementsGrid}>
            {streakData.achievements.map((achievement) => (
              <View
                key={achievement.id}
                style={[
                  styles.achievementCard,
                  !achievement.unlocked && styles.achievementLocked
                ]}
              >
                <Text style={[
                  styles.achievementEmoji,
                  !achievement.unlocked && styles.achievementEmojiLocked
                ]}>
                  {achievement.emoji}
                </Text>
                <Text style={[
                  styles.achievementTitle,
                  !achievement.unlocked && styles.achievementTitleLocked
                ]}>
                  {achievement.title}
                </Text>
                <Text style={styles.achievementDesc}>
                  {achievement.description}
                </Text>
                {!achievement.unlocked && (
                  <View style={styles.lockBadge}>
                    <Text style={styles.lockText}>🔒</Text>
                  </View>
                )}
              </View>
            ))}
          </View>
        </View>

        {/* Motivation Quote */}
        <View style={styles.quoteCard}>
          <Text style={styles.quoteText}>
            "Success is the sum of small efforts, repeated day in and day out."
          </Text>
          <Text style={styles.quoteAuthor}>- Robert Collier</Text>
        </View>

        <View style={{ height: 100 }} />
      </ScrollView>

      {/* Celebration Overlay */}
      {showCelebration && (
        <View style={styles.celebrationOverlay}>
          <Text style={styles.celebrationEmoji}>🎉</Text>
          <Text style={styles.celebrationText}>Streak Extended!</Text>
          <Text style={styles.celebrationSubtext}>
            {streakData.currentStreak} days and counting!
          </Text>
        </View>
      )}
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
  streakCard: {
    marginHorizontal: 20,
    marginTop: -20,
    borderRadius: 24,
    overflow: 'hidden',
    shadowColor: '#f97316',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 8,
  },
  streakCardGradient: {
    padding: 30,
    alignItems: 'center',
  },
  streakEmoji: {
    fontSize: 48,
    marginBottom: 8,
  },
  streakNumber: {
    fontSize: 72,
    fontWeight: '800',
    color: '#1f2937',
  },
  streakLabel: {
    fontSize: 18,
    fontWeight: '600',
    color: '#6b7280',
    marginBottom: 20,
  },
  checkInButton: {
    borderRadius: 16,
    overflow: 'hidden',
  },
  checkInGradient: {
    paddingHorizontal: 32,
    paddingVertical: 14,
  },
  checkInText: {
    fontSize: 16,
    fontWeight: '700',
    color: 'white',
  },
  completedBadge: {
    backgroundColor: '#dcfce7',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 12,
  },
  completedText: {
    fontSize: 14,
    fontWeight: '700',
    color: '#16a34a',
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
  weekContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  dayColumn: {
    alignItems: 'center',
  },
  dayCircle: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 6,
  },
  dayCircleActive: {
    backgroundColor: '#22c55e',
  },
  dayCircleToday: {
    borderWidth: 2,
    borderColor: '#f97316',
  },
  dayCheck: {
    color: 'white',
    fontSize: 16,
    fontWeight: '700',
  },
  dayLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#9ca3af',
  },
  dayLabelToday: {
    color: '#f97316',
  },
  statsRow: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    gap: 12,
  },
  statBox: {
    flex: 1,
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 20,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  statNumber: {
    fontSize: 32,
    fontWeight: '800',
    color: '#1f2937',
  },
  statLabel: {
    fontSize: 13,
    color: '#6b7280',
    marginTop: 4,
  },
  challengeCard: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  challengeHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  challengeEmoji: {
    fontSize: 28,
    marginRight: 12,
  },
  challengeInfo: {
    flex: 1,
  },
  challengeTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#1f2937',
  },
  challengeDesc: {
    fontSize: 12,
    color: '#6b7280',
  },
  challengeReward: {
    alignItems: 'center',
    backgroundColor: '#fef3c7',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 10,
  },
  rewardText: {
    fontSize: 14,
    fontWeight: '800',
    color: '#d97706',
  },
  rewardLabel: {
    fontSize: 10,
    color: '#d97706',
  },
  progressBarBg: {
    height: 8,
    backgroundColor: '#e5e7eb',
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 6,
  },
  progressBarFill: {
    height: '100%',
    borderRadius: 4,
  },
  progressText: {
    fontSize: 12,
    color: '#6b7280',
    textAlign: 'right',
  },
  achievementsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  achievementCard: {
    width: (width - 52) / 2,
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  achievementLocked: {
    opacity: 0.6,
  },
  achievementEmoji: {
    fontSize: 32,
    marginBottom: 8,
  },
  achievementEmojiLocked: {
    opacity: 0.4,
  },
  achievementTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#1f2937',
    textAlign: 'center',
    marginBottom: 4,
  },
  achievementTitleLocked: {
    color: '#9ca3af',
  },
  achievementDesc: {
    fontSize: 11,
    color: '#6b7280',
    textAlign: 'center',
  },
  lockBadge: {
    position: 'absolute',
    top: 8,
    right: 8,
  },
  lockText: {
    fontSize: 14,
  },
  quoteCard: {
    marginHorizontal: 20,
    backgroundColor: '#1f2937',
    padding: 24,
    borderRadius: 20,
  },
  quoteText: {
    fontSize: 16,
    fontStyle: 'italic',
    color: 'white',
    lineHeight: 24,
    marginBottom: 12,
  },
  quoteAuthor: {
    fontSize: 13,
    color: '#9ca3af',
    textAlign: 'right',
  },
  celebrationOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.8)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  celebrationEmoji: {
    fontSize: 80,
    marginBottom: 20,
  },
  celebrationText: {
    fontSize: 32,
    fontWeight: '800',
    color: 'white',
    marginBottom: 8,
  },
  celebrationSubtext: {
    fontSize: 18,
    color: '#fbbf24',
  },
});
