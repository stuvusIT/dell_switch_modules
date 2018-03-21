#!/usr/bin/env python3
import pexpect
import pexpect.fdpexpect
from serial import Serial
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

ser = Serial(
        port="/dev/ttyS0",
        baudrate=9600
        )

def run_module():
    module_args = dict(
            port = dict(type='str', required=True),
            mode = dict(type='str', required=True),
            pvid = dict(type='str', required=True),
            untagged = dict(type='list', required=False, default=[]),
            tagged = dict(type='list', required=False, default=[])
            )

    result = dict(
            changed = False
            )

    module = AnsibleModule(
            argument_spec = module_args,
            supports_check_mode = False
            )

    try:
        switch = pexpect.fdpexpect.fdspawn(ser, 5)
        switch.sendline("\n\r")
        console_state = switch.expect(["console>","console#","console(config)#"], 5)
        if console_state == 0:
            switch.sendline("enable")
            switch.expect("console#", 5)
            switch.sendline("configure")
            switch.expect("console(config)#", 5)
        elif console_state == 1:
            switch.sendline("configure")
            switch.expect("console(config)#", 5)
    finally:
        ser.close()

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
