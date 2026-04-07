import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  ScrollView,
} from 'react-native';

export default function LoginScreen({ navigation }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [nameError, setNameError] = useState('');
  const [emailError, setEmailError] = useState('');

  const isValidEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

  const validate = () => {
    let valid = true;

    if (!name.trim()) {
      setNameError('O nome não pode estar vazio.');
      valid = false;
    } else {
      setNameError('');
    }

    if (!email.trim()) {
      setEmailError('O e-mail não pode estar vazio.');
      valid = false;
    } else if (!isValidEmail(email.trim())) {
      setEmailError('Digite um e-mail válido.');
      valid = false;
    } else {
      setEmailError('');
    }

    return valid;
  };

  const handleLogin = () => {
    if (!validate()) return;
    navigation.replace('Home');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.inner}
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={false}
      >
        {/* Avatar */}
        <View style={styles.avatarCircle}>
          <Text style={styles.avatarIcon}>👤</Text>
        </View>

        <Text style={styles.title}>Bem-vindo</Text>
        <Text style={styles.subtitle}>Entre com seus dados para continuar</Text>

        {/* Nome */}
        <Text style={styles.label}>Nome *</Text>
        <TextInput
          style={[styles.input, nameError ? styles.inputError : null]}
          placeholder="Ex: João Silva"
          placeholderTextColor="#AAAABC"
          value={name}
          onChangeText={(text) => {
            setName(text);
            if (nameError) setNameError('');
          }}
          maxLength={60}
          returnKeyType="next"
        />
        {nameError ? <Text style={styles.errorText}>{nameError}</Text> : null}

        {/* Email */}
        <Text style={[styles.label, { marginTop: 20 }]}>E-mail *</Text>
        <TextInput
          style={[styles.input, emailError ? styles.inputError : null]}
          placeholder="Ex: joao@email.com"
          placeholderTextColor="#AAAABC"
          value={email}
          onChangeText={(text) => {
            setEmail(text);
            if (emailError) setEmailError('');
          }}
          keyboardType="email-address"
          autoCapitalize="none"
          maxLength={100}
          returnKeyType="done"
        />
        {emailError ? <Text style={styles.errorText}>{emailError}</Text> : null}

        {/* Botão */}
        <TouchableOpacity style={styles.loginButton} onPress={handleLogin} activeOpacity={0.85}>
          <Text style={styles.loginButtonText}>Entrar</Text>
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
  inner: {
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 60,
  },
  avatarCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#FFFFFF',
    alignItems: 'center',
    justifyContent: 'center',
    alignSelf: 'center',
    marginBottom: 24,
    shadowColor: '#000',
    shadowOpacity: 0.07,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 4 },
    elevation: 3,
  },
  avatarIcon: {
    fontSize: 36,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: '#1A1A2E',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#9999AA',
    textAlign: 'center',
    marginBottom: 40,
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
  loginButton: {
    backgroundColor: '#4338F7',
    borderRadius: 14,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 36,
    shadowColor: '#4338F7',
    shadowOpacity: 0.35,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 4 },
    elevation: 5,
  },
  loginButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
    letterSpacing: 0.3,
  },
});