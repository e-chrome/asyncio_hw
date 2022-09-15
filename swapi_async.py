import asyncio
import aiohttp

from more_itertools import chunked


URL = 'https://swapi.dev/api/people/'


async def get_person(person_id, web_session):
    async with web_session.get(f'{URL}{person_id}') as response:
        result = await response.json()
        if response.status == 200:
            return result


async def get_people(all_ids, partition, web_session):
    result = []
    for chunk_ids in chunked(all_ids, partition):
        tasks = [asyncio.create_task(get_person(person_id, web_session)) for person_id in chunk_ids]
        for task in tasks:
            task_result = await task
            if task_result is not None:
                result.append(task_result)
    return result


async def health_check():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get('https://swapi.dev/api/') as response:
                    if response.status == 200:
                        print('OK')
                    else:
                        print(response.status)
            except Exception as er:
                print(er)
            await asyncio.sleep(1)
