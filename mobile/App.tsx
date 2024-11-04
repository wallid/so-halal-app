import React, { useState, useRef } from 'react';
import { View, StyleSheet, Animated } from 'react-native';
import { CameraView, useCameraPermissions, BarcodeScanningResult } from 'expo-camera';
import { fetchProductData, ProductData, HalalStatus } from './apiService';
import CameraPermissionRequest from './components/CameraPermissionRequest';
import ProductInfoModal from './components/ProductInfoModal';
import FlashOverlay from './components/FlashOverlay';
import BarcodeFrameOverlay from './components/BarcodeFrameOverlay';

export default function App() {
  const [permission, requestPermission] = useCameraPermissions();
  const [hasScanned, setHasScanned] = useState(false);
  const [isFetching, setIsFetching] = useState(false);
  const [productData, setProductData] = useState<ProductData | null>(null);
  const [isProductFound, setIsProductFound] = useState(true);
  const [isModalVisible, setIsModalVisible] = useState(false);

  const flashAnim = useRef(new Animated.Value(0)).current;
  const overlayColor = useRef(new Animated.Value(0)).current;

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return <CameraPermissionRequest requestPermission={requestPermission} />;
  }

  const handleBarCodeScanned = async (scannedResult: BarcodeScanningResult) => {
    if (!hasScanned && !isFetching) {
      setHasScanned(true);
      setIsFetching(true);

      const barcode = scannedResult.data;
      try {
        const data = await fetchProductData(barcode);
        if (data) {
          setProductData(data);
          setIsProductFound(true);
          triggerOverlayFlash(data.status);
        } else {
          setProductData(null);
          setIsProductFound(false);
          triggerOverlayFlash(HalalStatus.UNKNOWN);
        }
        setIsModalVisible(true);
      } catch (error) {
        console.error('Error fetching product data:', error);
      } finally {
        setIsFetching(false);
      }
    }
  };

  const triggerOverlayFlash = (status: HalalStatus) => {
    let colorValue;
    switch (status) {
      case HalalStatus.HALAL:
      case HalalStatus.HALAL_GIVEN_INGREDIENTS:
        colorValue = 1; // Green
        break;
      case HalalStatus.NOT_HALAL:
        colorValue = 0; // Red
        break;
      case HalalStatus.NOT_ENOUGH_INFORMATION:
      case HalalStatus.UNKNOWN:
      default:
        colorValue = 2; // Yellow
        break;
    }

    Animated.timing(overlayColor, {
      toValue: colorValue,
      duration: 0,
      useNativeDriver: false,
    }).start();

    Animated.sequence([
      Animated.timing(flashAnim, {
        toValue: 1, // Fully visible
        duration: 300,
        useNativeDriver: false,
      }),
      Animated.delay(300),
      Animated.timing(flashAnim, {
        toValue: 0, // Fade out
        duration: 300,
        useNativeDriver: false,
      }),
    ]).start();
  };

  const closeModal = () => {
    setIsModalVisible(false);
    setHasScanned(false);
  };

  const overlayBackgroundColor = overlayColor.interpolate({
    inputRange: [0, 1, 2],
    outputRange: ['red', 'green', 'yellow'],
  });

  return (
    <View style={styles.container}>
      <CameraView
        style={styles.camera}
        barcodeScannerSettings={{
          barcodeTypes: ['ean13', 'ean8'],
        }}
        onBarcodeScanned={handleBarCodeScanned}>
        <BarcodeFrameOverlay />
      </CameraView>

      <FlashOverlay flashAnim={flashAnim} overlayBackgroundColor={overlayBackgroundColor} />

      {isModalVisible && (
        <ProductInfoModal
          productData={productData}
          isProductFound={isProductFound}
          closeModal={closeModal}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  camera: {
    flex: 1,
  },
});
