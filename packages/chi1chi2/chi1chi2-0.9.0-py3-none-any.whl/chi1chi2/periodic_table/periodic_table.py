import os
from typing import Dict


class PeriodicTable:
    def __init__(self, atomic_number_to_symbol: Dict[int, str], atomic_number_to_covalent_radius: Dict[int, float]):
        self.atomic_number_to_symbol = atomic_number_to_symbol
        self.symbol_to_atomic_number = {it[1].lower(): it[0] for it in atomic_number_to_symbol.items()}
        self.atomic_number_to_covalent_radius = atomic_number_to_covalent_radius

    @classmethod
    def create(cls):
        atomic_number_to_symbol = {}
        atomic_number_to_covalent_radius = {}
        with open(os.path.join(os.path.dirname(__file__), 'ptable.csv')) as fh:
            lines = fh.readlines()[1:]
        for line in lines:
            atomic_number, atom_symbol, radius_in_pm = line.split(',')
            atomic_number_to_symbol[int(atomic_number)] = atom_symbol
            atomic_number_to_covalent_radius[int(atomic_number)] = float(radius_in_pm) / 100
        return cls(atomic_number_to_symbol, atomic_number_to_covalent_radius)

    def get_atomic_number(self, atomic_symbol: str) -> int:
        return self.symbol_to_atomic_number[atomic_symbol.lower()]

    def get_atomic_symbol(self, atomic_number: int) -> str:
        return self.atomic_number_to_symbol[atomic_number]

    def get_covalent_radius_by_symbol(self, atomic_symbol: str) -> float:
        return self.atomic_number_to_covalent_radius[self.get_atomic_number(atomic_symbol)]

    def get_covalent_radius_by_atomic_number(self, atomic_number: int) -> float:
        return self.atomic_number_to_covalent_radius[atomic_number]
