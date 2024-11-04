import { Animated, StyleSheet } from 'react-native';

function FlashOverlay({ flashAnim, overlayBackgroundColor }: any) {
  return (
    <Animated.View
      style={[
        styles.flashOverlay,
        { backgroundColor: overlayBackgroundColor, opacity: flashAnim },
      ]}
    />
  );
}

const styles = StyleSheet.create({
  flashOverlay: { ...StyleSheet.absoluteFillObject, zIndex: 1, opacity: 0.5 },
});

export default FlashOverlay;
