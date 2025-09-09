# Cloud and Edge Bundle Service

## Overview
This repository contains a service for managing bundles in cloud and edge environments, including components for cloud integration, edge deployment, and metrics collection.

## Project Structure
- **bundle/**: Core bundle management logic, including:
  - **Model.py**: Definitions of model entities for bundles and capacities.
  - **ODRLmanager.py**: Manager for building, applying, and validating ODRL policies.
  - **Policy1.json / Policy2.json**: Example policies applied to bundle capacities.
  - **builder.py**: to create policy's objects
- **cloud/**: Cloud integration and deployment components and capacities running in the cloud platform (e.g., identification, trajectory planning, storage, traffic prediction).
- **edge/**: Edge integration and deployment components and capacities running in the edge platform (e.g., detection, decision-making).
- **latency calcul/**: Metrics collection and latency calculation (edge vs. cloud latencies).Mickael's Results
- **picar-x-code/**: Code for the autonomous car (Picar-X) interacting with the bundle service.
- **main.py**: Main script to run the bundle service.
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

## Notes on Usage

- In the **Picar-X main code (`picar-x-code/main.py`)**, you can choose whether to **evaluate policies** or not:
  - If policies are enabled, the car interacts with the `/decision` and `/detection` endpoints (which enforce **Policy1** and **Policy2**).
  - If policies are disabled, the car uses the raw endpoints `/decision-raw` and `/detection-raw`, bypassing policy evaluation.

- The repository includes a results.py  script for generating performance analysis.  
  Running these scripts will produce latency comparison plots, which are saved into the **images/** folder.

## Recommendations for Future Users

1. **Configuration**  
   - Verify IP addresses and ports in both `cloud/` and `edge/` before deployment.  
   - Make sure Docker is correctly configured with network access between edge, cloud, and the car.  

2. **Policies**  
   - New ODRL policies can be added in JSON format inside `bundle/`.  
   - Update `ODRLManager.py` if you need to define new actions, constraints, or verification logic. 

3. **Results and Monitoring**  
   - Latency logs are saved in `picar-x-code/`.  
   - Figures are automatically generated into `images/` for reports.  

