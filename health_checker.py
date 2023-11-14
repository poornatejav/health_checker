import requests
import yaml
import time
from collections import defaultdict

class HealthChecker:
    def __init__(self, config_file):
        self.config_file = config_file
        self.results = defaultdict(lambda: {'total': 0, 'up': 0})

    def load_config(self):
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)

    def check_health(self, endpoint):
        try:
            response = requests.request(
                method=endpoint.get('method', 'GET'),
                url=endpoint['url'],
                headers=endpoint.get('headers', {}),
                data=endpoint.get('body', '')
            )
            latency = response.elapsed.total_seconds() * 1000
            if 200 <= response.status_code < 300 and latency < 500:
                return 'UP', latency
            else:
                return 'DOWN', latency
        except requests.RequestException as e:
            return 'DOWN', 0

    def run_health_checks(self):
        config = self.load_config()
        try:
            while True:
                for endpoint in config:
                    status, latency = self.check_health(endpoint)
                    domain = endpoint['url'].split('//')[1].split('/')[0]
                    self.results[domain]['total'] += 1
                    if status == 'UP':
                        self.results[domain]['up'] += 1
                self.print_results()
                time.sleep(15)
        except KeyboardInterrupt:
            self.print_results()

    def print_results(self):
        for domain, data in self.results.items():
            availability_percentage = (data['up'] / data['total']) * 100 if data['total'] > 0 else 0
            print(f"{domain} has {round(availability_percentage)}% availability percentage")

def main():
    checker = HealthChecker("/Users/poornateja/Documents/Documents/Fetch/config.yaml")  # Replace with the path to the configuration file
    checker.run_health_checks()

if __name__ == "__main__":
    main()
