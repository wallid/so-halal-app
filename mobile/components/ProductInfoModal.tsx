import React from 'react';
import { Modal, TouchableOpacity, StyleSheet, View, Button } from 'react-native';
import { ProductData, HalalStatus } from '../apiService';
import ProductInformation from './ProductInformation';
import ProductNotFound from './ProductNotFound';
import HalalStatusHalal from './HalalStatusHalal';
import HalalStatusNotHalal from './HalalStatusNotHalal';
import HalalStatusGivenIngredients from './HalalStatusGivenIngredients';
import HalalStatusNotEnoughInformation from './HalalStatusNotEnoughInformation';
import HalalStatusUnknown from './HalalStatusUnknown';

interface ProductInfoModalProps {
  productData: ProductData | null;
  isProductFound: boolean;
  closeModal: () => void;
}

function ProductInfoModal({ productData, isProductFound, closeModal }: ProductInfoModalProps) {
  const renderHalalStatus = (status: HalalStatus, reasons: string[] = []) => {
    switch (status) {
      case HalalStatus.HALAL:
        return <HalalStatusHalal />;
      case HalalStatus.NOT_HALAL:
        return <HalalStatusNotHalal reasons={reasons} />;
      case HalalStatus.HALAL_GIVEN_INGREDIENTS:
        return <HalalStatusGivenIngredients />;
      case HalalStatus.NOT_ENOUGH_INFORMATION:
        return <HalalStatusNotEnoughInformation />;
      default:
        return <HalalStatusUnknown />;
    }
  };

  const renderProductContent = () => {
    if (isProductFound && productData) {
      const { status, reasons } = productData;
      let borderColor: string;

      switch (status) {
        case HalalStatus.HALAL:
        case HalalStatus.HALAL_GIVEN_INGREDIENTS:
          borderColor = 'green';
          break;
        default:
          borderColor = 'red';
          break;
      }
      
      return (
        <View style={[styles.modalContent, { borderColor }]}>
          <ProductInformation productData={productData}>
            {renderHalalStatus(status, reasons)}
          </ProductInformation>
          <Button title="Close" onPress={closeModal} />
        </View>
      );
    } else {
      return <ProductNotFound closeModal={closeModal} />;
    }
  };

  return (
    <Modal animationType="slide" transparent visible={true} onRequestClose={closeModal}>
      <TouchableOpacity style={styles.modalOverlay} onPress={closeModal} activeOpacity={1}>
        <TouchableOpacity style={styles.modalContainer} activeOpacity={1}>
          {renderProductContent()}
        </TouchableOpacity>
      </TouchableOpacity>
    </Modal>
  );
}

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalContainer: {
    backgroundColor: 'white',
    padding: 20,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  modalContent: {
    marginBottom: 20,
  },
});

export default ProductInfoModal;
