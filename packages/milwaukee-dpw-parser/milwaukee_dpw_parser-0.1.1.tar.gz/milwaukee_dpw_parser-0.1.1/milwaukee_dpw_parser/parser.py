import argparse
from bs4 import BeautifulSoup
import datetime
import aiohttp
import asyncio

def _try_parse_date(text: str):
	try:
		return datetime.datetime.strptime(text, "%A %B %d, %Y").date()
	except:
		pass

async def get_next_garbage_and_recycling_dates(address_number: str, street_direction: str, street_name: str, street_suffix: str):
	data = dict(laddr=address_number, sdir=street_direction, sname=street_name, stype=street_suffix, embed="Y", Submit="Submit")
	async with aiohttp.ClientSession() as session:
		async with session.post("https://itmdapps.milwaukee.gov/DpwServletsPublic/garbage_day", data=data) as response:
			response.raise_for_status()
			html = await response.text()

	parsed = BeautifulSoup(html, features="html.parser")
	strong_elements = parsed.find_all("strong")
	dates = []
	for element in parsed.find_all("strong"):
		parsed_date = _try_parse_date(element.text)
		if parsed_date:
			dates.append(parsed_date)
	
	if len(dates) != 2:
		raise Exception(f"Failed to parse: {html}")

	return dates[0], dates[1]

async def main():
	parser = argparse.ArgumentParser(description="Get data from Milwaukee DPW")
	parser.add_argument("address_number", type=str, help="Address number, e.g., 200")
	parser.add_argument("street_direction", type=str, help="Street direction, e.g., N")
	parser.add_argument("street_name", type=str, help="Street name, e.g., 1st")
	parser.add_argument("street_suffix", type=str, help="Street suffix, e.g., st")
	args = parser.parse_args()
	garbage_date, recycling_date = await get_next_garbage_and_recycling_dates(
		args.address_number, 
		args.street_direction.upper(), 
		args.street_name.upper(), 
		args.street_suffix.upper(),
	)
	print(garbage_date)
	print(recycling_date)

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
