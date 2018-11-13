import os
import time

class EsgfTestUtils(object):
    __this_dir = os.path.abspath(os.path.dirname(__file__))
    __conf_dir = os.path.join(__this_dir, '..', 'configs')
    def run_cmd(self, cmd):
        ret_code = os.system(cmd)
        print("CMD: {cmd}, ret_code: {r}".format(cmd=cmd,
                                                 r=ret_code))
        return ret_code

    def update_esgf_policies_common(self, type, esgf_node=None):
        policy_file = "/esg/config/esgf_policies_common.xml"
        current_time = time.localtime(time.time())
        time_str = time.strftime("%b.%d.%Y.%H:%M:%S", current_time)
        backup = "{f}.{t}".format(f=policy_file,
                                  t=time_str)
        if type == 'restricted':
            filename = "esgf_policies_common.xml.restricted"
        elif type == 'cmip5':
            filename = "esgf_policies_common.xml.CMIP5"
        else:
            return 1

        file_to_copy = os.path.join(self.__conf_dir, filename)
        if os.path.isdir("/esg/config"):
            # on an esgf node
            cmd = "sudo -E bash -c \"cp -f {s} {d}\"".format(s=policy_file,
                                                             d=backup)
            ret_code = self.run_cmd(cmd)
            if ret_code != 0:
                return ret_code
            cmd = "sudo -E bash -c \"cp -f {s} {d}\"".format(s=file_to_copy,
                                                             d=policy_file)
            ret_code = self.run_cmd(cmd)
        else:
            # assumption: user can ssh to the esgf node
            cmd = "scp {s} {n}:/tmp".format(s=file_to_copy,
                                            n=esgf_node)
            ret_code = self.run_cmd(cmd)
            if ret_code != 0:
                return ret_code

            cmd = "ssh {n} sudo cp -f {s} {d}".format(n=esgf_node,
                                                      s=policy_file,
                                                      d= backup)
            ret_code = self.run_cmd(cmd)
            if ret_code != 0:
                return ret_code
            cmd = "ssh {n} sudo cp -f /tmp/{s} {d}".format(n=esgf_node,
                                                           s=filename,
                                                           d=policy_file)
            ret_code = self.run_cmd(cmd)
        return ret_code, backup

    def restore_esgf_policies_common(self, file_to_restore_from, esgf_node=None):
        file_to_restore_to = "/esg/config/esgf_policies_common.xml"
        if os.path.isdir("/esg/config"):
            # on an esgf node
            cmd = "sudo -E bash -c \"cp -f {s} {d}\"".format(s=file_to_restore_from,
                                                             d=file_to_restore_to)
            ret_code = self.run_cmd(cmd)
            if ret_code != 0:
                return ret_code
            cmd = "sudo -E bash -c \"rm {f}\"".format(f=file_to_restore_from)
            ret_code = self.run_cmd(cmd)
        else:
            cmd = "ssh {n} sudo cp -f {s} {d}".format(n=esgf_node,
                                                      s=file_to_restore_from,
                                                      d=file_to_restore_to)
            ret_code = self.run_cmd(cmd)
            if ret_code != 0:
                return ret_code
            cmd = "ssh {n} sudo rm {f}".format(n=esgf_node,
                                               f=file_to_restore_from)
            ret_code = self.run_cmd(cmd)
        return ret_code


