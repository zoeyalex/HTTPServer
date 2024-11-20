def pretty_print_request(parsed_request):
    '''
    Custom pretty print for parsed HTTP requests.
    '''
    print(f'Method: {parsed_request['method']}')
    print(f'Path: {parsed_request['path']}')
    print('Query Parameters:')
    if parsed_request['query_params']:
        for key, value in parsed_request['query_params'].items():
            print(f'  {key}: {value}')
    else:
        print('  None')
    print('Headers:')
    for key, value in parsed_request['headers'].items():
        print(f'  {key}: {value}')
    print(f'Body: {parsed_request['body']}')