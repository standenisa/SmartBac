import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, Modal } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  xp: number;
  unlocked: boolean;
}

interface GamificationStats {
  xp: number;
  level: number;
  level_name: string;
  xp_progress: number;
  xp_needed: number;
  current_streak: number;
  best_streak: number;
  achievements_count: number;
  total_achievements: number;
}

export default function AchievementsScreen() {
  const [stats, setStats] = useState<GamificationStats | null>(null);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedAchievement, setSelectedAchievement] = useState<Achievement | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, achievementsRes] = await Promise.all([
        fetch('http://localhost:5000/api/gamification/stats'),
        fetch('http://localhost:5000/api/gamification/achievements'),
      ]);

      const statsData = await statsRes.json();
      const achievementsData = await achievementsRes.json();

      if (statsData.success) setStats(statsData);
      if (achievementsData.success) setAchievements(achievementsData.achievements);
    } catch (error) {
      console.log('Error fetching gamification data:', error);
    }
    setLoading(false);
  };

  const getLevelColors = (level: number): [string, string] => {
    const colors: [string, string][] = [
      ['#9ca3af', '#6b7280'], // Level 1 - Gray
      ['#60a5fa', '#3b82f6'], // Level 2 - Blue
      ['#34d399', '#10b981'], // Level 3 - Green
      ['#a78bfa', '#8b5cf6'], // Level 4 - Purple
      ['#f472b6', '#ec4899'], // Level 5 - Pink
      ['#fbbf24', '#f59e0b'], // Level 6 - Yellow
      ['#f97316', '#ea580c'], // Level 7 - Orange
      ['#ef4444', '#dc2626'], // Level 8 - Red
      ['#8b5cf6', '#7c3aed'], // Level 9 - Violet
      ['#fcd34d', '#f59e0b'], // Level 10 - Gold
    ];
    return colors[Math.min(level - 1, 9)];
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Se încarcă...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Achievement Detail Modal */}
      <Modal
        visible={selectedAchievement !== null}
        transparent
        animationType="fade"
        onRequestClose={() => setSelectedAchievement(null)}
      >
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => setSelectedAchievement(null)}
        >
          <View style={styles.achievementModal}>
            {selectedAchievement && (
              <>
                <Text style={styles.modalIcon}>{selectedAchievement.icon}</Text>
                <Text style={styles.modalName}>{selectedAchievement.name}</Text>
                <Text style={styles.modalDescription}>{selectedAchievement.description}</Text>
                <View style={styles.modalXpBadge}>
                  <Text style={styles.modalXpText}>+{selectedAchievement.xp} XP</Text>
                </View>
                {selectedAchievement.unlocked ? (
                  <View style={styles.unlockedBadge}>
                    <Text style={styles.unlockedBadgeText}>✓ Deblocat</Text>
                  </View>
                ) : (
                  <View style={styles.lockedBadge}>
                    <Text style={styles.lockedBadgeText}>🔒 Blocat</Text>
                  </View>
                )}
              </>
            )}
          </View>
        </TouchableOpacity>
      </Modal>

      {/* Header with Level */}
      <LinearGradient
        colors={stats ? getLevelColors(stats.level) : ['#8b5cf6', '#6366f1']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <View style={styles.levelBadge}>
          <Text style={styles.levelNumber}>{stats?.level || 1}</Text>
        </View>
        <Text style={styles.levelName}>{stats?.level_name || 'Începător'}</Text>
        <Text style={styles.xpText}>{stats?.xp || 0} XP</Text>

        {/* XP Progress Bar */}
        <View style={styles.xpBarContainer}>
          <View
            style={[
              styles.xpBar,
              { width: `${stats ? (stats.xp_progress / stats.xp_needed) * 100 : 0}%` },
            ]}
          />
        </View>
        <Text style={styles.xpProgress}>
          {stats?.xp_progress || 0} / {stats?.xp_needed || 100} XP până la nivelul următor
        </Text>
      </LinearGradient>

      {/* Streak Card */}
      <View style={styles.streakCard}>
        <View style={styles.streakItem}>
          <Text style={styles.streakEmoji}>🔥</Text>
          <Text style={styles.streakValue}>{stats?.current_streak || 0}</Text>
          <Text style={styles.streakLabel}>Streak Curent</Text>
        </View>
        <View style={styles.streakDivider} />
        <View style={styles.streakItem}>
          <Text style={styles.streakEmoji}>⭐</Text>
          <Text style={styles.streakValue}>{stats?.best_streak || 0}</Text>
          <Text style={styles.streakLabel}>Cel Mai Bun</Text>
        </View>
        <View style={styles.streakDivider} />
        <View style={styles.streakItem}>
          <Text style={styles.streakEmoji}>🏆</Text>
          <Text style={styles.streakValue}>
            {stats?.achievements_count || 0}/{stats?.total_achievements || 0}
          </Text>
          <Text style={styles.streakLabel}>Achievements</Text>
        </View>
      </View>

      {/* Achievements Section */}
      <View style={styles.achievementsSection}>
        <Text style={styles.sectionTitle}>Achievements</Text>
        <Text style={styles.sectionSubtitle}>
          {stats?.achievements_count || 0} din {stats?.total_achievements || 0} deblocate
        </Text>

        <View style={styles.achievementsGrid}>
          {achievements.map((achievement) => (
            <TouchableOpacity
              key={achievement.id}
              style={[
                styles.achievementCard,
                !achievement.unlocked && styles.achievementCardLocked,
              ]}
              onPress={() => setSelectedAchievement(achievement)}
            >
              <Text
                style={[
                  styles.achievementIcon,
                  !achievement.unlocked && styles.achievementIconLocked,
                ]}
              >
                {achievement.unlocked ? achievement.icon : '🔒'}
              </Text>
              <Text
                style={[
                  styles.achievementName,
                  !achievement.unlocked && styles.achievementNameLocked,
                ]}
                numberOfLines={2}
              >
                {achievement.name}
              </Text>
              <View
                style={[
                  styles.achievementXp,
                  !achievement.unlocked && styles.achievementXpLocked,
                ]}
              >
                <Text style={styles.achievementXpText}>+{achievement.xp}</Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* Tips Section */}
      <View style={styles.tipsSection}>
        <Text style={styles.tipsTitle}>💡 Cum să deblochezi mai multe</Text>
        <View style={styles.tipCard}>
          <Text style={styles.tipText}>• Răspunde corect la exerciții consecutive pentru streak-uri</Text>
        </View>
        <View style={styles.tipCard}>
          <Text style={styles.tipText}>• Rezolvă exerciții din toate subiectele</Text>
        </View>
        <View style={styles.tipCard}>
          <Text style={styles.tipText}>• Completează simulări de examen</Text>
        </View>
        <View style={styles.tipCard}>
          <Text style={styles.tipText}>• Studiază dimineața devreme sau noaptea târziu</Text>
        </View>
      </View>

      <View style={{ height: 100 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f7fa',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f7fa',
  },
  loadingText: {
    fontSize: 18,
    color: '#6b7280',
  },
  header: {
    paddingTop: 60,
    paddingBottom: 30,
    paddingHorizontal: 24,
    alignItems: 'center',
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },
  levelBadge: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255,255,255,0.25)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
    borderWidth: 3,
    borderColor: 'rgba(255,255,255,0.5)',
  },
  levelNumber: {
    fontSize: 36,
    fontWeight: '800',
    color: 'white',
  },
  levelName: {
    fontSize: 24,
    fontWeight: '700',
    color: 'white',
    marginBottom: 4,
  },
  xpText: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.9)',
    marginBottom: 16,
  },
  xpBarContainer: {
    width: '100%',
    height: 8,
    backgroundColor: 'rgba(255,255,255,0.3)',
    borderRadius: 4,
    overflow: 'hidden',
  },
  xpBar: {
    height: '100%',
    backgroundColor: 'white',
    borderRadius: 4,
  },
  xpProgress: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
    marginTop: 8,
  },
  streakCard: {
    flexDirection: 'row',
    backgroundColor: 'white',
    marginHorizontal: 20,
    marginTop: -20,
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 5,
  },
  streakItem: {
    flex: 1,
    alignItems: 'center',
  },
  streakDivider: {
    width: 1,
    backgroundColor: '#e5e7eb',
    marginVertical: 4,
  },
  streakEmoji: {
    fontSize: 28,
    marginBottom: 8,
  },
  streakValue: {
    fontSize: 24,
    fontWeight: '800',
    color: '#1f2937',
  },
  streakLabel: {
    fontSize: 11,
    color: '#6b7280',
    marginTop: 4,
    textAlign: 'center',
  },
  achievementsSection: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: '800',
    color: '#1f2937',
    marginBottom: 4,
  },
  sectionSubtitle: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 16,
  },
  achievementsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  achievementCard: {
    width: '30%',
    aspectRatio: 1,
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 12,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  achievementCardLocked: {
    backgroundColor: '#f3f4f6',
    opacity: 0.7,
  },
  achievementIcon: {
    fontSize: 32,
    marginBottom: 8,
  },
  achievementIconLocked: {
    opacity: 0.5,
  },
  achievementName: {
    fontSize: 11,
    fontWeight: '600',
    color: '#1f2937',
    textAlign: 'center',
  },
  achievementNameLocked: {
    color: '#9ca3af',
  },
  achievementXp: {
    position: 'absolute',
    top: 8,
    right: 8,
    backgroundColor: '#fef3c7',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 8,
  },
  achievementXpLocked: {
    backgroundColor: '#e5e7eb',
  },
  achievementXpText: {
    fontSize: 9,
    fontWeight: '700',
    color: '#92400e',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  achievementModal: {
    backgroundColor: 'white',
    borderRadius: 24,
    padding: 32,
    alignItems: 'center',
    width: '80%',
  },
  modalIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  modalName: {
    fontSize: 24,
    fontWeight: '800',
    color: '#1f2937',
    marginBottom: 8,
    textAlign: 'center',
  },
  modalDescription: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    marginBottom: 16,
    lineHeight: 20,
  },
  modalXpBadge: {
    backgroundColor: '#fef3c7',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 12,
    marginBottom: 16,
  },
  modalXpText: {
    fontSize: 16,
    fontWeight: '700',
    color: '#92400e',
  },
  unlockedBadge: {
    backgroundColor: '#d1fae5',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 12,
  },
  unlockedBadgeText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#065f46',
  },
  lockedBadge: {
    backgroundColor: '#f3f4f6',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 12,
  },
  lockedBadgeText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#6b7280',
  },
  tipsSection: {
    padding: 20,
    paddingTop: 0,
  },
  tipsTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1f2937',
    marginBottom: 12,
  },
  tipCard: {
    backgroundColor: 'white',
    padding: 14,
    borderRadius: 12,
    marginBottom: 8,
  },
  tipText: {
    fontSize: 14,
    color: '#4b5563',
    lineHeight: 20,
  },
});
