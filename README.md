## Usage

This script allows you to manage your Monzo account balance by automatically transferring money between your main account and a specified savings pot.

### Prerequisites

- Python 3.12 or higher
- A Monzo account with API access
- Your Monzo API access token

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/mwakerman/monzo-sweep
   cd monzo-sweep
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Configuration

1. Create a `.env` file in the project root directory with your Monzo API access token:
   ```
   MONZO_ACCESS_TOKEN=your_access_token_here
   ```

2. (Optional) If you want to use a specific Monzo account, you can also add its ID to the `.env` file:
   ```
   MONZO_ACCOUNT_ID=your_account_id_here
   ```

### Running the Script

The script requires two arguments:
- `--pot`: The name of your savings pot
- `--balance`: The desired balance in your main account (in pence)

Run the script using the following command:

```
python main.py --pot "Your Pot Name" --balance 15000
```

This example will aim to maintain a balance of £150 in your main account, moving excess funds to the specified pot or withdrawing from it if the balance falls below £1,500.

### Examples

1. To maintain a balance of £200 in your main account, using a pot named "Savings":
   ```
   python main.py --pot "Savings" --balance 20000
   ```

2. To maintain a balance of £500 in your main account, using a pot named "Rainy Day Fund":
   ```
   python main.py --pot "Rainy Day Fund" --balance 50000
   ```

### Notes

- The balance must be specified in pence. For example, £10 is represented as 1000.
- If the specified pot doesn't exist, the script will exit with an error message.
- The script will log its actions, including any deposits or withdrawals made.

### Troubleshooting

- If you encounter authentication errors, ensure your Monzo API access token is correct and hasn't expired.
- If the script can't find your account, try specifying the `MONZO_ACCOUNT_ID` in the `.env` file.
- For any other issues, check the error messages in the console output for guidance.

### Safety and Security

- Never share your Monzo API access token or include it directly in the script.
- Always use the `.env` file to store sensitive information.
- Regularly review your Monzo account activity to ensure the script is behaving as expected.

For more information on the Monzo API, visit the [Monzo Developer Documentation](https://docs.monzo.com/).