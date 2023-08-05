=====
Usage
=====


To create handles::

    import os
    from acdh_handle_pyutils.client import HandleClient

    user = 'user12.12345-06'
    pw = os.environ.get('HANDLE_PASSWORD')  # e.g. if you don't want to expose credentials in code
    parsed_data = 'https://id.hansi4ever.com/123'  # URL to register handle

    hdl = HandleClient(user, pw)
    print(hdl.register_handle(parsed_data))
    #  'https://hdl.handle.net/21.11115/0000-000D-FFA0-F'

    print(hdl.register_handle(parsed_data, full_url=False))  # be aware, each time you call this method, a new handle is registered
    #  '21.11115/0000-010D-FFA0-F'


