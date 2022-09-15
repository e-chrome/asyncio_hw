import asyncio
import json
import aiohttp
import requests
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from swapi_async import get_people, health_check
from create_table import create_table, People

from sqlalchemy.orm import sessionmaker


PARTITION = 10
URL = 'https://swapi.dev/api/people/'
PG_DSN = 'postgresql+asyncpg://app:1234@127.0.0.1:5431/netology'

engine = create_async_engine(PG_DSN)

# определение числа персонажей
response = requests.get(URL)
dict_response = json.loads(response.text)
person_count = dict_response['count']


async def main():
    await create_table()

    health_check_task = asyncio.create_task(health_check())
    print(health_check_task)

    async with aiohttp.ClientSession() as web_session:
        people = await get_people(range(1, person_count + 1), PARTITION, web_session)

    people_list = []

    for person in people:
        params = {
            'birth_year': person['birth_year'],
            'eye_color': person['eye_color'],
            'films': ' '.join(person['films']),
            'gender': person['gender'],
            'hair_color': person['hair_color'],
            'height': person['height'],
            'homeworld': person['homeworld'],
            'mass': person['mass'],
            'name': person['name'],
            'skin_color': person['skin_color'],
            'species': ' '.join(person['species']),
            'starships': ' '.join(person['starships']),
            'vehicles': ' '.join(person['vehicles']),
            }
        people_list.append(People(**params))

    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as orm_session:
        orm_session.add_all(people_list)
        await orm_session.commit()


asyncio.run(main())
