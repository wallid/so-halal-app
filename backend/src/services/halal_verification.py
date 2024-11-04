from typing import Dict, Any
from src.services.halal_strategies import initialize_strategies
from src.models.enums import HalalStatus
import logging

logger = logging.getLogger(__name__)

def verify_halal(product_info: Dict[str, Any]):
    logger.info("Starting halal verification for product: %s", product_info.get('product_name', 'Unknown'))

    factory = initialize_strategies()
    overall_status = HalalStatus.HALAL
    haram_found_overall = set()
    reasons_overall = set()

    for strategy in factory.get_strategies():
        strategy_name = strategy.__class__.__name__
        logger.info("Applying strategy: %s", strategy_name)

        status, haram_found, reasons = strategy.is_halal(product_info)

        logger.debug("Strategy %s result - status: %s, haram_found: %s, reasons: %s",
                     strategy_name, status, haram_found, reasons)

        if status == HalalStatus.NOT_HALAL:
            overall_status = HalalStatus.NOT_HALAL
            haram_found_overall.update(haram_found)
            reasons_overall.update(reasons)
            logger.info("Strategy %s identified product as NOT_HALAL due to: %s", strategy_name, reasons)
            # No need to continue; we confirmed it as NOT_HALAL.
            break
        elif status == HalalStatus.HALAL_GIVEN_INGREDIENTS:
            if overall_status != HalalStatus.NOT_HALAL:
                overall_status = HalalStatus.HALAL_GIVEN_INGREDIENTS
                reasons_overall.update(reasons)
                logger.info("Strategy %s identified product as HALAL_GIVEN_INGREDIENTS.", strategy_name)
        elif status == HalalStatus.NOT_ENOUGH_INFORMATION:
            if overall_status == HalalStatus.HALAL:
                overall_status = HalalStatus.NOT_ENOUGH_INFORMATION
                reasons_overall.update(reasons)
                logger.info("Strategy %s identified product as NOT_ENOUGH_INFORMATION.", strategy_name)

    logger.info("Halal verification completed. Overall status: %s", overall_status)

    return {
        "status": overall_status,
        "haram_items_found": list(haram_found_overall),
        "reasons": list(reasons_overall)
    }
