import prettytable
import argparse
from openstack import profile, connection


def get_server(con):
    result = prettytable.PrettyTable(['name', 'image', 'status', 'flavor', 'networks'])
    for server in con.compute.servers():
        image = con.compute.get_image(server["image"]["id"])["name"]
        flavor = con.compute.get_flavor(server["flavor"]["id"])["name"]
        result.add_row([server["name"], image, server["status"], flavor, 'net01'])
    return result.get_string()


def create_server(con, name):
    flavor = con.compute.find_flavor("m1.tiny")
    image = con.compute.find_image("cirros-0.3.4-x86_64")
    return con.compute.create_server(name=name, flavor=flavor, image=image)


def delete_server(con, name):
    server = con.compute.find_server(name)
    return con.compute.delete_server(server)


def get_volume(con):
    result = prettytable.PrettyTable(['name', 'status', 'size'])
    print(con.block_store.volumes)
    return result


def get_image(con):
    result = prettytable.PrettyTable(['name', 'disk_format'])
    result.align['name'] = 'l'
    for image in con.image.images():
        result.add_row([image["name"], image["disk_format"]])
    return result.get_string()


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
    print(get_image(con))
#   get_volume(con)
#   print(get_server(con))


if __name__ == '__main__':
    main()
