import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { ProductData } from '../apiService';
import HalalStatusIcon from './HalalStatusIcon';

interface ProductInformationProps {
  productData: ProductData;
  children: React.ReactNode;
}

function ProductInformation({ productData, children }: ProductInformationProps) {
  const { product_name, brands, ingredients_text, haram_items_found, status } = productData;

  return (
    <View>
      <View style={styles.header}>
        <Text style={styles.title}>{product_name}</Text>
        <HalalStatusIcon status={status} />
      </View>
      <Text style={styles.text}>Brand {brands}</Text>
      {ingredients_text ? (
        <Text style={styles.text}>Ingredients {ingredients_text}</Text>
      ) : (
        <Text style={styles.text}>
          No ingredients information available.
        </Text>
      )}
    {children}
      {haram_items_found && haram_items_found.length > 0 && (
        <View style={styles.haramItemsContainer}>
          <Text style={styles.text}>Haram items found:</Text>
          {haram_items_found.map((item, index) => (
            <Text key={index} style={styles.haramItem}>
              • {item}
            </Text>
          ))}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  text: {
    fontSize: 16,
    marginBottom: 10,
  },
  haramItemsContainer: {
    marginTop: 15,
  },
  haramItem: {
    fontSize: 14,
    marginBottom: 5,
    color: 'red',
  },
});

export default ProductInformation;
