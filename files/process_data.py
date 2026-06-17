#!/usr/bin/env python3
import sys
import json

def main():
    # AAP will pass arguments through the playbook wrapper
    if len(sys.argv) < 2:
        print(json.dumps({"failed": True, "msg": "Missing required input argument."}))
        sys.exit(1)
        
    input_data = sys.argv[1]
    
    # Perform your custom logic here
    output_message = f"Python successfully processed data: {input_data}"
    
    # Return data as JSON so Ansible can easily parse it
    result = {
        "changed": True,
        "message": output_message,
        "status": "Success"
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()
  
