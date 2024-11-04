import React from 'react';
import { View, StyleSheet } from 'react-native';
import { FontAwesome, Entypo } from '@expo/vector-icons';
import { HalalStatus } from '../apiService';

interface HalalStatusIconProps {
  status: HalalStatus;
}

function HalalStatusIcon({ status }: HalalStatusIconProps) {
  let icon;
  let color;

  switch (status) {
    case HalalStatus.HALAL:
    case HalalStatus.HALAL_GIVEN_INGREDIENTS:
      icon = <FontAwesome name="check-circle" size={30} color="green" />;
      color = 'green';
      break;
    case HalalStatus.NOT_HALAL:
      icon = <Entypo name="circle-with-cross" size={30} color="red" />;
      color = 'red';
      break;
    case HalalStatus.NOT_ENOUGH_INFORMATION:
    case HalalStatus.UNKNOWN:
    default:
      icon = <Entypo name="warning" size={30} color="yellow" />;
      color = 'yellow';
      break;
  }

  return <View style={[styles.iconContainer, { borderColor: color }]}>{icon}</View>;
}

const styles = StyleSheet.create({
  iconContainer: {
    padding: 5,
  },
});

export default HalalStatusIcon;
