import { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
  Modal
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';
import { API_BASE_URL } from '@/constants/api';

interface KnowledgeTopic {
  id: string;
  name: string;
  keywords?: string[];
}

export default function AdminScreen() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [topics, setTopics] = useState<KnowledgeTopic[]>([]);
  const [loading, setLoading] = useState(false);

  // Form pentru topic nou
  const [topicId, setTopicId] = useState('');
  const [keywords, setKeywords] = useState('');
  const [response, setResponse] = useState('');

  // Modal pentru editare
  const [showAddModal, setShowAddModal] = useState(false);

  // Doar gard de UI; endpoint-urile de knowledge din backend nu sunt autentificate
  const ADMIN_PASSWORD = 'bac2025admin';

  const handleLogin = () => {
    if (password === ADMIN_PASSWORD) {
      setIsAuthenticated(true);
      fetchTopics();
    } else {
      Alert.alert('Eroare', 'Parolă greșită!');
    }
  };

  const fetchTopics = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/chat/knowledge`);
      const data = await res.json();
      setTopics(data.topics ?? []);
    } catch (error) {
      console.log('Error fetching topics:', error);
    }
  };

  const addKnowledge = async () => {
    if (!topicId.trim() || !keywords.trim() || !response.trim()) {
      Alert.alert('Eroare', 'Completează toate câmpurile!');
      return;
    }

    setLoading(true);
    try {
      const keywordsArray = keywords.split(',').map(k => k.trim().toLowerCase());

      const res = await fetch(`${API_BASE_URL}/api/chat/add-knowledge`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: topicId.trim().toLowerCase().replace(/\s+/g, '_'),
          keywords: keywordsArray,
          response: response.trim()
        })
      });

      const data = await res.json();

      if (data.success) {
        Alert.alert('Succes!', `Topic "${topicId}" adăugat!`);
        setTopicId('');
        setKeywords('');
        setResponse('');
        setShowAddModal(false);
        fetchTopics();
      } else {
        Alert.alert('Eroare', data.message || 'Nu s-a putut adăuga');
      }
    } catch (error) {
      Alert.alert('Eroare', 'Eroare de conexiune');
    }
    setLoading(false);
  };

  // Ecran de login
  if (!isAuthenticated) {
    return (
      <View style={styles.loginContainer}>
        <LinearGradient
          colors={['#1f2937', '#111827']}
          style={styles.loginGradient}
        >
          <Text style={styles.loginTitle}>Admin Panel</Text>
          <Text style={styles.loginSubtitle}>Accesează baza de cunoștințe</Text>

          <TextInput
            style={styles.passwordInput}
            value={password}
            onChangeText={setPassword}
            placeholder="Introdu parola..."
            placeholderTextColor="#6b7280"
            secureTextEntry
            onSubmitEditing={handleLogin}
          />

          <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
            <Text style={styles.loginButtonText}>Autentificare</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.backLink}
            onPress={() => router.back()}
          >
            <Text style={styles.backLinkText}>← Înapoi la aplicație</Text>
          </TouchableOpacity>
        </LinearGradient>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Modal pentru adăugare */}
      <Modal visible={showAddModal} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <ScrollView>
              <Text style={styles.modalTitle}>Adaugă Răspuns Nou</Text>

              <Text style={styles.inputLabel}>ID Topic (ex: logaritmi)</Text>
              <TextInput
                style={styles.input}
                value={topicId}
                onChangeText={setTopicId}
                placeholder="nume_topic"
                placeholderTextColor="#9ca3af"
              />

              <Text style={styles.inputLabel}>
                Cuvinte cheie (separate prin virgulă)
              </Text>
              <TextInput
                style={styles.input}
                value={keywords}
                onChangeText={setKeywords}
                placeholder="logaritm, log, ln, baza"
                placeholderTextColor="#9ca3af"
              />

              <Text style={styles.inputLabel}>Răspuns</Text>
              <TextInput
                style={[styles.input, styles.textArea]}
                value={response}
                onChangeText={setResponse}
                placeholder="Scrie răspunsul detaliat aici...

Poți folosi:
• Liste cu bullet points
• **text bold**
• Formule matematice"
                placeholderTextColor="#9ca3af"
                multiline
                numberOfLines={10}
              />

              <View style={styles.modalButtons}>
                <TouchableOpacity
                  style={styles.cancelButton}
                  onPress={() => setShowAddModal(false)}
                >
                  <Text style={styles.cancelButtonText}>Anulează</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={styles.saveButton}
                  onPress={addKnowledge}
                  disabled={loading}
                >
                  <Text style={styles.saveButtonText}>
                    {loading ? 'Se salvează...' : 'Salvează'}
                  </Text>
                </TouchableOpacity>
              </View>
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* Header */}
      <LinearGradient
        colors={['#1f2937', '#374151']}
        style={styles.header}
      >
        <View style={styles.headerRow}>
          <TouchableOpacity onPress={() => router.back()}>
            <Text style={styles.backButton}>←</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Admin - Baza de Cunoștințe</Text>
        </View>
        <Text style={styles.headerSubtitle}>
          {topics.length} topicuri în baza de date
        </Text>
      </LinearGradient>

      {/* Add Button */}
      <TouchableOpacity
        style={styles.addButton}
        onPress={() => setShowAddModal(true)}
      >
        <LinearGradient
          colors={['#10b981', '#059669']}
          style={styles.addButtonGradient}
        >
          <Text style={styles.addButtonText}>+ Adaugă Răspuns Nou</Text>
        </LinearGradient>
      </TouchableOpacity>

      {/* Lista topicuri existente */}
      <ScrollView style={styles.topicsList}>
        <Text style={styles.sectionTitle}>Topicuri Existente:</Text>

        {topics.map((topic, index) => (
          <View key={index} style={styles.topicCard}>
            <Text style={styles.topicId}>{topic.name}</Text>
            <Text style={styles.topicKeywords}>
              Cuvinte cheie: {(topic.keywords ?? []).join(', ')}
            </Text>
          </View>
        ))}
      </ScrollView>

      {/* Instrucțiuni */}
      <View style={styles.instructions}>
        <Text style={styles.instructionsTitle}>Cum funcționează:</Text>
        <Text style={styles.instructionsText}>
          1. Adaugă un topic cu cuvinte cheie{'\n'}
          2. Când utilizatorul scrie o întrebare cu acele cuvinte{'\n'}
          3. Bot-ul va răspunde cu textul tău
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#111827',
  },
  loginContainer: {
    flex: 1,
  },
  loginGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  loginTitle: {
    fontSize: 32,
    fontWeight: '800',
    color: 'white',
    marginBottom: 8,
  },
  loginSubtitle: {
    fontSize: 16,
    color: '#9ca3af',
    marginBottom: 40,
  },
  passwordInput: {
    width: '100%',
    maxWidth: 300,
    backgroundColor: '#374151',
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    color: 'white',
    marginBottom: 16,
    textAlign: 'center',
  },
  loginButton: {
    backgroundColor: '#10b981',
    paddingHorizontal: 40,
    paddingVertical: 14,
    borderRadius: 12,
  },
  loginButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '700',
  },
  backLink: {
    marginTop: 30,
  },
  backLinkText: {
    color: '#6b7280',
    fontSize: 14,
  },
  header: {
    paddingTop: 60,
    paddingBottom: 20,
    paddingHorizontal: 20,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  backButton: {
    fontSize: 24,
    color: 'white',
    marginRight: 16,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: 'white',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#9ca3af',
    marginLeft: 40,
  },
  addButton: {
    margin: 16,
    borderRadius: 12,
    overflow: 'hidden',
  },
  addButtonGradient: {
    padding: 16,
    alignItems: 'center',
  },
  addButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '700',
  },
  topicsList: {
    flex: 1,
    padding: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#9ca3af',
    marginBottom: 12,
  },
  topicCard: {
    backgroundColor: '#1f2937',
    padding: 16,
    borderRadius: 12,
    marginBottom: 8,
    borderLeftWidth: 3,
    borderLeftColor: '#10b981',
  },
  topicId: {
    fontSize: 16,
    fontWeight: '700',
    color: 'white',
    marginBottom: 4,
  },
  topicKeywords: {
    fontSize: 12,
    color: '#6b7280',
  },
  instructions: {
    backgroundColor: '#1f2937',
    padding: 16,
    margin: 16,
    borderRadius: 12,
  },
  instructionsTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#fbbf24',
    marginBottom: 8,
  },
  instructionsText: {
    fontSize: 13,
    color: '#9ca3af',
    lineHeight: 20,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.8)',
    justifyContent: 'center',
    padding: 20,
  },
  modalContent: {
    backgroundColor: '#1f2937',
    borderRadius: 16,
    padding: 20,
    maxHeight: '90%',
  },
  modalTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: 'white',
    marginBottom: 20,
    textAlign: 'center',
  },
  inputLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#9ca3af',
    marginBottom: 8,
    marginTop: 12,
  },
  input: {
    backgroundColor: '#374151',
    borderRadius: 10,
    padding: 14,
    fontSize: 15,
    color: 'white',
  },
  textArea: {
    minHeight: 200,
    textAlignVertical: 'top',
  },
  modalButtons: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 24,
  },
  cancelButton: {
    flex: 1,
    backgroundColor: '#374151',
    padding: 14,
    borderRadius: 10,
    alignItems: 'center',
  },
  cancelButtonText: {
    color: '#9ca3af',
    fontSize: 15,
    fontWeight: '600',
  },
  saveButton: {
    flex: 1,
    backgroundColor: '#10b981',
    padding: 14,
    borderRadius: 10,
    alignItems: 'center',
  },
  saveButtonText: {
    color: 'white',
    fontSize: 15,
    fontWeight: '700',
  },
});
