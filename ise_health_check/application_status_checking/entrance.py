from ise_health_check.ise_cli_handler import ise_cli_handler
from ise_health_check.ise_show_format import format_handler
import time
import json


if __name__ == "__main__":
    ise_ssh_session = ise_cli_handler()

    # Login ISE & check and clear all existing sessions
    while True:
        '''
        check and clear all existing sessions
        '''
        output = ise_ssh_session.remote_terminal.recv(65535)
        output_list = output.decode().split("\n")
        # print(output_list)
        if "admin#" in output_list[-1]:
            # 如果不存在existing session
            print("[Info] no existing session")
            break
        else:
            # 如果存在existing session
            ise_ssh_session.clear_existing_session()
            # renew the connection
            ise_ssh_session = ise_cli_handler()
            print("[Warning] Destroy the existing session and create a new session")

    # "enter key" sleep for 2 sec
    ise_ssh_session.remote_terminal.send("\n".encode())
    ise_ssh_session.remote_terminal.send("\n".encode())
    ise_ssh_session.remote_terminal.send("\x03\n".encode())
    ise_ssh_session.remote_terminal.send("\n".encode())
    # ise_ssh_session.remote_terminal.send("exit\n".encode())
    time.sleep(2)

    # perform the command
    output = ise_ssh_session.remote_terminal.recv(65535)
    output_list = output.decode().split("\n")
    # print(output_list)

    if "admin#" in output_list[-1]:
        print("[Info] Perform the show command 'show application status ise'")
        ise_ssh_session.remote_terminal.send("show application status ise\n".encode())
        time.sleep(50)
        output = ise_ssh_session.remote_terminal.recv(65535)
        output_list = output.decode().split("\n")
        # print(output_list)

    # format the output
    application_status_info = []   # raw data status line from "database listener" to "SXP engine service"
    for line_num in range(len(output_list)):
        # print(output_list[line_num])
        if "Database Listener" in output_list[line_num]:
            for info_num in range(11):
                application_status_info.append(output_list[line_num + info_num])
            break

    # format the raw data list
    format_processor = format_handler(application_status_info)
    # print(format_processor.format_application_info())

    # write the output in to log file
    log_file = open("../output_log/show_application.txt", "w", encoding="utf-8")
    log_file.write(json.dumps(format_processor.format_application_info()))
    log_file.close()

    # close the session
    ise_ssh_session.clear_existing_session()

