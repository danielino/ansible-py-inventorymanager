

class Host:
    """
    this class is an abstraction of ansible Host

    ==== example usage ====
    > host = Host("my_host", {"key" : "val"})
    """

    def __init__(self, hostname, variables={}):
        """
        create a new host instnace

        :param hostname: hostname of host
        :param variables: ansible host_vars
        """
        self.hostname = hostname
        self._variables = variables

    def get_variables(self):
        return self._variables


class Group:
    """
    this class is an abstraction of ansible inventory Group

    ==== example usage ====
    > group = Group("myGroup")
    > host = Host("my_host", {"key" : "value"})
    > group.add_host(host)
    """

    def __init__(self, name, variables={}):
        """
        create a new group instance

        :param name: name of group
        :param variables: ansible group_vars
        """
        self.name = name
        self.variables = variables
        self.hosts = []
        self.children = []


    def has_childrens(self):
        return len(self.children) > 0

    def has_children(self, group):
        return group in self.children


    def get_childrens(self):
        return self.children


    def add_children(self, group):
        self.children.append(group)

    def has_hosts(self):
        return len(self.hosts) > 0

    def has_host(self, host):
        return host in self.hosts

    def get_hosts(self):
        return self.hosts

    def add_host(self, host):
        if not self.has_host(host):
            self.hosts.append(host)
            return True
        return False


class Inventory:
    """
    this class is an inventory object

    ==== example usage ====

    > group = Group("mygroup")
    > host_without_group = Host("ungrouped_host", {"key":"value"})
    > host_with_group  = Host("myhost", {"key": "value"})
    > group.add_host(host_with_group)

    > inv = Inventory("myInventory")
    > inv.add_group(group)
    > inv.add_host(host)
    > print json.dumps(inv.toJSON())
    """

    def __init__(self, name):
        """
        create new inventory object
        :param name: name of inventory
        """
        self.name = name
        self.groups = []
        self.hosts = []

    def search_group(self, groupName):
        """
        search a group by name
        :param groupName:
        :return:
        """
        for group in self.groups:
            if group.name == groupName:
                return group
        return False

    def search_host(self, hostname):
        """
        search an host by hostname
        :param hostname:
        :return:
        """
        for host in self.hosts:
            if host.hostname == hostname:
                return host
        return False

    def add_group(self, group):
        """
        add group to inventory
        :param group:
        :return:
        """
        if not self.search_group(group.name):
            self.groups.append(group)

    def add_hosts(self, host):
        """
        host added goes into "ungrouped" group
        :param host:
        :return:
        """
        if not self.search_host(host.hostname):
            self.hosts.append(host)


    def get_empty_inventory(self):
        return {
            "ungrouped" : [],
            "_meta" : {
                "hostvars" : {}
            }
        }


    def toJSON(self):
        """
        method that return a json object in ansible inventory format
        :return:
        """
        res = self.get_empty_inventory()

        for group in self.groups:
            if group.has_hosts() or group.has_childrens():
                res[group.name] = {
                    "hosts": [],
                    "vars": group.variables,
                    "children": []
                }
                if group.has_hosts():
                    for host in group.get_hosts():
                        res[group.name]['hosts'].append(host.hostname)
                        res['_meta']['hostvars'][host.hostname] = host.get_variables()
                if group.has_childrens():
                    for child in group.get_childrens():
                        res[group.name]['children'].append(child.name)


        for host in self.hosts:
            res['ungrouped'].append(host.hostname)
            res['_meta']['hostvars'][host.hostname] = host.get_variables()

        return res


