import yaml


def read_settings():
    with open('settings.yaml', 'r', encoding='utf-8') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def get_cluster_by_version(version):
    clusters = read_settings()['variables']['CLUSTERS']
    for cluster in clusters:
        if clusters[cluster]['version'] == version:
            return cluster


def get_cluster_and_ib_name(connection_string):
    connection_string = connection_string.replace('";', '')
    connection_string = connection_string.replace('Srvr="', '')
    cluster, ib_name = connection_string.split('Ref="')
    return cluster, ib_name
