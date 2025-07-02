def one_map_geocode(address):
    """
    Geocode an address using the OneMap API.
    
    Parameters:
    address (str): The address to geocode.
    
    Returns:
    lat and long in a list
    """
    url = "https://www.onemap.gov.sg/api/common/elastic/search"
    params = {
        'searchVal': address,
        'returnGeom': 'Y',
        'getAddrDetails': 'Y',
        'pageNum': 1
    }
    
    headers = {"Authorization": "Bearer **********************"}  # Replace with your actual token
    
    print(address)

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        if response.json()['found'] > 0:
            results = response.json()['results']
            #print address name
            print(address, ' : ',results[0]['ADDRESS'])
            lat = results[0]['LATITUDE']
            long = results[0]['LONGITUDE']
            return [lat, long]
        else:
            print(f"No results found for address: {address}")
            return None
    else:
        print(f"No results found for address: {address}")
        return None