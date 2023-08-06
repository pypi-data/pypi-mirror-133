# urltesting

URLs testing tool.

## Usage

```
C:\test\httptest>python urltesting.py simpleurls --help
Usage: urltesting.py simpleurls [OPTIONS]

  Test urls. Urls are fetched from an url.

Options:
  --listurl TEXT                  The url where to get all the urls.
                                  [required]

  --listurl-method TEXT           Request method. Default to GET.
  --listurl-param TEXT            Request parameter in format key=value. Can
                                  be applied mutiple times.

  --listurl-header TEXT           Request header in format
                                  header_name=header_value. Can be applied
                                  multiple times.

  --listurl-payload TEXT          Request payload.
  --list-format [list|jsonarray|json]
                                  The format of "--listurl" response content.
                                  "list" means every url per line. "jsonarray"
                                  means response content likes: ["/url1/",
                                  "url2"]. "json" means response likes:
                                  {"data": "urls": ["/url1", "url2"]}. Default
                                  to "list".

  --list-json-path TEXT           If "--list-format=json", use the path to get
                                  urls from the json data, e.g. "--list-json-
                                  path=data.urls" when the response content is
                                  {"data": {"urls": ["/url1/", "/url2/"]}}. If
                                  url string is NOT starts with http, the
                                  entry url "--listurl" will be used to make
                                  the final url with "urljoin" method.

  --loginurl TEXT                 Login url. [Optional]
  --loginurl-method TEXT          Request method. Default to GET.
  --loginurl-param TEXT           Request parameter in format key=value. Can
                                  be applied mutiple times.

  --loginurl-header TEXT          Request header in format
                                  header_name=header_value. Can be applied
                                  multiple times.

  --loginurl-payload TEXT         Request payload.
  --help                          Show this message and exit.

```

## Releases

### v0.1.0 2021/01/05

- First release.
