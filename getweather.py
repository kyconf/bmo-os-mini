import asyncio
import httpx

async def get_north_york_weather():
    url = "https://weather.gc.ca/api/app/v3/en/Location/43.762,-79.410?type=city"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        print(data)

    # The API returns a list, grab the first result
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    else:
        return {"error": "Unexpected data format or empty list"}

    obs = data.get('observation', {})
   
    temp = obs.get('temperature', {}).get('metric')

    feels_like_val = obs.get('feelsLike', {}).get('metric')
 
    feels_like = feels_like_val if feels_like_val else temp
    
    # Extract Condition
    condition = obs.get('condition', 'Unknown')
    province = obs.get('provinceCode', {})
    return {
        "location": data.get('displayName', 'North York'),
        "provinceCode": province,
        "temp": temp,
        "feels_like": feels_like,
        "condition": condition
    }

if __name__ == "__main__":
    result = asyncio.run(get_north_york_weather())
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"B.MO Report for {result['location']}, {result['provinceCode']}:")
        print(f"Temp: {result['temp']}°C (Feels like {result['feels_like']}°C)")
        print(f"Conditions: {result['condition']}")