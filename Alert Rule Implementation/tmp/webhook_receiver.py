#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # TODO: Read content length and request body
        content_length = # TODO: Get content length from headers
        post_data = # TODO: Read request body
        
        # TODO: Parse JSON data
        try:
            alerts = # TODO: Parse JSON
            
            # TODO: Process each alert
            print(f"\n{'='*60}")
            print(f"Alert received at {datetime.now()}")
            print(f"{'='*60}")
            
            for alert in alerts.get('alerts', []):
                # TODO: Extract alert details
                status = # TODO: Get status
                labels = # TODO: Get labels
                annotations = # TODO: Get annotations
                
                # TODO: Print alert information
                print(f"Status: {status}")
                print(f"Alert: {labels.get('alertname', 'Unknown')}")
                print(f"Severity: {labels.get('severity', 'Unknown')}")
                print(f"Summary: {annotations.get('summary', 'N/A')}")
                print(f"Description: {annotations.get('description', 'N/A')}")
                print("-" * 60)
                
        except Exception as e:
            print(f"Error processing alert: {e}")
        
        # TODO: Send response
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress default logging

# TODO: Start server
if __name__ == '__main__':
    server = HTTPServer(('localhost', 5001), WebhookHandler)
    print("Webhook receiver listening on port 5001...")
    server.serve_forever()
