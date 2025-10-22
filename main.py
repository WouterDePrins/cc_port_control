import os
from dotenv import load_dotenv
from auth import CCAPI
from log import logging
import time

load_dotenv()  # Make sure .env if present

def ask_for_mac():
    while True:
        mac = input("Enter MAC address (format: XX:XX:XX:XX:XX:XX): ").strip()
        if len(mac.split(":")) == 6:
            return mac
        print("Invalid MAC address format. Try again.")


def ask_for_status():
    while True:
        status = input("Enter desired port status (UP/DOWN): ").strip().upper()
        if status in ["UP", "DOWN"]:
            return status
        print("Invalid status. Please enter 'UP' or 'DOWN'.")

def main():
    cc_url = os.environ.get("CC_URL")
    cc_username = os.environ.get("CC_USERNAME")
    cc_password = os.environ.get("CC_PASSWORD")
    cc = CCAPI(cc_url, cc_username, cc_password)
   
    switch_uuid = ''
    switch_name = ''
    switch_port_name = ''
    switch_port_uuid = ''
    switch_port_status = ''
    
    # Get device details by MAC address 
    while True:
        mac_address = ask_for_mac()
        logging.info(f"Searching for MAC address: {mac_address}")
        
        devices = cc.get(f"/dna/intent/api/v1/client-detail?macAddress={mac_address}")
        
        if "error" in devices:
            logging.info(f"MAC address {mac_address} not found. Try again.")
            continue
        else:
            break

    status = ask_for_status()
    connected_devices = devices.get('detail', {}).get('connectedDevice', [])
    switch_port_name = devices.get('detail', {}).get('port')

    for device in connected_devices:
        switch_uuid = device.get('id')
        switch_name = device.get('name')

    logging.info(f"Found {mac_address}, located on switch: '{switch_name}', port: '{switch_port_name}'")

    # Get switch port details and current status

    sw_interface = cc.get(f"/dna/intent/api/v1/interface/network-device/{switch_uuid}/interface-name?name={switch_port_name}")    
    interface = sw_interface.get('response', {})
    switch_port_uuid = interface.get('instanceUuid')
    switch_port_status = interface.get('adminStatus')

    logging.info(f"Current port status is '{switch_port_status}' for port name '{switch_port_name}' with UUID: '{switch_port_uuid}'")
    
    # Change port status if needed

    if switch_port_status != status:
        logging.info(f"Going to change the port status in: '{status}'...")
        port_change = cc.put(f"/dna/intent/api/v1/interface/{switch_port_uuid}?deploymentMode=Deploy", data={
            "adminStatus": status})
        port_change_task = port_change.get('response', {})
        port_change_task_id = port_change_task.get('taskId')
        logging.info(f"Executing task ID: {port_change_task_id} to change port status...")

        timeout = 20
        start_time = time.time()

        # Poll for task completion

        while True:
            task_response = cc.get(f"/api/v1/task/{port_change_task_id}")
            task_status_data = task_response.get('response', {})
            progress = task_status_data.get('progress', '')

            if 'SUCCESS' in progress:
                logging.info("Successfully pushed configuration.")
                break
            else:
                logging.info("Port status change in progress...")
            
            if time.time() - start_time > timeout:
                logging.error("Timeout waiting for port status change task to complete.")
                break
        
            time.sleep(3)



if __name__ == "__main__":
    main()