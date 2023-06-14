from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from database_connections import azure_configuration
import difflib


def download_blob(container_name, file_name, path='static/downloaded/'):
    connection_string = azure_configuration.storage_connection_string
    blob = BlobClient.from_connection_string(conn_str = connection_string,
                                             container_name = container_name,
                                             blob_name = file_name)
    p = path+file_name
    with open(p, "wb+") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)
    my_blob.close()


def get_blob_list(container_name):
    connection_string = azure_configuration.storage_connection_string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_list = blob_service_client.get_container_client(container_name).list_blobs()
    l = []
    for blob in blob_list:
        l.append(blob.name)
    return l

def get_containing_file(host_list, filename):
    l = []
    for c in host_list:
        b = get_blob_list(container_name = c)
        if filename in b:
            l.append(c)
    return l

def print_host(host_list):
    for h in host_list:
        print(h)

def likely(s1, s2):
    result =  difflib.SequenceMatcher(a=s1.lower(), b=s2.lower())
    return result.ratio() >= 0.5

def likely_file(connected, filename):
    l = []
    for c in connected:
        blob_list = get_blob_list(container_name = c)
        for f in blob_list:
            if f not in l:
                if likely(f, filename):                
                    l.append(f)
    return l
