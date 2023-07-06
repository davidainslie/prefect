import httpx  # requests capability, but can work with async
from prefect import flow, task

@task
def fetch_weather(lat: float, lon: float):
  base_url = "https://api.open-meteo.com/v1/forecast/"

  weather = httpx.get(base_url, params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"))
  most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])

  return most_recent_temp

@task
def fetch_wind_speed(lat: float, lon: float):
  base_url = "https://api.open-meteo.com/v1/forecast/"

  weather = httpx.get(base_url, params=dict(latitude=lat, longitude=lon, hourly="windspeed_10m"))
  wind_speed = float(weather.json()["hourly"]["windspeed_10m"][0])

  return wind_speed

@task
def save_weather(temp: float, wind_speed: float):
  with open("weather.csv", "a+") as w:
    w.write(str(temp) + ", " + str(wind_speed) + "\n")

  return "Successfully wrote temp and wind speed"

@flow
def pipeline(lat: float, lon: float):
  temp = fetch_weather(lat, lon)
  wind_speed = fetch_wind_speed(lat, lon)
  result = save_weather(temp, wind_speed)
  return result

if __name__ == "__main__":
  pipeline(38.9, -77.0)
