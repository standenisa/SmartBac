import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';

interface ProgressStats {
  total: number;
  correct: number;
  accuracy: number;
}

export default function ProgressScreen() {
  const [stats, setStats] = useState<ProgressStats | null>(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/stats')
      .then(res => res.json())
      .then(data => {
        setStats({
          total: data.total_attempts || 0,
          correct: data.correct_answers || 0,
          accuracy: Math.round(data.accuracy) || 0
        });
      })
      .catch(err => console.log('Error:', err));
  }, []);

  if (!stats) {
    return (
      <View style={styles.container}>
        <Text style={styles.loading}>Se încarcă...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>📊 Progresul tău</Text>
      </View>

      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{stats.total}</Text>
          <Text style={styles.statLabel}>Exerciții rezolvate</Text>
        </View>

        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{stats.accuracy}%</Text>
          <Text style={styles.statLabel}>Acuratețe</Text>
        </View>

        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{stats.correct}</Text>
          <Text style={styles.statLabel}>Răspunsuri corecte</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loading: {
    fontSize: 18,
    textAlign: 'center',
    marginTop: 100,
    color: '#666',
  },
  header: {
    backgroundColor: '#2563eb',
    padding: 40,
    paddingTop: 60,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
  },
  statsContainer: {
    padding: 20,
    gap: 16,
  },
  statCard: {
    backgroundColor: 'white',
    padding: 24,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statNumber: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#2563eb',
    marginBottom: 8,
  },
  statLabel: {
    fontSize: 16,
    color: '#666',
    fontWeight: '600',
  },
});