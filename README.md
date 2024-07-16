# Cloud and Edge Bundle Service

## Overview
This repository contains a service for managing bundles in cloud and edge environments, including components for cloud integration, edge deployment, and metrics collection.

## Project Structure
- **bundle/**: Core bundle management logic.
- **cloud/**: Cloud integration and deployment components and capacities running in the cloud plateforme.
- **edge/**: Edge integration and deployment components and capacities running in the edge plateforme.
- **latency calcul/**: Metrics collection and latency calcul.
- **main.py**: Main script to run the service.
- **requirements.txt**: List of dependencies.

## Installation bundle service
1. Clone the repository:
    ```sh
    git clone https://github.com/mpezongo/cloud-and-edge-bundle-service.git
    ```
2. Navigate to the project directory:
    ```sh
    cd cloud-and-edge-bundle-service
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Installation cloud configurations
1. Copy the cloud/ doc to your cloud server
2. Navigate to the projetc
   ```sh
   cd cloud/
   ```
3. Run the code with dockerfile
   ```sh
   chmod +x run.sh
   ./run.sh
   ```

## Installation edge configurations
1. Copy the edge/ doc to your edge server
2. Navigate to the projetc
   ```sh
   cd edge/
   ```
3. Run the code with dockerfile
   ```sh
   chmod +x run.sh
   ./run.sh
   ```
## Run bundle service
To run the main service:
```sh
python main.py
```

## Picar-x code usage
1. Copy the picar-x-code in the raspberry pi-4 on the picar-x car
2. Navigate to the project
  ```sh
  cd picar-x-code
  ```
3. Install requirements
   ```sh
   pip install -r requirements.txt
3. Run
   ```sh
   python main.py
   ```
