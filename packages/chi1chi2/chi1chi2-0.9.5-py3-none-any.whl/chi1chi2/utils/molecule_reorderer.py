import itertools
from collections import deque
from functools import reduce
from typing import List, Tuple, Deque

import numpy as np

from chi1chi2.periodic_table.periodic_table import PeriodicTable
from chi1chi2.utils.constants import ChiException
from chi1chi2.utils.molecule import Molecule, XyzMolecule, Atom

periodic_table = PeriodicTable.create()


def are_atoms_bound(atom1: Atom, atom2: Atom) -> bool:
    sum_of_covalent_radii = periodic_table.get_covalent_radius_by_atomic_number(
        atom1.get_atomic_num()) + periodic_table.get_covalent_radius_by_atomic_number(atom2.get_atomic_num())
    return np.linalg.norm(np.array(atom1.get_coords()) - np.array(atom2.get_coords())) <= sum_of_covalent_radii * 1.1


def is_ordered(molecule: Molecule) -> bool:
    heavy_atom_index = 0
    heavy_atom = molecule.atoms[heavy_atom_index]
    if heavy_atom.is_hydrogen():
        return False
    current_index = 1
    while current_index < molecule.num_atoms:
        atom = molecule.atoms[current_index]
        if atom.is_heavy():
            heavy_atom_index = current_index
            heavy_atom = molecule.atoms[heavy_atom_index]
            current_index += 1
        else:
            hydrogen_atom = atom
            if not are_atoms_bound(heavy_atom, hydrogen_atom):
                print("heavy atom: " + str(heavy_atom) + " and hydrogen atom: " + str(
                    hydrogen_atom) + " are not bound - molecule not ordered")
                return False
            current_index += 1
    return True


def _group_heavies_by_molecule(heavy_atom_indices, connectivity_matrix):
    remaining_heavy_atoms = set(heavy_atom_indices.copy())

    # first (and maybe the only) molecule group for sure
    remaining_heavy_atoms = remaining_heavy_atoms.difference([heavy_atom_indices[0]])
    groups = [[heavy_atom_indices[0]]]

    while len(remaining_heavy_atoms) > 0:
        to_check = [groups[-1][0]]
        while len(to_check) > 0:
            current = to_check.pop(0)
            for heavy in remaining_heavy_atoms:
                if connectivity_matrix[current, heavy] > 0:
                    to_check.append(heavy)
                    groups[-1].append(heavy)
                    remaining_heavy_atoms = remaining_heavy_atoms.difference({heavy})
        if len(remaining_heavy_atoms) > 0:
            groups.append([remaining_heavy_atoms.pop()])
    # adding step to post-sort groups after using sets
    groups = [sorted(gr) for gr in groups]
    groups = sorted(groups, key=lambda gr: gr[0])
    return groups


def get_groups_uc(xyz_uc_molecules: List[XyzMolecule]) -> list:
    return list(itertools.chain.from_iterable(get_groups(molecule) for molecule in xyz_uc_molecules))


def get_groups(molecule: XyzMolecule) -> list:
    if not is_ordered(molecule):
        raise ChiException("Molecule should first be reordered! Failure from method >>get_groups<<")
    heavies, hydrogens = partition_atoms(molecule)
    adjacency_matrix = get_adjacency_matrix(molecule)
    heavies = _group_heavies_by_molecule(heavies, adjacency_matrix)
    groups = []
    for group_idx in range(len(heavies)):
        groups.append([])
        for heavy_idx in range(1, len(heavies[group_idx])):
            groups[-1].append(heavies[group_idx][heavy_idx] - heavies[group_idx][heavy_idx - 1])
        if group_idx < len(heavies) - 1:
            groups[-1].append(heavies[group_idx + 1][0] - heavies[group_idx][len(heavies[group_idx]) - 1])
    groups[-1].append(molecule.num_atoms - heavies[-1][-1])
    return groups


def get_molecules_by_groups(molecule: XyzMolecule) -> tuple:
    groups = get_groups(molecule)
    molecules = []
    act_first = 0
    for i in range(len(groups)):
        act_last = act_first + reduce(lambda a, b: a + b, groups[i])
        molecules.append(XyzMolecule(molecule.atoms[act_first:act_last], molecule.params))
        act_first = act_last
    return tuple(molecules)


def reorder_and_group_by_charge(molecule: Molecule) -> (tuple, tuple):
    molecule, groups = reorder(molecule)
    return group_by_charge(molecule, groups)


def group_by_charge(molecule: Molecule, groups: list) -> (tuple, tuple):
    if not is_ordered(molecule):
        raise ChiException("molecule is not ordered, failed to get group by charge")
    grouped_coordinates = []
    contracted_group_list = []
    current_atom_index = 0
    for i in range(len(groups)):
        submolecules = groups[i]
        contracted_group_list.append(len(submolecules))
        # iteration over one molecule group
        for j in range(len(submolecules)):
            coords, weight = np.zeros((3, 1)), 0.
            for k in range(submolecules[j]):
                atom = molecule.atoms[current_atom_index]
                weight += atom.get_atomic_num()
                coords += atom.get_atomic_num() * np.array(atom.get_coords()).reshape((3, 1))
                current_atom_index += 1
            grouped_coordinates.append((coords / weight)[:, 0].tolist())
    return grouped_coordinates, contracted_group_list


