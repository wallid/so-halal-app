import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Entypo } from '@expo/vector-icons';

interface HalalStatusNotHalalProps {
  reasons: string[];
}

function HalalStatusNotHalal({ reasons }: HalalStatusNotHalalProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>This product is not Halal for the following reasons</Text>
      <View style={styles.reasons}>
        {reasons.map((reason, index) => (
          <Text key={index} style={styles.reason}>
            • {reason}
          </Text>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginBottom: 10 },
  text: { fontSize: 16, fontWeight: 'bold', marginBottom: 5, color: 'red' },
  reasons: { marginLeft: 10 },
  reason: { fontSize: 14, color: 'red' },
});

export default HalalStatusNotHalal;
