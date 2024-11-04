import { View, Text, Button, StyleSheet } from 'react-native';

function CameraPermissionRequest({ requestPermission }: any) {
  return (
    <View style={styles.container}>
      <Text style={styles.message}>We need your permission to show the camera</Text>
      <Button onPress={requestPermission} title="Grant Permission" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center' },
  message: { textAlign: 'center', paddingBottom: 10 },
});

export default CameraPermissionRequest;
