import prettytable
import argparse
from openstack import profile, connection


class OSController:
    def __init__(self, auth_url, region, project_name, username, password):
        prof = profile.Profile()
        prof.set_region(profile.Profile.ALL, region)

        self.con = connection.Connection(
            profile=prof,
            user_agent='examples',
            auth_url=auth_url,
            project_name=project_name,
            username=username,
            password=password
        )

    def list_server(self):
        svr_list = ""
        for server in self.con.compute.servers():
            addresses = server["addresses"]
            for net, address in addresses.items():
                net_out = net+" = "
                for addr in address:
                    net_out = net_out+addr["addr"]+" "

            svr_list = svr_list + "* " + server["name"] + " / " + server["status"] + " / " + net_out + "\n"
        return svr_list

    def show_server(self, name):
        sec_out = ""
        net_out = ""
        server_id = self.con.compute.find_server(name)["id"]
        server = self.con.compute.get_server(server_id)
        addresses = server["addresses"]
        for net, address in addresses.items():
            net_out = net+" = "
            for addr in address:
                net_out = net_out+addr["addr"]+" "
                secgroups = server["security_groups"]
                for secgroup in secgroups:
                    sec_out = sec_out + secgroup["name"] + " "

        result = "name : " + server["name"] + "\n"
        result = result + "status : " + server["status"] + "\n"
        result = result + "image : " + self.con.compute.get_image(server["image"]["id"])["name"] + "\n"
        result = result + "flavor : " + self.con.compute.get_flavor(server["flavor"]["id"])["name"] + "\n"
        result = result + "netowrk : " + net_out + "\n"
        result = result + "sec_group : " + sec_out

        return result

    def create_server(self, name):
        flavor = self.con.compute.find_flavor("m1.tiny")
        image = self.con.compute.find_image("cirros-0.3.4-x86_64")
        return self.con.compute.create_server(name=name, flavor=flavor, image=image)

    def delete_server(self, name):
        server = self.con.compute.find_server(name)
        return self.con.compute.delete_server(server)

    def get_flavor(self):
        result = ""
        for flavor in self.con.compute.flavors():
            result = result + "* " + flavor['name']
            result = result + " / " + str(flavor['vcpus']) + " cpu"
            result = result + " / " + str(flavor['ram']) + " MB"
            result = result + " / " + str(flavor['disk']) + " GB" + "\n"
        return result

    def get_volume(self):
        result = prettytable.PrettyTable(['name', 'status', 'size'])
        print(self.con.block_store.volumes)
        return result

    def get_image(self):
        result = ""
        for image in self.con.image.images():
            result = result + "* " + image['name'] + " / " + image["disk_format"] + "\n"
        return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-url")
    p.add_argument("-project")
    p.add_argument("-user")
    p.add_argument("-password")
    args = p.parse_args()
    os = OSController(args.url, "RegionOne", args.project, args.user, args.password)
    print(os.show_server("netone"))


if __name__ == '__main__':
    main()
