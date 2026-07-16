This Repo includes several use cases to experiment

1. ansible-wrapper-python (/files)
2. Squid Proxy Configuration with Event-Driven Capabilities (/proxy and /rulebooks)
3. IP and Ansible Ping sample (/ping)

# ansible-wrapper-python


Wrapping an existing Python script into Ansible to run inside Ansible Automation Platform (AAP) is a fantastic way to leverage your custom code while capitalizing on AAP's RBAC, logging, and execution governance.

When running scripts in AAP, you want the script to execute locally within the Automation Execution Environment (the container running the job) rather than on a remote target.

Here is a step-by-step example using a Python script, an Ansible playbook wrapper, and how it translates to an AAP configuration.

**Step 1: The Python Script (process_data.py)**

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
**Step 2: The Ansible Playbook Wrapper (run_script.yml)**

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
**Step 3: Executing in Ansible Automation Platform (AAP)**

To make this active inside AAP, follow these standard workflow steps:

Push to Git: Push both process_data.py and run_script.yml to your Git repository sync'd with AAP.

Sync Project: In the AAP Web UI, go to Projects and sync your repository.

Create a Job Template:

Go to Templates -> Add -> Add job template.

Inventory: Select Demo Inventory (or any inventory containing localhost).

Project: Select the Project you sync'd in step 2.

Playbook: Select run_script.yml from the dropdown.

Execution Environment: Select the standard target Execution Environment (e.g., ee-supported-rhel9 or your custom image containing any specific python pip packages your script imports).

Add an Optional Survey: * Click the Survey tab on the Job Template.

Add a text question with the Answer Variable named user_input. This maps directly to the {{ user_input }} variable in the playbook.

Launch: Click Launch. AAP will spawn an isolated container execution environment, feed your survey input down through the playbook, pass it into the Python execution layer, and print your JSON structured output cleanly inside the job tracking logs.

**Ansible Output Execution**

```
PLAY [Execute Custom Python Script in AAP] *************************************  3:14:20 PM

TASK [Run local Python script within the Execution Environment] ****************  3:14:20 PM
changed: [localhost]

TASK [Parse and Display the Python Script Output] ******************************  3:14:20 PM
ok: [localhost] => {
    "msg": "The script returned: {'changed': True, 'message': 'Python successfully processed data: Hello Ops Labs', 'status': 'Success'}"
}

PLAY RECAP *********************************************************************

localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
