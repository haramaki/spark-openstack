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


def get_volume(con):
    result = prettytable.PrettyTable(['name', 'status', 'size'])
    print(con.block_store.volumes)
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
#   get_volume(con)
    print(get_server(con))


if __name__ == '__main__':
    main()
