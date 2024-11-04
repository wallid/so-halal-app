import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

function HalalStatusUnknown() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>The Halal status of this product is unknown.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginBottom: 10 },
  text: { fontSize: 16, fontWeight: 'bold' },
});

export default HalalStatusUnknown;
