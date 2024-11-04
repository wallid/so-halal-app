import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { FontAwesome } from '@expo/vector-icons';

interface HalalStatusHalalProps {}

function HalalStatusHalal({}: HalalStatusHalalProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>This product is Halal.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: 'row', alignItems: 'center' },
  text: { fontSize: 16, fontWeight: 'bold', marginRight: 5 },
});

export default HalalStatusHalal;
