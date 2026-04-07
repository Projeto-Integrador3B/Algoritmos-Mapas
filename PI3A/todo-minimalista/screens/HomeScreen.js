import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  SafeAreaView,
} from 'react-native';
import { useTasks } from '../context/TaskContext';

function getWeekDays() {
  const today = new Date();
  const days = [];
  const dayNames = ['DOM', 'SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB'];

  const monday = new Date(today);
  const day = today.getDay();
  const diff = day === 0 ? -6 : 1 - day;
  monday.setDate(today.getDate() + diff);

  for (let i = 0; i < 7; i++) {
    const d = new Date(monday);
    d.setDate(monday.getDate() + i);
    days.push({
      label: dayNames[d.getDay()],
      number: d.getDate(),
      dateStr: d.toISOString().split('T')[0],
      isToday: d.toISOString().split('T')[0] === today.toISOString().split('T')[0],
    });
  }
  return days;
}

export default function HomeScreen({ navigation }) {
  const { tasks, toggleTask } = useTasks();
  const weekDays = getWeekDays();
  const today = new Date().toISOString().split('T')[0];
  const [selectedDate, setSelectedDate] = useState(today);

  const filteredTasks = tasks.filter((t) => t.date === selectedDate);

  const renderTask = ({ item }) => (
    <TouchableOpacity
      style={styles.taskRow}
      onPress={() => toggleTask(item.id)}
      activeOpacity={0.7}
    >
      <View style={[styles.checkbox, item.completed && styles.checkboxDone]}>
        {item.completed && <Text style={styles.checkmark}>✓</Text>}
      </View>
      <Text style={[styles.taskTitle, item.completed && styles.taskDone]}>
        {item.title}
      </Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.navigate('Week')}>
          <Text style={styles.menuIcon}>☰</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Hoje</Text>
        <View style={styles.avatarPlaceholder}>
          <Text style={styles.avatarIcon}>👤</Text>
        </View>
      </View>

      <View style={styles.calendarCard}>
        {weekDays.map((d) => (
          <TouchableOpacity
            key={d.dateStr}
            style={[styles.dayCol, selectedDate === d.dateStr && styles.dayColActive]}
            onPress={() => setSelectedDate(d.dateStr)}
            activeOpacity={0.8}
          >
            <Text style={[styles.dayLabel, selectedDate === d.dateStr && styles.dayLabelActive]}>
              {d.label}
            </Text>
            <Text style={[styles.dayNumber, selectedDate === d.dateStr && styles.dayNumberActive]}>
              {d.number}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle}>Foco de Hoje</Text>

      {filteredTasks.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyText}>Nenhuma tarefa para este dia.</Text>
          <Text style={styles.emptyHint}>Toque em + para adicionar!</Text>
        </View>
      ) : (
        <FlatList
          data={filteredTasks}
          keyExtractor={(item) => item.id}
          renderItem={renderTask}
          contentContainerStyle={styles.listContainer}
          showsVerticalScrollIndicator={false}
          ItemSeparatorComponent={() => <View style={styles.separator} />}
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
    paddingTop: 48,
    paddingBottom: 12,
  },
  menuIcon: {
    fontSize: 22,
    color: '#1A1A2E',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#1A1A2E',
    letterSpacing: 0.3,
  },
  avatarPlaceholder: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#E4E4EE',
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarIcon: {
    fontSize: 18,
  },
  calendarCard: {
    flexDirection: 'row',
    backgroundColor: '#FFFFFF',
    marginHorizontal: 16,
    borderRadius: 16,
    paddingVertical: 12,
    paddingHorizontal: 8,
    justifyContent: 'space-between',
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
    marginBottom: 24,
  },
  dayCol: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 8,
    borderRadius: 12,
  },
  dayColActive: {
    backgroundColor: '#4338F7',
  },
  dayLabel: {
    fontSize: 10,
    fontWeight: '600',
    color: '#9999AA',
    marginBottom: 6,
    letterSpacing: 0.5,
  },
  dayLabelActive: {
    color: '#FFFFFF',
  },
  dayNumber: {
    fontSize: 15,
    fontWeight: '700',
    color: '#1A1A2E',
  },
  dayNumberActive: {
    color: '#FFFFFF',
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#1A1A2E',
    marginHorizontal: 24,
    marginBottom: 12,
  },
  listContainer: {
    marginHorizontal: 16,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    paddingHorizontal: 16,
    paddingVertical: 8,
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
  },
  taskRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 14,
  },
  separator: {
    height: 1,
    backgroundColor: '#F0F0F5',
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
    alignItems: 'center',
    marginTop: 60,
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