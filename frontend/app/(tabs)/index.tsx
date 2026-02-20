import { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Dimensions
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';

const { width } = Dimensions.get('window');

interface Stats {
  total_attempts: number;
  correct_answers: number;
  accuracy: number;
}

interface DayInfo {
  day: string;
  date: number;
  isToday: boolean;
  isSelected: boolean;
}

export default function HomeScreen() {
  const [selectedProfile, setSelectedProfile] = useState<'M1' | 'M2' | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [selectedDate, setSelectedDate] = useState(new Date().getDate());
  const [greeting, setGreeting] = useState('');

  useEffect(() => {
    fetchStats();
    fetchProfile();
    updateGreeting();
  }, []);

  const updateGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Bună dimineața');
    else if (hour < 18) setGreeting('Bună ziua');
    else setGreeting('Bună seara');
  };

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.log('Error fetching stats:', error);
    }
  };

  const fetchProfile = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/get-profile');
      const data = await response.json();
      if (data.profile) {
        setSelectedProfile(data.profile);
      }
    } catch (error) {
      console.log('Error fetching profile:', error);
    }
  };

  // Generate week days
  const getWeekDays = (): DayInfo[] => {
    const days = ['Dum', 'Lun', 'Mar', 'Mie', 'Joi', 'Vin', 'Sâm'];
    const today = new Date();
    const result: DayInfo[] = [];

    for (let i = -3; i <= 3; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      result.push({
        day: days[date.getDay()],
        date: date.getDate(),
        isToday: i === 0,
        isSelected: date.getDate() === selectedDate
      });
    }
    return result;
  };

  const completedToday = stats?.total_attempts || 0;
  const dailyGoal = 5;
  const progressPercent = Math.min((completedToday / dailyGoal) * 100, 100);

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>{greeting}! </Text>
            <Text style={styles.userName}>Elev BAC 2025</Text>
          </View>
          <TouchableOpacity style={styles.avatarContainer}>
            <LinearGradient
              colors={['#a78bfa', '#8b5cf6']}
              style={styles.avatar}
            >
              <Text style={styles.avatarText}>E</Text>
            </LinearGradient>
          </TouchableOpacity>
        </View>

        {/* Calendar Strip */}
        <View style={styles.calendarContainer}>
          <View style={styles.calendarHeader}>
            <Text style={styles.monthYear}>
              {new Date().toLocaleDateString('ro-RO', { month: 'long', year: 'numeric' })}
            </Text>
          </View>
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={styles.daysContainer}
          >
            {getWeekDays().map((item, index) => (
              <TouchableOpacity
                key={index}
                style={[
                  styles.dayItem,
                  item.isSelected && styles.dayItemSelected
                ]}
                onPress={() => setSelectedDate(item.date)}
              >
                <Text style={[
                  styles.dayName,
                  item.isSelected && styles.dayNameSelected
                ]}>
                  {item.day}
                </Text>
                <Text style={[
                  styles.dayNumber,
                  item.isSelected && styles.dayNumberSelected
                ]}>
                  {item.date}
                </Text>
                {item.isToday && !item.isSelected && (
                  <View style={styles.todayDot} />
                )}
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* Activity Cards Row */}
        <View style={styles.activityRow}>
          {/* Total Activity Card */}
          <TouchableOpacity
            style={styles.activityCard}
            onPress={() => router.push('/(tabs)/exercises')}
          >
            <LinearGradient
              colors={['#fef3c7', '#fde68a']}
              style={styles.activityGradient}
            >
              <View style={styles.activityIcon}>
                <Text style={styles.activityEmoji}>📚</Text>
              </View>
              <Text style={styles.activityTitle}>Activitate</Text>
              <Text style={styles.activityTitle}>Totală</Text>
              <View style={styles.activityStats}>
                <Text style={styles.activityNumber}>{stats?.total_attempts || 0}</Text>
                <Text style={styles.activityLabel}>exerciții</Text>
              </View>
            </LinearGradient>
          </TouchableOpacity>

          {/* Accuracy Card */}
          <TouchableOpacity
            style={styles.activityCard}
            onPress={() => router.push('/(tabs)/exercises')}
          >
            <LinearGradient
              colors={['#dbeafe', '#bfdbfe']}
              style={styles.activityGradient}
            >
              <View style={styles.activityIcon}>
                <Text style={styles.activityEmoji}>🎯</Text>
              </View>
              <Text style={styles.activityTitle}>Acuratețe</Text>
              <Text style={styles.activityTitle}>Medie</Text>
              <View style={styles.activityStats}>
                <Text style={styles.activityNumber}>{stats?.accuracy || 0}%</Text>
                <Text style={styles.activityLabel}>corect</Text>
              </View>
            </LinearGradient>
          </TouchableOpacity>
        </View>

        {/* Daily Goal Card */}
        <TouchableOpacity style={styles.goalCard}>
          <LinearGradient
            colors={['#f0fdf4', '#dcfce7']}
            style={styles.goalGradient}
          >
            <View style={styles.goalHeader}>
              <View>
                <Text style={styles.goalTitle}>Obiectivul de azi</Text>
                <Text style={styles.goalSubtitle}>{completedToday} din {dailyGoal} completate</Text>
              </View>
              <View style={styles.goalIconContainer}>
                <Text style={styles.goalEmoji}>🌱</Text>
              </View>
            </View>
            <View style={styles.progressBarContainer}>
              <View style={styles.progressBarBg}>
                <LinearGradient
                  colors={['#22c55e', '#16a34a']}
                  style={[styles.progressBarFill, { width: `${progressPercent}%` }]}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                />
              </View>
              <Text style={styles.progressText}>{Math.round(progressPercent)}%</Text>
            </View>
          </LinearGradient>
        </TouchableOpacity>

        {/* Quick Actions */}
        <Text style={styles.sectionTitle}>Acțiuni Rapide</Text>

        <View style={styles.quickActionsGrid}>
          {/* Exam Practice */}
          <TouchableOpacity
            style={styles.quickAction}
            onPress={() => router.push('/(tabs)/exam')}
          >
            <LinearGradient
              colors={['#fae8ff', '#f5d0fe']}
              style={styles.quickActionGradient}
            >
              <Text style={styles.quickActionEmoji}>🎓</Text>
              <Text style={styles.quickActionTitle}>Simulare</Text>
              <Text style={styles.quickActionTitle}>Examen</Text>
              <Text style={styles.quickActionDesc}>3 ore</Text>
            </LinearGradient>
          </TouchableOpacity>

          {/* Pomodoro Timer */}
          <TouchableOpacity
            style={styles.quickAction}
            onPress={() => router.push('/(tabs)/pomodoro')}
          >
            <LinearGradient
              colors={['#fee2e2', '#fecaca']}
              style={styles.quickActionGradient}
            >
              <Text style={styles.quickActionEmoji}>⏰</Text>
              <Text style={styles.quickActionTitle}>Pomodoro</Text>
              <Text style={styles.quickActionTitle}>Timer</Text>
              <Text style={styles.quickActionDesc}>Focus</Text>
            </LinearGradient>
          </TouchableOpacity>

          {/* Theory */}
          <TouchableOpacity
            style={styles.quickAction}
            onPress={() => router.push('/(tabs)/theory')}
          >
            <LinearGradient
              colors={['#cffafe', '#a5f3fc']}
              style={styles.quickActionGradient}
            >
              <Text style={styles.quickActionEmoji}>📖</Text>
              <Text style={styles.quickActionTitle}>Teorie</Text>
              <Text style={styles.quickActionTitle}>&nbsp;</Text>
              <Text style={styles.quickActionDesc}>Formule</Text>
            </LinearGradient>
          </TouchableOpacity>

          {/* Chat AI */}
          <TouchableOpacity
            style={styles.quickAction}
            onPress={() => router.push('/(tabs)/chat')}
          >
            <LinearGradient
              colors={['#d1fae5', '#a7f3d0']}
              style={styles.quickActionGradient}
            >
              <Text style={styles.quickActionEmoji}>💬</Text>
              <Text style={styles.quickActionTitle}>Chat</Text>
              <Text style={styles.quickActionTitle}>AI</Text>
              <Text style={styles.quickActionDesc}>Ajutor</Text>
            </LinearGradient>
          </TouchableOpacity>
        </View>

        {/* Profile Card */}
        <View style={styles.profileCard}>
          <LinearGradient
            colors={['#8b5cf6', '#7c3aed']}
            style={styles.profileGradient}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
          >
            <View style={styles.profileContent}>
              <View style={styles.profileLeft}>
                <Text style={styles.profileTitle}>Profil BAC</Text>
                <Text style={styles.profileSubtitle}>
                  {selectedProfile
                    ? `${selectedProfile} - ${selectedProfile === 'M1' ? 'Mate-Info' : 'Tehnologic'}`
                    : 'Alege profilul tău'}
                </Text>
              </View>
              <View style={styles.profileButtons}>
                <TouchableOpacity
                  style={[
                    styles.profileBtn,
                    selectedProfile === 'M1' && styles.profileBtnActive
                  ]}
                  onPress={async () => {
                    setSelectedProfile('M1');
                    await fetch('http://localhost:5000/api/set-profile', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ profile: 'M1' })
                    });
                  }}
                >
                  <Text style={[
                    styles.profileBtnText,
                    selectedProfile === 'M1' && styles.profileBtnTextActive
                  ]}>M1</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[
                    styles.profileBtn,
                    selectedProfile === 'M2' && styles.profileBtnActive
                  ]}
                  onPress={async () => {
                    setSelectedProfile('M2');
                    await fetch('http://localhost:5000/api/set-profile', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ profile: 'M2' })
                    });
                  }}
                >
                  <Text style={[
                    styles.profileBtnText,
                    selectedProfile === 'M2' && styles.profileBtnTextActive
                  ]}>M2</Text>
                </TouchableOpacity>
              </View>
            </View>
          </LinearGradient>
        </View>

        {/* Countdown to BAC */}
        <View style={styles.countdownCard}>
          <View style={styles.countdownContent}>
            <View style={styles.countdownLeft}>
              <Text style={styles.countdownLabel}>Zile până la BAC</Text>
              <Text style={styles.countdownNumber}>
                {Math.max(0, Math.ceil((new Date('2025-07-01').getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)))}
              </Text>
            </View>
            <View style={styles.countdownRight}>
              <Text style={styles.countdownEmoji}>⏰</Text>
            </View>
          </View>
          <View style={styles.countdownBar}>
            <LinearGradient
              colors={['#f97316', '#ea580c']}
              style={styles.countdownBarFill}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
            />
          </View>
        </View>

        <View style={{ height: 100 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fafafa',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 60,
    paddingHorizontal: 24,
    paddingBottom: 20,
  },
  greeting: {
    fontSize: 16,
    color: '#6b7280',
    fontWeight: '500',
  },
  userName: {
    fontSize: 24,
    fontWeight: '800',
    color: '#1f2937',
    marginTop: 4,
  },
  avatarContainer: {
    shadowColor: '#8b5cf6',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    fontSize: 20,
    fontWeight: '700',
    color: 'white',
  },
  calendarContainer: {
    paddingHorizontal: 16,
    marginBottom: 20,
  },
  calendarHeader: {
    marginBottom: 12,
    paddingHorizontal: 8,
  },
  monthYear: {
    fontSize: 16,
    fontWeight: '600',
    color: '#374151',
    textTransform: 'capitalize',
  },
  daysContainer: {
    paddingHorizontal: 4,
    gap: 8,
  },
  dayItem: {
    width: 52,
    height: 72,
    borderRadius: 16,
    backgroundColor: 'white',
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  dayItemSelected: {
    backgroundColor: '#8b5cf6',
    shadowColor: '#8b5cf6',
    shadowOpacity: 0.3,
  },
  dayName: {
    fontSize: 12,
    color: '#9ca3af',
    fontWeight: '500',
    marginBottom: 4,
  },
  dayNameSelected: {
    color: 'rgba(255,255,255,0.8)',
  },
  dayNumber: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1f2937',
  },
  dayNumberSelected: {
    color: 'white',
  },
  todayDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#8b5cf6',
    marginTop: 4,
  },
  activityRow: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    gap: 12,
    marginBottom: 16,
  },
  activityCard: {
    flex: 1,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  activityGradient: {
    padding: 16,
    minHeight: 140,
  },
  activityIcon: {
    marginBottom: 8,
  },
  activityEmoji: {
    fontSize: 28,
  },
  activityTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    lineHeight: 18,
  },
  activityStats: {
    marginTop: 'auto',
    paddingTop: 12,
  },
  activityNumber: {
    fontSize: 28,
    fontWeight: '800',
    color: '#1f2937',
  },
  activityLabel: {
    fontSize: 12,
    color: '#6b7280',
    fontWeight: '500',
  },
  goalCard: {
    marginHorizontal: 16,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#22c55e',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 4,
    marginBottom: 24,
  },
  goalGradient: {
    padding: 20,
  },
  goalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  goalTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#166534',
    marginBottom: 4,
  },
  goalSubtitle: {
    fontSize: 14,
    color: '#15803d',
    fontWeight: '500',
  },
  goalIconContainer: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(34, 197, 94, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  goalEmoji: {
    fontSize: 24,
  },
  progressBarContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  progressBarBg: {
    flex: 1,
    height: 10,
    backgroundColor: 'rgba(34, 197, 94, 0.2)',
    borderRadius: 5,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    borderRadius: 5,
  },
  progressText: {
    fontSize: 14,
    fontWeight: '700',
    color: '#166534',
    width: 40,
    textAlign: 'right',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1f2937',
    paddingHorizontal: 24,
    marginBottom: 16,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: 16,
    gap: 12,
    marginBottom: 24,
  },
  quickAction: {
    width: (width - 44) / 2,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  quickActionGradient: {
    padding: 16,
    minHeight: 120,
  },
  quickActionEmoji: {
    fontSize: 32,
    marginBottom: 8,
  },
  quickActionTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#1f2937',
    lineHeight: 20,
  },
  quickActionDesc: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 4,
    fontWeight: '500',
  },
  profileCard: {
    marginHorizontal: 16,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#8b5cf6',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 6,
    marginBottom: 16,
  },
  profileGradient: {
    padding: 20,
  },
  profileContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  profileLeft: {
    flex: 1,
  },
  profileTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: 'white',
    marginBottom: 4,
  },
  profileSubtitle: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
    fontWeight: '500',
  },
  profileButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  profileBtn: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.2)',
  },
  profileBtnActive: {
    backgroundColor: 'white',
  },
  profileBtnText: {
    fontSize: 14,
    fontWeight: '700',
    color: 'rgba(255,255,255,0.9)',
  },
  profileBtnTextActive: {
    color: '#7c3aed',
  },
  countdownCard: {
    marginHorizontal: 16,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.08,
    shadowRadius: 12,
    elevation: 4,
  },
  countdownContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  countdownLeft: {},
  countdownLabel: {
    fontSize: 14,
    color: '#6b7280',
    fontWeight: '500',
    marginBottom: 4,
  },
  countdownNumber: {
    fontSize: 36,
    fontWeight: '800',
    color: '#f97316',
  },
  countdownRight: {},
  countdownEmoji: {
    fontSize: 40,
  },
  countdownBar: {
    height: 6,
    backgroundColor: '#fed7aa',
    borderRadius: 3,
    overflow: 'hidden',
  },
  countdownBarFill: {
    width: '60%',
    height: '100%',
  },
});
