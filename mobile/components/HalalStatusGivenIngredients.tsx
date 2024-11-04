import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { FontAwesome } from '@expo/vector-icons';

function HalalStatusGivenIngredients() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>This product is considered Halal based on its ingredients.</Text>
      <FontAwesome name="check-circle" size={30} color="green" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: 'row', alignItems: 'center' },
  text: { fontSize: 16, fontWeight: 'bold', marginRight: 5 },
});

export default HalalStatusGivenIngredients;
