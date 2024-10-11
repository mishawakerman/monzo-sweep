import logging
import os
import sys
import argparse
from typing import Optional
from dotenv import load_dotenv
import monzo_lib as monzo

load_dotenv()

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

MIN_BALANCE = 1000  # Minimum balance in pence (£10)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monzo account balance manager")
    parser.add_argument("--pot", type=str, required=True, help="Name of the savings pot")
    parser.add_argument("--balance", type=int, required=True, help="Desired balance in pence")
    return parser.parse_args()


def get_account_id() -> Optional[str]:
    if account_id := os.getenv("MONZO_ACCOUNT_ID"):
        return account_id
    accounts = monzo.get_accounts()
    return accounts[0].get("id") if accounts else None


def find_savings_pot(account_id: str, pot_name: str) -> Optional[dict]:
    pots = monzo.get_pots(account_id)
    return next((pot for pot in pots if pot["name"] == pot_name), None)


def adjust_balance(account_id: str, pot_id: str, current_balance: int, desired_balance: int) -> None:
    if current_balance > desired_balance:
        amount = current_balance - desired_balance
        logger.info(f"Depositing {amount} into pot...")
        monzo.deposit_into_pot(account_id, pot_id, amount)
    else:
        amount = desired_balance - current_balance
        logger.info(f"Withdrawing {amount} from pot...")
        monzo.withdraw_from_pot(account_id, pot_id, amount)


def main() -> int:
    args = parse_arguments()
    logger.info("Starting Monzo Sweep...")
    try:
        account_id = get_account_id()
        if not account_id:
            logger.error("No account ID found")
            return EXIT_FAILURE

        logger.info(f"Using Account ID: {account_id}")
        current_balance = monzo.get_balance(account_id).get("balance")
        logger.info(f"Current balance: {current_balance}")

        if current_balance == args.balance:
            logger.info(f"Current balance is equal to desired balance of {args.balance}, exiting...")
            return EXIT_SUCCESS

        savings_pot = find_savings_pot(account_id, args.pot)
        if not savings_pot:
            logger.warning(f"No pot found with name '{args.pot}', exiting...")
            return EXIT_FAILURE

        logger.info(f"Found '{args.pot}' pot with ID: {savings_pot['id']}")
        adjust_balance(account_id, savings_pot["id"], current_balance, args.balance)

    except monzo.MonzoAPIError as e:
        logger.error(f"Monzo API error: {str(e)}")
        return EXIT_FAILURE
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return EXIT_FAILURE

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
