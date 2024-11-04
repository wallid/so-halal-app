import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { HalalStatus } from '../apiService';

interface HalalReasonsRendererProps {
  status: HalalStatus;
  reasons: string[];
}

function HalalReasonsRenderer({ status, reasons }: HalalReasonsRendererProps) {
  const renderStatusText = () => {
    switch (status) {
      case HalalStatus.HALAL:
        return 'This product is Halal.';
      case HalalStatus.NOT_HALAL:
        return 'This product is not Halal for the following reasons:';
      case HalalStatus.HALAL_GIVEN_INGREDIENTS:
        return 'This product is Halal based on its ingredients.';
      case HalalStatus.NOT_ENOUGH_INFORMATION:
        return 'Not enough information to verify if this product is Halal.';
      case HalalStatus.UNKNOWN:
      default:
        return 'The Halal status of this product is unknown.';
    }
  };

  return (
    <View style={styles.halalInfoContainer}>
      <Text style={styles.halalText}>{renderStatusText()}</Text>
      <View style={styles.halalReasons}>
        {reasons.map((reason, index) => (
          <Text key={index} style={styles.halalReason}>
            • {reason}
          </Text>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  halalInfoContainer: { marginTop: 20 },
  halalText: { fontSize: 16, fontWeight: 'bold', marginBottom: 5 },
  halalReasons: { marginLeft: 10 },
  halalReason: { fontSize: 14, marginBottom: 5 },
});

export default HalalReasonsRenderer;
