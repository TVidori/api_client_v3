# Api Client v3

This is a repository used for explaining how to improve data collection speed for a custom API client by parallelising collections between different sources but also on the same source and by using proxies if needed.
The whole tutorial can be found at: https://medium.com/@thomas.vidori/386499e08fcb

If you need to adapt the code for a different API, modify the `API_BASE_URL` constant in `src/cleanuri_client.py` then adjust the existing endpoint function (`post_shorten_url`) to your needs. 
You can also add more endpoints.

This client and the associated tutorial are based on two previous repositories that can be found at: https://github.com/TVidori/api_client and https://github.com/TVidori/api_client_v2 
The associated tutorials are at: https://medium.com/@thomas.vidori/d9863b3ae7c2 and https://medium.com/@thomas.vidori/66aca6027c6e.