def adjust_hydrogen_atoms(molecule: Molecule) -> Molecule:
    """
    Adjusts heavy-hydrogen distances according to covalent radii
    :param molecule: molecule for adjustment
    :return: molecule with adjusted hydrogen atom positions
    """
    adjacency_matrix = get_adjacency_matrix(molecule)
    atom_list = []
    for atom_index, atom in enumerate(molecule.get_atoms()):
        if atom.is_hydrogen():
            heavy_atom_index = adjacency_matrix[atom_index].nonzero()[0][0]
            heavy_atom = molecule.atoms[heavy_atom_index]
            approximate_new_bond_length = (periodic_table.get_covalent_radius_by_symbol(
                'H') + periodic_table.get_covalent_radius_by_atomic_number(heavy_atom.get_atomic_num())) * .95
            bond_vector = atom.get_coords_array() - heavy_atom.get_coords_array()
            hydrogen_coordinates = heavy_atom.get_coords_array() + bond_vector / np.linalg.norm(
                bond_vector) * approximate_new_bond_length
            atom_list.append(Atom(atom.symbol, *hydrogen_coordinates.tolist()))
        else:
            atom_list.append(atom)
    return Molecule(atom_list, molecule.params)


def reorder(molecule: Molecule) -> (Molecule, tuple):
    reordered_atoms, groups = add_all_atoms(partition_atoms(molecule), get_adjacency_matrix(molecule))
    atoms = [molecule.atoms[i] for i in reordered_atoms]

    return Molecule(atoms, molecule.params), groups


def partition_atoms(molecule: Molecule) -> Tuple[Deque[Atom], Deque[Atom]]:
    heavy_atoms = deque()
    hydrogen_atoms = deque()

    atoms = molecule.get_atoms()
    for atom_index, atom in enumerate(atoms):
        if atom.is_hydrogen():
            hydrogen_atoms.append(atom_index)
        else:
            heavy_atoms.append(atom_index)

    return heavy_atoms, hydrogen_atoms


def get_adjacency_matrix(molecule: Molecule) -> np.ndarray:
    atoms = molecule.get_atoms()
    adjacency_matrix = np.zeros((molecule.num_atoms, molecule.num_atoms))
    for atom_index in range(molecule.num_atoms):
        for other_atom_index in range(molecule.num_atoms):
            if other_atom_index == atom_index:
                continue
            bound_value = 1 if are_atoms_bound(atoms[atom_index], atoms[other_atom_index]) else 0
            adjacency_matrix[atom_index, other_atom_index] = bound_value
            adjacency_matrix[other_atom_index, atom_index] = bound_value
    return adjacency_matrix


def __get_indices_for(a_list):
    return set([ind for ind in range(len(a_list)) if a_list[ind] > 0])


def __add_all_hydrogen_atoms_to_heavy_atom(seq, current_heavy, hydrogens, conn_matr, groups):
    connected_hydrogens = set(hydrogens).intersection(__get_indices_for(conn_matr[current_heavy]))
    for hydrogen_idx in connected_hydrogens:
        seq.append(hydrogen_idx)
        hydrogens.remove(hydrogen_idx)
        groups[-1][-1] += 1


def get_connected_heavy_atoms(current_heavy, heavies, adjacency_matrix):
    connected_heavies = set(heavies).intersection(__get_indices_for(adjacency_matrix[current_heavy]))
    for heavy_idx in connected_heavies:
        heavies.remove(heavy_idx)
    return connected_heavies


def add_all_atoms_to_sequence(seq, first_heavy, heavy_atoms, hydrogen_atoms, adjacency_matrix, groups):
    current_heavies = deque()
    current_heavies.append(first_heavy)
    while current_heavies:
        current_heavy = current_heavies.popleft()
        seq.append(current_heavy)
        groups[-1].append(1)
        current_heavies.extend(get_connected_heavy_atoms(current_heavy, heavy_atoms, adjacency_matrix))
        __add_all_hydrogen_atoms_to_heavy_atom(seq, current_heavy, hydrogen_atoms, adjacency_matrix, groups)


def add_all_atoms(heavy_and_hydrogen_atoms: Tuple[Deque[Atom], Deque[Atom]], adjacency_matrix: np.ndarray) -> \
        Tuple[List[Atom], List[List[int]]]:
    heavy_atoms, hydrogen_atoms = heavy_and_hydrogen_atoms
    if not heavy_atoms:
        raise ChiException("only hydrogen atoms, it won't work...")
    seq = []
    groups = []
    while heavy_atoms:  # there might be more than one molecule, let's iterate over them
        first_heavy = heavy_atoms.popleft()
        groups.append([])
        add_all_atoms_to_sequence(seq, first_heavy, heavy_atoms, hydrogen_atoms, adjacency_matrix, groups)
    return seq, groups
