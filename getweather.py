import asyncio
from env_canada import ECWeather

async def get_north_york_weather():
    #north york
    ec = ECWeather(station_id='ON/s0000395')
    await ec.update()

    temp = ec.conditions.get('temperature', {}).get('value')
    
    # Environment Canada Logic: 
    # If it's winter, it uses wind_chill. If it's summer, it uses humidex.
    feels_like = ec.conditions.get('wind_chill', {}).get('value') or \
                 ec.conditions.get('humidex', {}).get('value') or temp
    
    # High-level condition (e.g., "Cloudy", "Light Rain")
    condition = ec.conditions.get('condition', {}).get('value')

    return {
        "location": "North York",
        "temp": temp,
        "feels_like": feels_like,
        "condition": condition
    }
if __name__ == "__main__":
    result = asyncio.run(get_north_york_weather())
    print(f"B.MO Report for {result['location']}:")
    print(f"Temp: {result['temp']}°C (Feels like {result['feels_like']}°C)")
    print(f"Conditions: {result['condition']}")