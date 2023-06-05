import logging
from random import choice
from typing import List, Tuple

logging.basicConfig(level=logging.DEBUG)


class Lottery:
    def pick(self, plays: int = 1) -> List[Tuple[List[int], int]]:
        res = []
        for play in range(plays):
            pick_5 = [num for num in range(1, 70)]
            play_res = []
            for pick in range(5):
                num = choice(pick_5)
                pick_5.remove(num)
                play_res.append(num)
            res.append((sorted(play_res), choice([num for num in range(1, 25)])))
        return res


if __name__ == '__main__':
    lottery = Lottery()
    results = lottery.pick(10)
    logging.info(results)
