import datetime
import heapq
import json
import logging
from typing import List

import requests

logging.basicConfig(level=logging.DEBUG)


class Lottery:
    def __init__(self):
        self.URL = 'https://www.njlottery.com/api/v1/draw-games/draws/page'
        self.pick_5_counter, self.mega_ball_counter = [], []
        self.pick_5_hot, self.mega_ball_hot = [], []
        self.pick_5_cold, self.mega_ball_cold = [], []

    def get_local_results(self, game_name: str = 'Mega Millions', period_in_years: int = 1) -> List[dict]:
        with open('mega_millions.json', 'r') as f:
            data = json.load(f)
            return data['draws']

    def get_results(self, game_name: str = 'Mega Millions', period_in_years: int = 1, size: int = 1000) -> List[dict]:
        params = {
            'date-from': int(
                (datetime.datetime.now() - datetime.timedelta(days=period_in_years * 365)).timestamp() * 1000),
            'date-to': int(datetime.datetime.now().timestamp() * 1000),
            'game-names': game_name,
            'status': 'CLOSED',
            'size': size,
            'page': 0
        }
        res = requests.get(self.URL, params).json()
        return res['draws']

    def parse_and_count(self, draws: List[dict]) -> None:
        self.pick_5_counter = [0] * 71
        self.mega_ball_counter = [0] * 26
        for draw in draws:
            results = draw['results'][0]['primary']
            for i in range(5):
                num = int(results[i])
                self.pick_5_counter[num] += 1
            self.mega_ball_counter[int(results[-1].replace('MB-', ''))] += 1

    def prepare_numbers_pool(self) -> None:
        for i, val in enumerate(self.pick_5_counter):
            if i:
                self.pick_5_hot.append((-val, i))
                self.pick_5_cold.append((val, i))
        for i, val in enumerate(self.mega_ball_counter):
            if i:
                self.mega_ball_hot.append((-val, i))
                self.mega_ball_cold.append((val, i))
        heapq.heapify(self.pick_5_hot)
        heapq.heapify(self.mega_ball_hot)
        heapq.heapify(self.pick_5_cold)
        heapq.heapify(self.mega_ball_cold)

    def pick(self) -> dict[str, list[list[int] | int]]:
        res = dict(hot=[[], 0], cold=[[], 0])
        for _ in range(5):
            res['hot'][0].append(heapq.heappop(self.pick_5_hot)[1])
            res['cold'][0].append(heapq.heappop(self.pick_5_cold)[1])
        res['hot'][0].sort()
        res['cold'][0].sort()
        res['hot'][1] = self.mega_ball_hot[0][1]
        res['cold'][1] = self.mega_ball_cold[0][1]
        return res


if __name__ == '__main__':
    lottery = Lottery()
    draws = lottery.get_results(period_in_years=3, size=100)
    lottery.parse_and_count(draws)
    lottery.prepare_numbers_pool()
    res = lottery.pick()
    logging.info(res)
