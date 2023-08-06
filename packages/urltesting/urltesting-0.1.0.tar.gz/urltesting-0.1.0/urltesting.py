import os
import json
from urllib.parse import urljoin

import click
import requests
from fastutils import dictutils
from fastutils import hashutils

def parse_kvs(kvs):
    result = {}
    kvs = kvs or []
    for param in kvs:
        key, value = param.split("=")
        key = key.strip()
        value = value.strip()
        result[key] = value
    return result

@click.group()
def main():
    pass

@main.command()
@click.option("--listurl", required=True, help="The url where to get all the urls.")
@click.option("--listurl-method", default="GET", help="Request method. Default to GET.")
@click.option("--listurl-param", multiple=True, help="Request parameter in format key=value. Can be applied mutiple times.")
@click.option("--listurl-header", multiple=True, help="Request header in format header_name=header_value. Can be applied multiple times.")
@click.option("--listurl-payload", help="Request payload.")
@click.option("--list-format", default="list", type=click.Choice(["list", "jsonarray", "json"]), help="""The format of "--listurl" response content. "list" means every url per line. "jsonarray" means response content likes: ["/url1/", "url2"]. "json" means response likes: {"data": "urls": ["/url1", "url2"]}. Default to "list".""")
@click.option("--list-json-path", help="""If "--list-format=json", use the path to get urls from the json data, e.g. "--list-json-path=data.urls" when the response content is {"data": {"urls": ["/url1/", "/url2/"]}}. If url string is NOT starts with http, the entry url "--listurl" will be used to make the final url with "urljoin" method.""")
@click.option("--loginurl", help="Login url. [Optional]")
@click.option("--loginurl-method", default="GET", help="Request method. Default to GET.")
@click.option("--loginurl-param", multiple=True, help="Request parameter in format key=value. Can be applied mutiple times.")
@click.option("--loginurl-header", multiple=True, help="Request header in format header_name=header_value. Can be applied multiple times.")
@click.option("--loginurl-payload", help="Request payload.")
def simpleurls(
        loginurl, loginurl_method, loginurl_param, loginurl_header, loginurl_payload,
        listurl, listurl_method, listurl_param, listurl_header, listurl_payload, list_format, list_json_path):
    """Test urls. Urls are fetched from an url.
    """
    session = requests.session()

    if loginurl:
        loginurl_params = parse_kvs(loginurl_param)
        loginurl_headers = parse_kvs(loginurl_header)
        try:
            response = session.request(loginurl_method, listurl, params=loginurl_params, headers=loginurl_headers, data=loginurl_payload)
        except Exception as error:
            print(f"Do {loginurl} login failed, error message: {error}")
            os.sys.exit(1)

    listurl_params = parse_kvs(listurl_param)
    listurl_headers = parse_kvs(listurl_header)
    try:
        response = session.request(listurl_method, listurl, params=listurl_params, headers=listurl_headers, data=listurl_payload)
    except Exception as error:
        print(f"Get urls from {listurl} failed, error message: {error}")
        os.sys.exit(1)
    
    if response.status_code != 200:
        print(f"Get urls from {listurl} got response status != 200...")

    try:
        if list_format == "list":
            urls = [x.strip() for x in response.text.splitlines() if x]
        elif list_format == "jsonarray":
            urls = json.loads(response.content)
        elif list_format == "json":
            response_data = json.loads(response.content)
            dictutils.select(response_data, list_json_path)
    except Exception as error:
        print(f"Parse response content failed, error message: {error}")
        os.sys.exit(2)

    for url in urls:
        if not url.startswith("http"):
            url = urljoin(listurl, url)
        try:
            response = session.get(url)
        except Exception as error:
            print(f"Test url {url} failed, error message: {error}")
            os.sys.exit(3)
        
        status_code = response.status_code
        size = len(response.content)
        md5 = hashutils.get_md5_hexdigest(response.content)
        print(f"Get url {url} done, status_code={status_code}, size={size}, md5={md5}")
        
        if status_code != 200:
            print(f"Test url {url} failed for status code != 200...")
            os.sys.exit(4)
    
        
    print("OK")
    os.sys.exit(0)



if __name__ == "__main__":
    main()
