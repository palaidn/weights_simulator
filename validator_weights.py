import bittensor as bt
from datetime import datetime
import numpy as np
import torch

def fetch_validators_set_weights(subnet: int, emissions: int, subtensor_url: str = "ws://127.0.0.1:9946"):
    """
    Fetch and print validators who have set weights for the given subnet.

    Args:
        subnet: Subnet ID for which to check the validators.
        subtensor_url: The endpoint of the subtensor node (default is local node ws://127.0.0.1:9946).
    """
    # Initialize the subtensor connection
    subtensor = bt.subtensor(network=subtensor_url)
    
    # Get the current metagraph 
    metagraph = subtensor.metagraph(netuid=subnet, lite=False)

    metagraph.sync(subtensor=subtensor)

    metagraph.weights.shape
    # Additional debug information
    print(f"{metagraph}")
    # print(f"{subtensor.weights(netuid=subnet)}")

    # Create a weight matrix with FP32 resolution
    W = metagraph.W.astype(np.float32)

    # Create "normalized" stake vector
    Sn = (metagraph.S / metagraph.S.sum()).astype(np.float32)


    # Iterate through the weight matrix
    for x in range(W.shape[0]):  # Iterate over rows (validators/subnets)
        if W[x][emissions] > 0:  # Check if weight is greater than 0
            print(f"Weight from UID[{x}] = {W[x][emissions]*100}%")  # Print row, column, a

    # Loop for user input to change weights
    while True:
        user_input = input("Enter UID to simulate change weight (or 'X' to exit): ").strip()
        
        if user_input.upper() == 'X':
            print("Exiting weight modification.")
            break
        
        try:
            uid = int(user_input)
            weight_value = float(input(f"Enter new weight value for UID[{uid}] in %: "))

            difference = weight_value / 100 - W[uid][emissions]
            W[uid][emissions] = weight_value / 100
            print(f"Updated Weight from UID[{uid}] = {W[uid][emissions]*100}%")

            # Iterate over the other weights in W[uid], lowering them sequentially
            for col in range(W.shape[1]):
                if col != emissions and difference > 0:  # Skip the emissions column
                    reduce_amount = min(W[uid][col], difference)  # Lower by `difference` or to zero
                    W[uid][col] -= reduce_amount
                    difference -= reduce_amount
                    
                    # Stop redistribution if the difference is fully absorbed
                    if difference <= 0:
                        break

        except ValueError:
            print("Invalid input. Please enter a numeric UID and weight value.")
        except IndexError:
            print(f"Invalid UID. Please enter a UID between 0 and {W.shape[0] - 1}.")
    


    # Iterate through the weight matrix
    for x in range(W.shape[0]):  # Iterate over rows (validators/subnets)
        if W[x][emissions] > 0:  # Check if weight is greater than 0
            print(f"Weight from UID[{x}] = {W[x][emissions]*100}%")  # Print row, column, a


    def trust(W, S, threshold=0):
        """Trust vector for subnets with variable threshold"""
        Wn = (W > threshold)
        return Wn.T @ S
    
    T = trust(W, Sn)

    def rank(W, S):
        """Rank vector for subnets"""
        R = W.T @ S
        return R / R.sum()
    
    R = rank(W, Sn)

    def consensus(T, kappa=0.5, rho=10):
        """Yuma Consensus 1"""
        # If T is a numpy array, convert it to a PyTorch tensor
        if isinstance(T, np.ndarray):
            T = torch.tensor(T, dtype=torch.float32)
        
        return torch.sigmoid(rho * (T - kappa))
    
    C = consensus(T)

    def emission(C, R):
        """Emission vector for subnets"""
        # Ensure both C and R are either NumPy arrays or PyTorch tensors
        if isinstance(C, torch.Tensor) and isinstance(R, np.ndarray):
            R = torch.tensor(R, dtype=C.dtype)
        elif isinstance(R, torch.Tensor) and isinstance(C, np.ndarray):
            C = torch.tensor(C, dtype=R.dtype)
    
        # Calculate the emission vector
        E = C * R
        return E / E.sum()
    
    E = emission(C, R)


    print(f"emissions: {E[emissions]*100}%")



if __name__ == "__main__":
    # Specify the subnet ID to fetch the validators for
    root_id = 0  # Change this to the subnet ID you want to check

    try:
        subnet_id = int(input("Enter the subnet ID (1-52): "))
        if subnet_id < 1 or subnet_id > 52:
            raise ValueError("Subnet ID must be between 1 and 52.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        exit()
    
    # Fetch and print validators who set weights
    fetch_validators_set_weights(subnet=root_id, emissions=subnet_id, subtensor_url='finney')
