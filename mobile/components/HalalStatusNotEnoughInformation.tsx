import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

function HalalStatusNotEnoughInformation() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Not enough information to determine if this product is Halal.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginBottom: 10 },
  text: { fontSize: 16, fontWeight: 'bold' },
});

export default HalalStatusNotEnoughInformation;
