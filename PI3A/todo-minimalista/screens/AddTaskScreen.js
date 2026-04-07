import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  Alert,
  ScrollView,
  Platform,
} from 'react-native';
import { useTasks } from '../context/TaskContext';

function getTodayStr() {
  return new Date().toISOString().split('T')[0];
}

function isValidDate(str) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(str)) return false;
  const d = new Date(str);
  return !isNaN(d.getTime());
}

export default function AddTaskScreen({ navigation }) {
  const { addTask } = useTasks();

  const [title, setTitle] = useState('');
  const [date, setDate] = useState(getTodayStr());
  const [titleError, setTitleError] = useState('');
  const [dateError, setDateError] = useState('');

  const validate = () => {
    let valid = true;

    if (!title.trim()) {
      setTitleError('O título da tarefa não pode estar vazio.');
      valid = false;
    } else {
      setTitleError('');
    }

    if (!date.trim()) {
      setDateError('A data é obrigatória.');
      valid = false;
    } else if (!isValidDate(date.trim())) {
      setDateError('Use o formato AAAA-MM-DD (ex: 2025-06-20).');
      valid = false;
    } else {
      setDateError('');
    }

    return valid;
  };

  const handleSave = () => {
    if (!validate()) return;

    addTask({
      title: title.trim(),
      date: date.trim(),
    });

    Alert.alert('Tarefa adicionada!', `"${title.trim()}" foi salva com sucesso.`, [
      {
        text: 'OK',
        onPress: () => navigation.goBack(),
      },
    ]);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.backIcon}>←</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Nova Tarefa</Text>
        <View style={{ width: 32 }} />
      </View>

      <ScrollView
        contentContainerStyle={styles.formContainer}
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.label}>Título da Tarefa *</Text>
        <TextInput
          style={[styles.input, titleError ? styles.inputError : null]}
          placeholder="Ex: Revisar relatório"
          placeholderTextColor="#AAAABC"
          value={title}
          onChangeText={(text) => {
            setTitle(text);
            if (titleError) setTitleError('');
          }}
          maxLength={100}
          returnKeyType="next"
        />
        {titleError ? <Text style={styles.errorText}>{titleError}</Text> : null}

        <Text style={[styles.label, { marginTop: 24 }]}>Data (AAAA-MM-DD) *</Text>
        <TextInput
          style={[styles.input, dateError ? styles.inputError : null]}
          placeholder="Ex: 2025-06-20"
          placeholderTextColor="#AAAABC"
          value={date}
          onChangeText={(text) => {
            setDate(text);
            if (dateError) setDateError('');
          }}
          keyboardType={Platform.OS === 'ios' ? 'numbers-and-punctuation' : 'default'}
          maxLength={10}
          returnKeyType="done"
        />
        {dateError ? <Text style={styles.errorText}>{dateError}</Text> : null}

        <Text style={styles.hint}>
          * Campos obrigatórios. A tarefa aparecerá no dia selecionado.
        </Text>

        <TouchableOpacity style={styles.saveButton} onPress={handleSave} activeOpacity={0.85}>
          <Text style={styles.saveButtonText}>Salvar Tarefa</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.cancelButton}
          onPress={() => navigation.goBack()}
          activeOpacity={0.7}
        >
          <Text style={styles.cancelButtonText}>Cancelar</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F3F7',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 24,
    paddingTop: 16,
    paddingBottom: 12,
  },
  backIcon: {
    fontSize: 22,
    color: '#1A1A2E',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#1A1A2E',
    letterSpacing: 0.3,
  },
  formContainer: {
    paddingHorizontal: 24,
    paddingTop: 16,
    paddingBottom: 60,
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
    color: '#555566',
    marginBottom: 8,
    letterSpacing: 0.4,
    textTransform: 'uppercase',
  },
  input: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 15,
    color: '#1A1A2E',
    borderWidth: 1.5,
    borderColor: '#E4E4EE',
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 4,
    shadowOffset: { width: 0, height: 1 },
    elevation: 1,
  },
  inputError: {
    borderColor: '#E53E3E',
  },
  errorText: {
    fontSize: 12,
    color: '#E53E3E',
    marginTop: 6,
    marginLeft: 4,
    fontWeight: '500',
  },
  hint: {
    fontSize: 12,
    color: '#AAAABC',
    marginTop: 20,
    lineHeight: 18,
  },
  saveButton: {
    backgroundColor: '#4338F7',
    borderRadius: 14,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 32,
    shadowColor: '#4338F7',
    shadowOpacity: 0.35,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 4 },
    elevation: 5,
  },
  saveButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
    letterSpacing: 0.3,
  },
  cancelButton: {
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 12,
  },
  cancelButtonText: {
    color: '#9999AA',
    fontSize: 15,
    fontWeight: '600',
  },
});