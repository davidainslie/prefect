import httpx
from prefect import flow
from prefect import task
from prefect.context import get_run_context

@task(retries=4)
def fetch_weather(lat: float, lon: float):
  base_url = "https://api.open-meteo.com/v1/forecast/"

  count = get_run_context().task_run.run_count
  print(f"Count = {count}")

  if count == 1:
    raise Exception("Whoops.............")
  else:
    weather = httpx.get(base_url, params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"))

  most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
  return most_recent_temp

@flow
def pipeline(lat: float, lon: float):
  temp = fetch_weather(lat, lon)
  return temp

if __name__ == "__main__":
  pipeline(38.9, -77.0)