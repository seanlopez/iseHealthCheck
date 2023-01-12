
class format_handler(object):
    def __init__(self, application_raw_output):
        self.application_output = application_raw_output
        self.application_status = {}

    def format_application_info(self):
        '''
        format the "show application status ise" output
        return
        {"application server": "running", "Database Listener": "disable", ...}
        '''
        for raw_line in self.application_output:
            # convert the raw_line to a list
            info_list = raw_line.split("  ")
            # leverage the set() to delete duplicate space
            info_list = list(set(info_list))
            # remove "\r" in raw line
            try:
                info_list.remove("\r")
            except ValueError as v:
                pass

            # extract the "service name" & "status"
            service_name = ""
            status = ""
            # print(info_list)

            for item in info_list:
                item = item.strip()
                if item.isalpha():
                    # get the status
                    status = item
                elif item.isnumeric():
                    # if pure number, then ignore, since it's the process number
                    continue
                elif item == "":
                    # remove the empty value in list
                    continue
                else:
                    temp = item
                    if item.split(" ")[0].isnumeric():
                        # avoid the the process info like "XX processor"
                        continue
                    else:
                        # get the service name
                        service_name = temp
                        continue

            # store in dic
            self.application_status[service_name] = status

        return self.application_status



