import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, StatusBar } from 'react-native';

const GeminiChallenge = () => {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <View style={styles.header}>
        <Text style={styles.greeting}>Hola Maria José</Text>
        <Text style={styles.balance}>USD: $950</Text>
      </View>
      <View style={styles.actions}>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>Transferir ahora</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1C1C1E', // Dark Grey background
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    marginBottom: 40,
    alignItems: 'center',
  },
  greeting: {
    color: '#FFFFFF',
    fontSize: 24,
    fontWeight: 'bold',
  },
  balance: {
    color: '#FFFFFF',
    fontSize: 32,
    fontWeight: 'bold',
    marginTop: 10,
  },
  actions: {
    width: '80%',
  },
  button: {
    backgroundColor: '#FF0000', // Scotiabank Red
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default GeminiChallenge;