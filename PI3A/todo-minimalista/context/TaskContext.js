import React, { createContext, useContext, useState } from 'react';

const TaskContext = createContext();

export function TaskProvider({ children }) {
  const [tasks, setTasks] = useState([
    {
      id: '1',
      title: 'Revisar relatório trimestral',
      date: new Date().toISOString().split('T')[0],
      completed: false,
    },
    {
      id: '2',
      title: 'Reunião com equipe de design',
      date: new Date().toISOString().split('T')[0],
      completed: true,
    },
    {
      id: '3',
      title: 'Atualizar apresentação do cliente',
      date: new Date().toISOString().split('T')[0],
      completed: false,
    },
    {
      id: '4',
      title: 'Responder e-mails importantes',
      date: new Date().toISOString().split('T')[0],
      completed: false,
    },
  ]);

  const addTask = (task) => {
    const newTask = {
      id: Date.now().toString(),
      ...task,
      completed: false,
    };
    setTasks((prev) => [...prev, newTask]);
  };

  const toggleTask = (id) => {
    setTasks((prev) =>
      prev.map((t) => (t.id === id ? { ...t, completed: !t.completed } : t))
    );
  };

  return (
    <TaskContext.Provider value={{ tasks, addTask, toggleTask }}>
      {children}
    </TaskContext.Provider>
  );
}

export function useTasks() {
  return useContext(TaskContext);
}