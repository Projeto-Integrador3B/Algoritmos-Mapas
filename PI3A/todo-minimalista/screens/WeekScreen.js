import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  SafeAreaView,
} from 'react-native';
import { useTasks } from '../context/TaskContext';

const DAY_NAMES_PT = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
const MONTH_NAMES_PT = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

function formatDate(dateStr) {
  const [year, month, day] = dateStr.split('-').map(Number);
  const d = new Date(year, month - 1, day);
  return {
    dayName: DAY_NAMES_PT[d.getDay()],
    full: `${day} de ${MONTH_NAMES_PT[month - 1]}`,
  };
}

export default function WeekScreen({ navigation }) {
  const { tasks, toggleTask } = useTasks();

  const grouped = tasks.reduce((acc, task) => {
    if (!acc[task.date]) acc[task.date] = [];
    acc[task.date].push(task);
    return acc;
  }, {});

  const sortedDates = Object.keys(grouped).sort();

  const sections = sortedDates.map((date) => ({
    date,
    tasks: grouped[date],
  }));

  const renderSection = ({ item }) => {
    const { dayName, full } = formatDate(item.date);
    return (
      <View style={styles.dayCard}>
        <Text style={styles.dayName}>{dayName}</Text>
        <Text style={styles.dayFull}>{full}</Text>
        {item.tasks.map((task, idx) => (
          <TouchableOpacity
            key={task.id}
            style={[styles.taskRow, idx > 0 && styles.taskBorder]}
            onPress={() => toggleTask(task.id)}
            activeOpacity={0.7}
          >
            <View style={[styles.checkbox, task.completed && styles.checkboxDone]}>
              {task.completed && <Text style={styles.checkmark}>✓</Text>}
            </View>
            <Text style={[styles.taskTitle, task.completed && styles.taskDone]}>
              {task.title}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.navigate('Home')}>
          <Text style={styles.backIcon}>←</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Esta Semana</Text>
        <View style={{ width: 32 }} />
      </View>

      {sections.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyText}>Nenhuma tarefa cadastrada ainda.</Text>
          <Text style={styles.emptyHint}>Volte e toque em + para adicionar!</Text>
        </View>
      ) : (
        <FlatList
          data={sections}
          keyExtractor={(item) => item.date}
          renderItem={renderSection}
          contentContainerStyle={styles.listPadding}
          showsVerticalScrollIndicator={false}
        />
      )}

      <TouchableOpacity
        style={styles.fab}
        onPress={() => navigation.navigate('AddTask')}
        activeOpacity={0.85}
      >
        <Text style={styles.fabIcon}>+</Text>
      </TouchableOpacity>
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
  listPadding: {
    paddingHorizontal: 16,
    paddingTop: 8,
    paddingBottom: 100,
  },
  dayCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
  },
  dayName: {
    fontSize: 16,
    fontWeight: '700',
    color: '#1A1A2E',
  },
  dayFull: {
    fontSize: 12,
    color: '#9999AA',
    marginBottom: 12,
    marginTop: 2,
  },
  taskRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
  },
  taskBorder: {
    borderTopWidth: 1,
    borderTopColor: '#F0F0F5',
  },
  checkbox: {
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 2,
    borderColor: '#CCCCDD',
    marginRight: 14,
    alignItems: 'center',
    justifyContent: 'center',
  },
  checkboxDone: {
    backgroundColor: '#4338F7',
    borderColor: '#4338F7',
  },
  checkmark: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '700',
  },
  taskTitle: {
    fontSize: 15,
    color: '#1A1A2E',
    fontWeight: '500',
    flex: 1,
  },
  taskDone: {
    color: '#AAAABC',
    textDecorationLine: 'line-through',
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: '#AAAABC',
    fontWeight: '500',
  },
  emptyHint: {
    fontSize: 13,
    color: '#CCCCDD',
    marginTop: 6,
  },
  fab: {
    position: 'absolute',
    bottom: 36,
    right: 24,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#4338F7',
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#4338F7',
    shadowOpacity: 0.4,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 4 },
    elevation: 6,
  },
  fabIcon: {
    color: '#FFFFFF',
    fontSize: 28,
    fontWeight: '300',
    marginTop: -2,
  },
});