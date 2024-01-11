import requests
import time
import logging
from logging.handlers import RotatingFileHandler

class AutoScaler:
    def __init__(self, base_url, target_cpu=0.75, threshold=0.05):
        self.base_url = base_url
        self.target_cpu = target_cpu
        self.threshold = threshold
        self.logger = self.setup_logger()

    def setup_logger(self):
        # Set up the logger configuration with a rotating file handler
        logger = logging.getLogger("AutoScaler")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Create a rotating file handler with a maximum file size of 10 MB and keep 3 backup files
        file_handler = RotatingFileHandler("autoscaler.log", maxBytes=10 * 1024 * 1024, backupCount=3)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def get_current_status(self):
        # Fetch the current status of the application via API
        url = f"{self.base_url}/app/status"
        try:
            response = requests.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error fetching current status: {e}")
            return None

    def update_replica_count(self, replicas):
        # Update the replica count of the application via API
        url = f"{self.base_url}/app/replicas"
        payload = {"replicas": replicas}
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.put(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.status_code
        except requests.RequestException as e:
            self.logger.error(f"Error updating replica count: {e}")
            return None

    def adjust_replicas(self):
        # Adjust the replicas based on CPU utilization
        current_status = self.get_current_status()
        if current_status is None:
            return

        current_cpu = current_status["cpu"]["highPriority"]
        current_replicas = current_status["replicas"]

        if current_cpu > self.target_cpu + self.threshold:
            # If CPU usage is high, increase replicas
            new_replicas = current_replicas + 1
            self.update_replica_count(new_replicas)
        elif current_cpu < self.target_cpu - self.threshold:
            # If CPU usage is low, decrease replicas, ensuring the replicas key is greater than one in /app/replicas API
            new_replicas = max(2, current_replicas - 1)
            self.update_replica_count(new_replicas)

def main():
    # Define the base URL of the Vimeo application
    base_url = "http://target-app-url"
    auto_scaler = AutoScaler(base_url)

    try:
        # Run the auto-scaler indefinitely, adjusting replicas every 60 seconds
        while True:
            auto_scaler.adjust_replicas()
            time.sleep(60)
    except KeyboardInterrupt:
        # Log a message when the auto-scaler is terminated
        auto_scaler.logger.info("Auto-scaler terminated.")

if __name__ == "__main__":
    main()
