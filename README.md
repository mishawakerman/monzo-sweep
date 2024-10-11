# Monzo Sweep

A script that allows you to manage your Monzo account balance by automatically transferring money between your main account and a specified savings pot to maintain a desired balance. And a GitHub Actions worker to run this script nightly.

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

This example will aim to maintain a balance of £150 in your main account, moving excess funds to the specified pot or withdrawing from it if the balance falls below £150.

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

## Automated Nightly Sweep

This repository is set up with a GitHub Action that runs the sweep script nightly. Here's what you need to know:

- The script runs automatically at 1 AM UTC every day.
- It uses secrets and variables stored in the GitHub repository to access your Monzo account and perform the sweep.
- You can also trigger the workflow manually from the "Actions" tab in the GitHub repository.

### Setting up the GitHub Action

1. Ensure your repository has the following secrets set up:
   - `MONZO_ACCESS_TOKEN`: Your Monzo API access token
   - (optional) `MONZO_ACCOUNT_ID`: Your Monzo account ID

2. Set up the following repository variables:
   - `MONZO_POT_NAME`: The name of your savings pot
   - `MONZO_DESIRED_BALANCE`: Your desired balance in pence

3. The GitHub Action is defined in `.github/workflows/nightly-balance-check.yml`.

4. You can modify the schedule in the workflow file if you want the script to run at a different time.

### Updating Pot Name or Desired Balance

To update the pot name or desired balance:

1. Go to your GitHub repository
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Click on the "Variables" tab
4. Edit the `MONZO_POT_NAME` or `MONZO_DESIRED_BALANCE` variable as needed

These variables can be updated without modifying the workflow file, making it easier to adjust your balance management strategy.

### Monitoring the Automated Runs

- You can view the results of each run in the "Actions" tab of your GitHub repository.
- If there are any issues with the script execution, you'll see a failed workflow run.

### Security Note

Remember that the GitHub Action uses your Monzo API token to access your account. Ensure that you don't share your GitHub secrets with anyone unauthorized. While the pot name and desired balance are stored as variables and are less sensitive, consider the privacy implications of making this information visible to repository collaborators.

### Safety and Security

- Never share your Monzo API access token or include it directly in the script.
- Always use the `.env` file to store sensitive information.
- Regularly review your Monzo account activity to ensure the script is behaving as expected.

For more information on the Monzo API, visit the [Monzo Developer Documentation](https://docs.monzo.com/).