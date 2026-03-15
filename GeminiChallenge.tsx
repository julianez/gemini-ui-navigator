import React from 'react';
import { SafeAreaView, StyleSheet, Text, TouchableOpacity, View, StatusBar } from 'react-native';

const GeminiChallenge = () => {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <View style={styles.header}>
        <Text style={styles.greeting}>Hola Maria José</Text>
        <Text style={styles.balanceLabel}>Tu saldo</Text>
        <Text style={styles.balanceValue}>USD: $950</Text>
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.primaryButton}>
          <Text style={styles.buttonText}>Transferir ahora</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1E1E1E', // Dark Grey background
    padding: 20,
  },
  header: {
    marginTop: 50,
  },
  greeting: {
    color: '#FFFFFF',
    fontSize: 24,
    fontWeight: 'bold',
  },
  balanceLabel: {
    color: '#A0A0A0',
    fontSize: 16,
    marginTop: 10,
  },
  balanceValue: {
    color: '#FFFFFF',
    fontSize: 32,
    fontWeight: 'bold',
    marginVertical: 10,
  },
  buttonContainer: {
    marginTop: 40,
  },
  primaryButton: {
    backgroundColor: '#E60000', // Scotiabank Red
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
  },
});

export default GeminiChallenge;