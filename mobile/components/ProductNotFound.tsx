import React from 'react';
import { View, Text, TouchableOpacity, Button, StyleSheet } from 'react-native';

interface ProductNotFoundProps {
  closeModal: () => void;
}

function ProductNotFound({ closeModal }: ProductNotFoundProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Product Not Found</Text>
      <Text style={styles.text}>
        The scanned product was not found in the database. You can help by taking a few photos of the product to add it to the database.
      </Text>
      <TouchableOpacity
        style={styles.primaryButton}
        onPress={() => alert('Take a series of photos to add the product')}>
        <Text style={styles.primaryButtonText}>Add Product by Taking Photos</Text>
      </TouchableOpacity>
      <Button title="Close" onPress={closeModal} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  text: {
    fontSize: 16,
    marginBottom: 10,
    textAlign: 'center',
  },
  primaryButton: {
    backgroundColor: '#007BFF',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 15,
  },
  primaryButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default ProductNotFound;
