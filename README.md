# ansible-wrapper-python


Wrapping an existing Python script into Ansible to run inside Ansible Automation Platform (AAP) is a fantastic way to leverage your custom code while capitalizing on AAP's RBAC, logging, and execution governance.

When running scripts in AAP, you want the script to execute locally within the Automation Execution Environment (the container running the job) rather than on a remote target.

Here is a step-by-step example using a Python script, an Ansible playbook wrapper, and how it translates to an AAP configuration.

Step 1: The Python Script (process_data.py)
This example script accepts a command-line argument using sys.argv and performs a task. Place this file in your project repository (e.g., in a directory named files/ or the root).


```#!/usr/bin/env python3
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
```
Step 2: The Ansible Playbook Wrapper (run_script.yml)
Use the ansible.builtin.script module. Because we want AAP to execute this inside its own environment container, we use hosts: localhost and set gather_facts: false.

```
---
- name: Execute Custom Python Script in AAP
  hosts: localhost
  gather_facts: false
  vars:
    # This variable can be passed dynamically via AAP Survey or Extra Vars
    user_input: "Default AAP Data"

  tasks:
    - name: Run local Python script within the Execution Environment
      ansible.builtin.script:
        cmd: "process_data.py '{{ user_input }}'"
      register: script_output

    - name: Parse and Display the Python Script Output
      ansible.builtin.debug:
        msg: "The script returned: {{ script_output.stdout | from_json }}"
```
