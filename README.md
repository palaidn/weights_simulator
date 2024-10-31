# Validator Weight Adjustment Tool

This script allows you to fetch and adjust validator weights within a Bittensor subnet. It connects to a specified subnet, fetches validators, and enables simulated weight modifications. The script iteratively adjusts weights for specified validators and redistributes remaining weights to maintain a consistent total of `1` across all validators.

## Requirements

- Python 3.7 or higher
- `bittensor` library
- `numpy` library
- `torch` library

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/validator-weight-adjustment.git
   cd validator-weight-adjustment
   ```


2. **Create and activate a virtual environment (optional)**  
   ```bash
    python3 -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
    pip install bittensor numpy torch
   ```  


## Usage

1. **Run the script**  
   ```bash
    python validator_weights.py
   ```

2. **Specify the subnet**  
You’ll be prompted to enter a subnet ID (between `1` and `52`) to specify which subnet you want to examine.

3. **View and modify weights**
- The script will fetch and display validators in the specified subnet.
- After displaying initial weights, you can enter a `UID` and specify a new weight value (in percent) for a particular validator in the emissions column.
- The script will adjust other weights for the validator proportionally to ensure the total remains `1`.
- To exit the weight modification process, enter `X` when prompted.

4. **Review updated weights**  
After modifying weights, the script will display the updated weight distribution.

### Example

   ```bash
    Enter the subnet ID (1-52): 5
    Weight from UID[2] = 0.20%
    Weight from UID[6] = 1.50%
    ...
    Enter UID to simulate change weight (or 'X' to exit): 2
    Enter new weight value for UID[2] in %: 1.5
    Updated Weight from UID[2] = 1.5%
    ...
    Enter UID to simulate change weight (or 'X' to exit): X
    Exiting weight modification.
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
