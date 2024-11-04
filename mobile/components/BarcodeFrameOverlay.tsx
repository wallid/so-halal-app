import { View, StyleSheet } from 'react-native';

function BarcodeFrameOverlay() {
  return (
    <View style={styles.overlayContainer}>
      <View style={styles.frameContainer}>
        <View style={styles.barcodeFrame} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  overlayContainer: { ...StyleSheet.absoluteFillObject, justifyContent: 'space-between' },
  frameContainer: { flex: 2, justifyContent: 'center', alignItems: 'center' },
  barcodeFrame: {
    width: '80%',
    height: 200,
    borderWidth: 4,
    borderColor: 'white',
    borderRadius: 8,
  },
});

export default BarcodeFrameOverlay;
