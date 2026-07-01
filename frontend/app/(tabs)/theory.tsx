import { useState } from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, Modal } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { DUO } from '@/constants/duo';
import { TOPICS, type Topic } from '@/constants/theoryTopics';

const SUBJECT_COLORS: Record<number, string> = {
  1: DUO.blue,
  2: DUO.green,
  3: DUO.yellow,
};

export default function TheoryScreen() {
  const [selectedSubject, setSelectedSubject] = useState<number | null>(null);
  const [selectedTopic, setSelectedTopic] = useState<Topic | null>(null);

  const filteredTopics = selectedSubject
    ? TOPICS.filter(t => t.subject === selectedSubject)
    : TOPICS;

  return (
    <ScrollView style={styles.container}>
      {/* Topic Detail Modal */}
      <Modal
        visible={selectedTopic !== null}
        animationType="slide"
        transparent={true}
        onRequestClose={() => setSelectedTopic(null)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <ScrollView showsVerticalScrollIndicator={false}>
              {selectedTopic && (
                <>
                  {/* Header */}
                  <View style={styles.modalHeader}>
                    <Text style={styles.modalIcon}>{selectedTopic.icon}</Text>
                    <Text style={styles.modalTitle}>{selectedTopic.name}</Text>
                    <TouchableOpacity
                      style={styles.closeButton}
                      onPress={() => setSelectedTopic(null)}
                    >
                      <Text style={styles.closeButtonText}>x</Text>
                    </TouchableOpacity>
                  </View>

                  {/* Theory */}
                  <View style={styles.theoryBox}>
                    <Text style={styles.sectionLabel}>TEORIE</Text>
                    <Text style={styles.theoryText}>{selectedTopic.theory}</Text>
                  </View>

                  {/* Formulas */}
                  <View style={styles.formulasBox}>
                    <Text style={styles.sectionLabel}>FORMULE</Text>
                    {selectedTopic.formulas.map((formula, index) => (
                      <View key={index} style={[
                        styles.formulaItem,
                        formula.startsWith('---') && styles.formulaHeader
                      ]}>
                        <Text style={[
                          styles.formulaText,
                          formula.startsWith('---') && styles.formulaHeaderText
                        ]}>
                          {formula.replace(/---/g, '').trim()}
                        </Text>
                      </View>
                    ))}
                  </View>

                  {/* Tips */}
                  <View style={styles.tipsBox}>
                    <Text style={styles.sectionLabel}>TIPS & TRUCURI</Text>
                    {selectedTopic.tips.map((tip, index) => (
                      <View key={index} style={styles.tipItem}>
                        <Text style={styles.tipBullet}>•</Text>
                        <Text style={styles.tipText}>{tip}</Text>
                      </View>
                    ))}
                  </View>
                </>
              )}
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* Header */}
      <LinearGradient
        colors={[DUO.purple + '30', DUO.bg]}
        style={styles.header}
      >
        <Text style={styles.headerTitle}>Teorie & Formule</Text>
        <Text style={styles.headerSubtitle}>Tot ce trebuie sa stii pentru BAC</Text>
      </LinearGradient>

      {/* Subject Filter */}
      <View style={styles.filterContainer}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          {[
            { label: 'Toate', val: null },
            { label: 'Subiectul 1', val: 1 },
            { label: 'Subiectul 2', val: 2 },
            { label: 'Subiectul 3', val: 3 },
          ].map(f => (
            <TouchableOpacity
              key={f.label}
              style={[styles.filterChip, selectedSubject === f.val && styles.filterChipActive]}
              onPress={() => setSelectedSubject(f.val)}
            >
              <Text style={[styles.filterChipText, selectedSubject === f.val && styles.filterChipTextActive]}>
                {f.label}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* Topics Grid */}
      <View style={styles.topicsContainer}>
        {filteredTopics.map((topic) => {
          const color = SUBJECT_COLORS[topic.subject] || DUO.blue;
          return (
            <TouchableOpacity
              key={topic.id}
              style={styles.topicCard}
              onPress={() => setSelectedTopic(topic)}
            >
              <View style={[styles.topicIconContainer, { backgroundColor: color + '20' }]}>
                <Text style={styles.topicIcon}>{topic.icon}</Text>
              </View>
              <Text style={styles.topicName}>{topic.name}</Text>
              <Text style={[styles.topicSubject, { color }]}>Subiectul {topic.subject}</Text>
              <View style={[styles.topicMeta, { backgroundColor: color + '15' }]}>
                <Text style={[styles.topicMetaText, { color }]}>
                  {topic.formulas.filter(f => !f.startsWith('---')).length} formule
                </Text>
              </View>
            </TouchableOpacity>
          );
        })}
      </View>

      {/* Quick Reference Card */}
      <View style={styles.quickRefCard}>
        <Text style={styles.quickRefTitle}>Formule de Memorat</Text>
        {[
          { label: 'Derivate:', formula: "(xⁿ)' = n·xⁿ⁻¹   |   (eˣ)' = eˣ   |   (ln x)' = 1/x" },
          { label: 'Integrale:', formula: '∫xⁿdx = xⁿ⁺¹/(n+1)   |   ∫eˣdx = eˣ   |   ∫1/x dx = ln|x|' },
          { label: 'Trigonometrie:', formula: 'sin²x + cos²x = 1   |   tg x = sin x/cos x' },
          { label: 'Determinant 2x2:', formula: 'det = ad - bc (diagonala principala - secundara)' },
          { label: 'Arie triunghi:', formula: 'A = bh/2   |   A = √[p(p-a)(p-b)(p-c)]' },
        ].map(s => (
          <View key={s.label} style={styles.quickRefSection}>
            <Text style={styles.quickRefLabel}>{s.label}</Text>
            <Text style={styles.quickRefFormula}>{s.formula}</Text>
          </View>
        ))}
      </View>

      <View style={{ height: 100 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: DUO.bg,
  },
  header: {
    paddingTop: 60,
    paddingBottom: 24,
    paddingHorizontal: 24,
    borderBottomWidth: 1,
    borderBottomColor: DUO.surface,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: DUO.textPrimary,
    marginBottom: 6,
  },
  headerSubtitle: {
    fontSize: 14,
    color: DUO.textSecondary,
    fontWeight: '600',
  },
  filterContainer: {
    paddingVertical: 16,
    paddingHorizontal: 20,
  },
  filterChip: {
    backgroundColor: DUO.card,
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: DUO.radiusFull,
    marginRight: 8,
    borderWidth: 1,
    borderColor: DUO.surface,
  },
  filterChipActive: {
    backgroundColor: DUO.purple + '20',
    borderColor: DUO.purple + '40',
  },
  filterChipText: {
    fontSize: 14,
    color: DUO.textMuted,
    fontWeight: '600',
  },
  filterChipTextActive: {
    color: DUO.purple,
  },
  topicsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: 16,
    gap: 12,
  },
  topicCard: {
    width: '47%',
    backgroundColor: DUO.card,
    borderRadius: DUO.radius,
    padding: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: DUO.surface,
  },
  topicIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  topicIcon: {
    fontSize: 28,
  },
  topicName: {
    fontSize: 14,
    fontWeight: '700',
    color: DUO.textPrimary,
    textAlign: 'center',
    marginBottom: 4,
  },
  topicSubject: {
    fontSize: 11,
    fontWeight: '600',
    marginBottom: 8,
  },
  topicMeta: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  topicMetaText: {
    fontSize: 10,
    fontWeight: '700',
  },
  quickRefCard: {
    backgroundColor: DUO.card,
    margin: 20,
    borderRadius: DUO.radiusLg,
    padding: 20,
    borderWidth: 1,
    borderColor: DUO.purple + '30',
  },
  quickRefTitle: {
    fontSize: 18,
    fontWeight: '800',
    color: DUO.textPrimary,
    marginBottom: 16,
  },
  quickRefSection: {
    marginBottom: 12,
  },
  quickRefLabel: {
    fontSize: 12,
    color: DUO.textMuted,
    marginBottom: 4,
    fontWeight: '600',
  },
  quickRefFormula: {
    fontSize: 13,
    color: DUO.yellow,
    fontWeight: '600',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.7)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: DUO.card,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    maxHeight: '90%',
    padding: 24,
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  modalIcon: {
    fontSize: 32,
    marginRight: 12,
  },
  modalTitle: {
    flex: 1,
    fontSize: 22,
    fontWeight: '800',
    color: DUO.textPrimary,
  },
  closeButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: DUO.surface,
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeButtonText: {
    fontSize: 20,
    color: DUO.textMuted,
    fontWeight: '700',
  },
  sectionLabel: {
    fontSize: 12,
    fontWeight: '800',
    color: DUO.textMuted,
    marginBottom: 12,
    letterSpacing: 1,
  },
  theoryBox: {
    backgroundColor: DUO.green + '10',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: DUO.green + '20',
  },
  theoryText: {
    fontSize: 15,
    color: DUO.green,
    lineHeight: 22,
    fontWeight: '600',
  },
  formulasBox: {
    backgroundColor: DUO.blue + '10',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: DUO.blue + '20',
  },
  formulaItem: {
    backgroundColor: DUO.surface,
    padding: 10,
    borderRadius: 8,
    marginBottom: 6,
  },
  formulaHeader: {
    backgroundColor: DUO.blue + '20',
    marginTop: 8,
  },
  formulaText: {
    fontSize: 14,
    color: DUO.cyan,
  },
  formulaHeaderText: {
    fontWeight: '700',
    color: DUO.blue,
    textAlign: 'center',
  },
  tipsBox: {
    backgroundColor: DUO.yellow + '10',
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: DUO.yellow + '20',
  },
  tipItem: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  tipBullet: {
    fontSize: 14,
    color: DUO.yellow,
    marginRight: 8,
  },
  tipText: {
    flex: 1,
    fontSize: 14,
    color: DUO.orange,
    lineHeight: 20,
    fontWeight: '600',
  },
});
