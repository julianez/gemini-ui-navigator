import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, SafeAreaView, StatusBar } from 'react-native';

const GeminiChallenge = () => {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <View style={styles.header}>
        <Text style={styles.greeting}>Hola Maria José</Text>
        <Text style={styles.balance}>USD: $950</Text>
      </View>
      <View style={styles.content}>
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
    backgroundColor: '#1C1C1C', // Dark Grey background
  },
  header: {
    padding: 20,
    marginTop: 20,
  },
  greeting: {
    color: '#FFFFFF',
    fontSize: 24,
    fontWeight: 'bold',
  },
  balance: {
    color: '#FFFFFF',
    fontSize: 32,
    marginTop: 10,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  primaryButton: {
    backgroundColor: '#E30613', // Scotiabank Red
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 8,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
  },
});

export default GeminiChallenge;
