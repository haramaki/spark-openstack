import prettytable
import argparse
from openstack import profile, connection


def list_server(con):
    svr_list = ""
    for server in con.compute.servers():
        addresses = server["addresses"]
        for net, address in addresses.items():
            net_out = net+" = "
            for addr in address:
                net_out = net_out+addr["addr"]+" "

        svr_list = svr_list + "* " + server["name"] + " / " + server["status"] + " / " + net_out + "\n"
    return svr_list


def show_server(con, name):
    sec_out = ""
    id = con.compute.find_server(name)["id"]
    server = con.compute.get_server(id)
    print(server)
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
    result = result + "image : " + con.compute.get_image(server["image"]["id"])["name"] + "\n"
    result = result + "flavor : " + con.compute.get_flavor(server["flavor"]["id"])["name"] + "\n"
    result = result + "netowrk : " + net_out + "\n"
    result = result + "sec_group : " + sec_out
    return result


def create_server(con, name):
    flavor = con.compute.find_flavor("m1.tiny")
    image = con.compute.find_image("cirros-0.3.4-x86_64")
    return con.compute.create_server(name=name, flavor=flavor, image=image)


def delete_server(con, name):
    server = con.compute.find_server(name)
    return con.compute.delete_server(server)


def get_flavor(con):
    result = ""
    for flavor in con.compute.flavors():
        result = result + "* " + flavor['name']
        result = result + " / " + str(flavor['vcpus']) + " cpu"
        result = result + " / " + str(flavor['ram']) + " MB"
        result = result + " / " + str(flavor['disk']) + " GB" + "\n"
    return result


def get_volume(con):
    result = prettytable.PrettyTable(['name', 'status', 'size'])
    print(con.block_store.volumes)
    return result


def get_image(con):
    result = ""
    for image in con.image.images():
        result = result + "* " + image['name'] + " / " + image["disk_format"] + "\n"
    return result


def create_connection(auth_url, region, project_name, username, password):
    prof = profile.Profile()
    prof.set_region(profile.Profile.ALL, region)

    return connection.Connection(
        profile=prof,
        user_agent='examples',
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password
    )



def main():
    p = argparse.ArgumentParser()
    p.add_argument("-url")
    p.add_argument("-project")
    p.add_argument("-user")
    p.add_argument("-password")
    args = p.parse_args()
    con = create_connection(args.url, "RegionOne", args.project, args.user, args.password)
#    print(get_image(con))
#    get_volume(con)
    print(show_server(con, "netone"))


if __name__ == '__main__':
    main()
