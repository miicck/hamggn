'''
Descripttion: 
version: 
Author: Yang Zhong
Date: 2023-01-16 13:00:43
LastEditors: Yang Zhong
LastEditTime: 2023-12-30 11:28:31
'''

from ase import Atoms
import numpy as np
from ctypes import Union
import numpy as np
from typing import Tuple, Union, Optional, List, Set, Dict, Any
from pymatgen.core.periodic_table import Element
from ase import Atoms
import re

def ase_atoms_to_openmxfile(atoms:Atoms, basic_commad:str, spin_set:dict, PAO_dict:dict, PBE_dict:dict, filename:str):
    chemical_symbols = atoms.get_chemical_symbols()
    species = set(chemical_symbols)
    positions = atoms.get_array(name='positions')
    cell = atoms.get_cell().array
    openmx = basic_commad
    openmx += "#\n# Definition of Atomic Species\n#\n"
    openmx += f'Species.Number       {len(species)}\n'
    openmx += '<Definition.of.Atomic.Species\n'
    for s in species:
        openmx += f"{s}   {PAO_dict[s]}       {PBE_dict[s]}\n"    
    openmx += "Definition.of.Atomic.Species>\n\n"
    openmx += "#\n# Atoms\n#\n"
    openmx += "Atoms.Number%12d" % len(chemical_symbols)
    openmx += "\nAtoms.SpeciesAndCoordinates.Unit   Ang # Ang|AU"
    openmx += "\n<Atoms.SpeciesAndCoordinates           # Unit=Ang."
    for num, sym in enumerate(chemical_symbols):
        openmx += "\n%3d  %s  %10.7f  %10.7f  %10.7f   %.2f   %.2f" % (num+1, sym, *positions[num], *spin_set[chemical_symbols[num]])
    openmx += "\nAtoms.SpeciesAndCoordinates>"
    openmx += "\nAtoms.UnitVectors.Unit             Ang #  Ang|AU"
    openmx += "\n<Atoms.UnitVectors                     # unit=Ang."
    openmx += "\n      %10.7f  %10.7f  %10.7f\n      %10.7f  %10.7f  %10.7f\n      %10.7f  %10.7f  %10.7f" % (*cell[0], *cell[1], *cell[2])
    openmx += "\nAtoms.UnitVectors>"
    with open(filename,'w') as wf:
        wf.write(openmx)

# Warning: this dict is not complete!!!
spin_set = {'H':[0.5, 0.5], # 1
            'He':[1.0,1.0], # 2
            'Li':[1.5,1.5], # 3
            'Be':[1.0,1.0], # 4
            'B':[1.5,1.5],  # 5
            'C':[2.0, 2.0],  # 6
            'N': [2.5,2.5],  # 7
            'O':[3.0,3.0],  # 8
            'F':[3.5,3.5], # 9
            'Ne':[4.0,4.0], # 10
            'Na':[4.5,4.5], # 11
            'Mg':[4.0,4.0], # 12
            'Al':[1.5,1.5], # 13
            'Si':[2.0,2.0], # 14
            'P':[2.5,2.5], # 15
            'S':[3.0,3.0], # 16
            'Cl':[3.5,3.5], # 17
            'Ar':[4.0,4.0], # 18
            'K':[4.5,4.5], # 19
            'Ca':[5.0,5.0], # 20
            'Sc':[5.5, 5.5],
            'Ti':[6.0, 6.0],
            'V': [6.5,6.5],
            'Cr':[7.0,7.0],
            'Mn':[7.5,7.5],
            'Fe':[8.0,8.0],
            'Co':[8.5,8.5],
            'Ni':[9.0, 9.0],
            'Cu':[9.5, 9.5],
            'Zn':[10.0, 10.0],
            'Ga':[6.5,6.5],
            'Ge':[2.0,2.0],
            'As':[7.5, 7.5],
            'Se':[3.0, 3.0],
            'Br':[3.5,3.5],
            'Kr':[4.0,4.0],
            'Rb':[4.5,4.5],
            'Sr':[5.0, 5.0],
            'Y':[5.5,5.5],
            'Zr':[6.0,6.0],
            'Nb':[6.5,6.5],
            'Mo':[7.0,7.0],
            'Tc':[7.5,7.5],
            'Ru':[7.0,7.0],
            'Rh':[7.5,7.5],
            'Pd':[8.0,8.0],
            'Ag':[8.5,8.5],
            'Cd':[6.0,6.0],
            'In':[6.5,6.5],
            'Sn':[7.0,7.0],
            'Sb':[7.5,7.5],
            'Te':[8.0,8.0],
            'I':[3.5,3.5],
            'Xe':[4.0,4.0],
            'Cs':[4.5,4.5],
            'Ba':[5.0,5.0],
            'La':[5.5,5.5],
            'Ce':[6.0,6.0],
            'Pr':[6.5,6.5],
            'Nd':[7.0,7.0],
            'Pm':[7.5,7.5],
            'Sm':[8.0,8.0],
            'Dy':[10.0,10.0],
            'Ho':[10.5,10.5],
            'Lu':[5.5,5.5],
            'Hf':[6.0,6.0],
            'Ta':[6.5,6.5],
            'W':[6.0,6.0],
            'Re':[7.5,7.5],
            'Os':[7.0,7.0],
            'Ir':[7.5,7.5],
            'Pt':[8.0,8.0],
            'Au':[8.5,8.5],
            'Hg':[9.0,9.0],
            'Tl':[9.5,9.5],
            'Pb':[7.0,7.0],
            'Bi':[7.5,7.5],
            }

# Warning: this dict is not complete!!!
PAO_dict = {'H':'H6.0-s2p1',
            'He':'He8.0-s2p1',
            'Li':'Li8.0-s3p2',
            'Be':'Be7.0-s2p2',
            'B':'B7.0-s2p2d1',
            'C':'C6.0-s2p2d1',
            'N':'N6.0-s2p2d1',
            'O':'O6.0-s2p2d1',
            'F':'F6.0-s2p2d1',
            'Ne':'Ne9.0-s2p2d1',
            'Na':'Na9.0-s3p2d1',
            'Mg':'Mg9.0-s3p2d1',
            'Al':'Al7.0-s2p2d1',
            'Si':'Si7.0-s2p2d1',
            'P':'P7.0-s2p2d1',
            'S':'S7.0-s2p2d1',
            'Cl':'Cl7.0-s2p2d1',
            'Ar':'Ar9.0-s2p2d1',
            'K':'K10.0-s3p2d1',
            'Ca':'Ca9.0-s3p2d1',
            'Sc':'Sc9.0-s3p2d1',
            'Ti':'Ti7.0-s3p2d1',
            'V':'V6.0-s3p2d1',
            'Cr':'Cr6.0-s3p2d1',
            'Mn':'Mn6.0-s3p2d1',
            'Fe':'Fe5.5H-s3p2d1',
            'Co':'Co6.0H-s3p2d1',
            'Ni':'Ni6.0H-s3p2d1',
            'Cu':'Cu6.0H-s3p2d1',
            'Zn':'Zn6.0H-s3p2d1',
            'Ga':'Ga7.0-s3p2d2',
            'Ge':'Ge7.0-s3p2d2',
            'As':'As7.0-s3p2d2',
            'Se':'Se7.0-s3p2d2',
            'Br':'Br7.0-s3p2d2',
            'Kr':'Kr10.0-s3p2d2',
            'Rb':'Rb11.0-s3p2d2',
            'Sr':'Sr10.0-s3p2d2',
            'Y':'Y10.0-s3p2d2',
            'Zr':'Zr7.0-s3p2d2',
            'Nb':'Nb7.0-s3p2d2',
            'Mo':'Mo7.0-s3p2d2',
            'Tc':'Tc7.0-s3p2d2',
            'Ru':'Ru7.0-s3p2d2',
            'Rh':'Rh7.0-s3p2d2',
            'Pd':'Pd7.0-s3p2d2',
            'Ag':'Ag7.0-s3p2d2',
            'Cd':'Cd7.0-s3p2d2',
            'In':'In7.0-s3p2d2',
            'Sn':'Sn7.0-s3p2d2',
            'Sb':'Sb7.0-s3p2d2',
            'Te':'Te7.0-s3p2d2f1',
            'I':'I7.0-s3p2d2f1',
            'Xe':'Xe11.0-s3p2d2',
            'Cs':'Cs12.0-s3p2d2',
            'Ba':'Ba10.0-s3p2d2',
            'La':'La8.0-s3p2d2f1',
            'Ce':'Ce8.0-s3p2d2f1',
            'Pr':'Pr8.0-s3p2d2f1',
            'Nd':'Nd8.0-s3p2d2f1',
            'Pm':'Pm8.0-s3p2d2f1',
            'Sm':'Sm8.0-s3p2d2f1',
            'Dy':'Dy8.0-s3p2d2f1',
            'Ho':'Ho8.0-s3p2d2f1',
            'Lu':'Lu8.0-s3p2d2f1',
            'Hf':'Hf9.0-s3p2d2f1',
            'Ta':'Ta7.0-s3p2d2f1',
            'W':'W7.0-s3p2d2f1',
            'Re':'Re7.0-s3p2d2f1',
            'Os':'Os7.0-s3p2d2f1',
            'Ir':'Ir7.0-s3p2d2f1',
            'Pt':'Pt7.0-s3p2d2f1',
            'Au':'Au7.0-s3p2d2f1',
            'Hg':'Hg8.0-s3p2d2f1',
            'Tl':'Tl8.0-s3p2d2f1',
            'Pb':'Pb8.0-s3p2d2f1',
            'Bi':'Bi8.0-s3p2d2f1',
            }

# Warning: this dict is not complete!!!
PBE_dict = {'H':'H_PBE19',
            'He':'He_PBE19',
            'Li':'Li_PBE19',
            'Be':'Be_PBE19',
            'B':'B_PBE19',
            'C':'C_PBE19',
            'N':'N_PBE19',
            'O':'O_PBE19',
            'F':'F_PBE19',
            'Ne':'Ne_PBE19',
            'Na':'Na_PBE19',
            'Mg':'Mg_PBE19',
            'Al':'Al_PBE19',
            'Si':'Si_PBE19',
            'P':'P_PBE19',
            'S':'S_PBE19',
            'Cl':'Cl_PBE19',
            'Ar':'Ar_PBE19',
            'K':'K_PBE19',
            'Ca':'Ca_PBE19',
            'Sc':'Sc_PBE19',
            'Ti':'Ti_PBE19',
            'V':'V_PBE19',
            'Cr':'Cr_PBE19',
            'Mn':'Mn_PBE19',
            'Fe':'Fe_PBE19H',
            'Co':'Co_PBE19H',
            'Ni':'Ni_PBE19H',
            'Cu':'Cu_PBE19H',
            'Zn':'Zn_PBE19H',
            'Ga':'Ga_PBE19',
            'Ge':'Ge_PBE19',
            'As':'As_PBE19',
            'Se':'Se_PBE19',
            'Br':'Br_PBE19',
            'Kr':'Kr_PBE19',
            'Rb':'Rb_PBE19',
            'Sr':'Sr_PBE19',
            'Y':'Y_PBE19',
            'Zr':'Zr_PBE19',
            'Nb':'Nb_PBE19',
            'Mo':'Mo_PBE19',
            'Tc':'Tc_PBE19',
            'Ru':'Ru_PBE19',
            'Rh':'Rh_PBE19',
            'Pd':'Pd_PBE19',
            'Ag':'Ag_PBE19',
            'Cd':'Cd_PBE19',
            'In':'In_PBE19',
            'Sn':'Sn_PBE19',
            'Sb':'Sb_PBE19',
            'Te':'Te_PBE19',
            'I':'I_PBE19',
            'Xe':'Xe_PBE19',
            'Cs':'Cs_PBE19',
            'Ba':'Ba_PBE19',
            'La':'La_PBE19',
            'Ce':'Ce_PBE19',
            'Pr':'Pr_PBE19',
            'Nd':'Nd_PBE19',
            'Pm':'Pm_PBE19',
            'Sm':'Sm_PBE19',
            'Dy':'Dy_PBE19',
            'Ho':'Ho_PBE19',
            'Lu':'Lu_PBE19',
            'Hf':'Hf_PBE19',
            'Ta':'Ta_PBE19',
            'W':'W_PBE19',
            'Re':'Re_PBE19',
            'Os':'Os_PBE19',
            'Ir':'Ir_PBE19',
            'Pt':'Pt_PBE19',
            'Au':'Au_PBE19',
            'Hg':'Hg_PBE19',
            'Tl':'Tl_PBE19',
            'Pb':'Pb_PBE19',
            'Bi':'Bi_PBE19',
            }

def _nice_float(x,just,rnd):
    return str(round(x,rnd)).rjust(just)

class kpoints_generator:
    """
    Used to generate K point path
    """
    def __init__(self, dim_k: int=3, lat: Union[np.array, list]=None, per: Union[List, Tuple] = None):
        self._dim_k = dim_k
        self._lat = lat
        # choose which self._dim_k out of self._dim_r dimensions are
        # to be considered periodic.        
        if per==None:
            # by default first _dim_k dimensions are periodic
            self._per=list(range(self._dim_k))
        else:
            if len(per)!=self._dim_k:
                raise Exception("\n\nWrong choice of periodic/infinite direction!")
            # store which directions are the periodic ones
            self._per=per
        
    def k_path(self,kpts,nk,report=True):
    
        # processing of special cases for kpts
        if kpts=='full':
            # full Brillouin zone for 1D case
            k_list=np.array([[0.],[0.5],[1.]])
        elif kpts=='fullc':
            # centered full Brillouin zone for 1D case
            k_list=np.array([[-0.5],[0.],[0.5]])
        elif kpts=='half':
            # half Brillouin zone for 1D case
            k_list=np.array([[0.],[0.5]])
        else:
            k_list=np.array(kpts)
    
        # in 1D case if path is specified as a vector, convert it to an (n,1) array
        if len(k_list.shape)==1 and self._dim_k==1:
            k_list=np.array([k_list]).T

        # make sure that k-points in the path have correct dimension
        if k_list.shape[1]!=self._dim_k:
            print('input k-space dimension is',k_list.shape[1])
            print('k-space dimension taken from model is',self._dim_k)
            raise Exception("\n\nk-space dimensions do not match")

        # must have more k-points in the path than number of nodes
        if nk<k_list.shape[0]:
            raise Exception("\n\nMust have more points in the path than number of nodes.")

        # number of nodes
        n_nodes=k_list.shape[0]
    
        # extract the lattice vectors from the TB model
        lat_per=np.copy(self._lat)
        # choose only those that correspond to periodic directions
        lat_per=lat_per[self._per]    
        # compute k_space metric tensor
        k_metric = np.linalg.inv(np.dot(lat_per,lat_per.T))

        # Find distances between nodes and set k_node, which is
        # accumulated distance since the start of the path
        #  initialize array k_node
        k_node=np.zeros(n_nodes,dtype=float)
        for n in range(1,n_nodes):
            dk = k_list[n]-k_list[n-1]
            dklen = np.sqrt(np.dot(dk,np.dot(k_metric,dk)))
            k_node[n]=k_node[n-1]+dklen
    
        # Find indices of nodes in interpolated list
        node_index=[0]
        for n in range(1,n_nodes-1):
            frac=k_node[n]/k_node[-1]
            node_index.append(int(round(frac*(nk-1))))
        node_index.append(nk-1)
    
        # initialize two arrays temporarily with zeros
        #   array giving accumulated k-distance to each k-point
        k_dist=np.zeros(nk,dtype=float)
        #   array listing the interpolated k-points    
        k_vec=np.zeros((nk,self._dim_k),dtype=float)
    
        # go over all kpoints
        k_vec[0]=k_list[0]
        for n in range(1,n_nodes):
            n_i=node_index[n-1]
            n_f=node_index[n]
            kd_i=k_node[n-1]
            kd_f=k_node[n]
            k_i=k_list[n-1]
            k_f=k_list[n]
            for j in range(n_i,n_f+1):
                frac=float(j-n_i)/float(n_f-n_i)
                k_dist[j]=kd_i+frac*(kd_f-kd_i)
                k_vec[j]=k_i+frac*(k_f-k_i)
    
        if report==True:
            if self._dim_k==1:
                print(' Path in 1D BZ defined by nodes at '+str(k_list.flatten()))
            else:
                print('----- k_path report begin ----------')
                original=np.get_printoptions()
                np.set_printoptions(precision=5)
                print('real-space lattice vectors\n', lat_per)
                print('k-space metric tensor\n', k_metric)
                print('internal coordinates of nodes\n', k_list)
                if (lat_per.shape[0]==lat_per.shape[1]):
                    # lat_per is invertible
                    lat_per_inv=np.linalg.inv(lat_per).T
                    print('reciprocal-space lattice vectors\n', lat_per_inv)
                    # cartesian coordinates of nodes
                    kpts_cart=np.tensordot(k_list,lat_per_inv,axes=1)
                    print('cartesian coordinates of nodes\n',kpts_cart)
                print('list of segments:')
                for n in range(1,n_nodes):
                    dk=k_node[n]-k_node[n-1]
                    dk_str=_nice_float(dk,7,5)
                    print('  length = '+dk_str+'  from ',k_list[n-1],' to ',k_list[n])
                print('node distance list:', k_node)
                print('node index list:   ', np.array(node_index))
                np.set_printoptions(precision=original["precision"])
                print('----- k_path report end ------------')
            print()

        return (k_vec,k_dist,k_node,lat_per_inv, node_index)

# Warning: this dict is not complete!!!
# openmx
# s1, s2, s3, px1, py1, pz1, px2, py2, pz2, d3z^2-r^2, dx^2-y^2, dxy, dxz, dyz
# siesta
# .........., py1, pz1, px1, ............., dxy, dyz, dz2, dxz, dx2-y2
#              4    5    3                  11   13    9   12    10
basis_def_19 = {1:np.array([0,1,3,4,5], dtype=int), # H
             2:np.array([0,1,3,4,5], dtype=int), # He
             3:np.array([0,1,2,3,4,5,6,7,8], dtype=int), # Li
             4:np.array([0,1,3,4,5,6,7,8], dtype=int), # Be
             5:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # B
             6:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # C
             7:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # N
             8:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # O
             9:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # F
             10:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ne
             11:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Na
             12:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Mg
             13:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Al
             14:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Si
             15:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # p
             16:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # S
             17:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Cl
             18:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ar
             19:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # K
             20:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ca 
             42:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Mo  
             83:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Bi
             32:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Ge  
             34:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Se 
             24:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Cr 
             53:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # I   
             82:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # pb
             55:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Cs
             33:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # As
             31:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Ga
             80:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Hg
             Element['V'].Z: np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # V
             Element['Sb'].Z: np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Sb
             }

basis_def_26 = (lambda s1=[0],s2=[1],s3=[2],p1=[3,4,5],p2=[6,7,8],d1=[9,10,11,12,13],d2=[14,15,16,17,18],f1=[19,20,21,22,23,24,25]: {
    Element['H'].Z : np.array(s1+s2+p1, dtype=int), # H6.0-s2p1
    Element['He'].Z : np.array(s1+s2+p1, dtype=int), # He8.0-s2p1
    Element['Li'].Z : np.array(s1+s2+s3+p1+p2, dtype=int), # Li8.0-s3p2
    Element['Be'].Z : np.array(s1+s2+p1+p2, dtype=int), # Be7.0-s2p2
    Element['B'].Z : np.array(s1+s2+p1+p2+d1, dtype=int), # B7.0-s2p2d1
    Element['C'].Z : np.array(s1+s2+p1+p2+d1, dtype=int), # C6.0-s2p2d1
    Element['N'].Z : np.array(s1+s2+p1+p2+d1, dtype=int), # N6.0-s2p2d1
    Element['O'].Z : np.array(s1+s2+p1+p2+d1, dtype=int), # O6.0-s2p2d1
    Element['F'].Z : np.array(s1+s2+p1+p2+d1, dtype=int), # F6.0-s2p2d1
    Element['Ne'].Z: np.array(s1+s2+p1+p2+d1, dtype=int), # Ne9.0-s2p2d1
    Element['Na'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Na9.0-s3p2d1
    Element['Mg'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Mg9.0-s3p2d1
    Element['Al'].Z: np.array(s1+s2+p1+p2+d1, dtype=int), # Al7.0-s2p2d1
    Element['Si'].Z: np.array(s1+s2+p1+p2+d1, dtype=int), # Si7.0-s2p2d1
    Element['P'].Z: np.array(s1+s2+p1+p2+d1, dtype=int), # P7.0-s2p2d1
    Element['S'].Z: np.array(s1+s2+p1+p2+d1, dtype=int), # S7.0-s2p2d1
    Element['Cl'].Z: np.array(s1+s2+p1+p2+d1, dtype=int), # Cl7.0-s2p2d1
    Element['Ar'].Z: np.array(s1+s2+p1+p2+d1, dtype=int), # Ar9.0-s2p2d1
    Element['K'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # K10.0-s3p2d1
    Element['Ca'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Ca9.0-s3p2d1
    Element['Sc'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Sc9.0-s3p2d1
    Element['Ti'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Ti7.0-s3p2d1
    Element['V'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # V6.0-s3p2d1
    Element['Cr'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Cr6.0-s3p2d1
    Element['Mn'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Mn6.0-s3p2d1
    Element['Fe'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Fe5.5H-s3p2d1
    Element['Co'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Co6.0H-s3p2d1
    Element['Ni'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Ni6.0H-s3p2d1
    Element['Cu'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Cu6.0H-s3p2d1
    Element['Zn'].Z: np.array(s1+s2+s3+p1+p2+d1, dtype=int), # Zn6.0H-s3p2d1
    Element['Ga'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Ga7.0-s3p2d2
    Element['Ge'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Ge7.0-s3p2d2
    Element['As'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # As7.0-s3p2d2
    Element['Se'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Se7.0-s3p2d2
    Element['Br'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Br7.0-s3p2d2
    Element['Kr'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Kr10.0-s3p2d2
    Element['Rb'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Rb11.0-s3p2d2
    Element['Sr'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Sr10.0-s3p2d2
    Element['Y'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Y10.0-s3p2d2
    Element['Zr'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Zr7.0-s3p2d2
    Element['Nb'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Nb7.0-s3p2d2
    Element['Mo'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Mo7.0-s3p2d2
    Element['Tc'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Tc7.0-s3p2d2
    Element['Ru'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Ru7.0-s3p2d2
    Element['Rh'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Rh7.0-s3p2d2
    Element['Pd'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Pd7.0-s3p2d2
    Element['Ag'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Ag7.0-s3p2d2
    Element['Cd'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Cd7.0-s3p2d2
    Element['In'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # In7.0-s3p2d2
    Element['Sn'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Sn7.0-s3p2d2
    Element['Sb'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Sb7.0-s3p2d2
    Element['Te'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Te7.0-s3p2d2f1
    Element['I'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # I7.0-s3p2d2f1
    Element['Xe'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Xe11.0-s3p2d2
    Element['Cs'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Cs12.0-s3p2d2
    Element['Ba'].Z: np.array(s1+s2+s3+p1+p2+d1+d2, dtype=int), # Ba10.0-s3p2d2
    Element['La'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # La8.0-s3p2d2f1
    Element['Ce'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Ce8.0-s3p2d2f1
    Element['Pr'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Pr8.0-s3p2d2f1
    Element['Nd'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Nd8.0-s3p2d2f1
    Element['Pm'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Pm8.0-s3p2d2f1
    Element['Sm'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Sm8.0-s3p2d2f1
    Element['Dy'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Dy8.0-s3p2d2f1
    Element['Ho'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Ho8.0-s3p2d2f1
    Element['Lu'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Lu8.0-s3p2d2f1
    Element['Hf'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Hf9.0-s3p2d2f1
    Element['Ta'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Ta7.0-s3p2d2f1
    Element['W'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # W7.0-s3p2d2f1
    Element['Re'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Re7.0-s3p2d2f1
    Element['Os'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Os7.0-s3p2d2f1
    Element['Ir'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Ir7.0-s3p2d2f1
    Element['Pt'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Pt7.0-s3p2d2f1
    Element['Au'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Au7.0-s3p2d2f1
    Element['Hg'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Hg8.0-s3p2d2f1
    Element['Tl'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Tl8.0-s3p2d2f1
    Element['Pb'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Pb8.0-s3p2d2f1
    Element['Bi'].Z: np.array(s1+s2+s3+p1+p2+d1+d2+f1, dtype=int), # Bi8.0-s3p2d2f1 
})()

basis_def_19_siesta = {55:np.array([0,1,4,5,3], dtype=int), # Cs
             51:np.array([0,1,4,5,3,7,8,6,11,13,9,12,10], dtype=int), # Sb
             47:np.array([0,1,11,13,9,12,10,16,18,14,17,15,4,5,3], dtype=int), # Ag
             17:np.array([0,1,4,5,3,7,8,6,11,13,9,12,10], dtype=int), # Cl
             14:np.array([0,1,4,5,3,7,8,6,11,13,9,12,10], dtype=int) # Si
             }

# Warning: this dict is not complete!!!
basis_def_14 = {1:np.array([0,1,3,4,5], dtype=int), # H
             2:np.array([0,1,3,4,5], dtype=int), # He
             3:np.array([0,1,2,3,4,5,6,7,8], dtype=int), # Li
             4:np.array([0,1,3,4,5,6,7,8], dtype=int), # Be
             5:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # B
             6:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # C
             7:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # N
             8:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # O
             9:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # F
             10:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ne
             11:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Na
             12:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Mg
             13:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Al
             14:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Si
             15:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # p
             16:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # S
             17:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Cl
             18:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ar
             19:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # K
             20:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ca 
             Element['V'].Z: np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # V
             }

# Warning: this dict is not complete!!!
# num_valence = {1:1,2:2,3:3,4:2,5:3,6:4,7:5,8:6,9:7,10:8,11:9,12:8,13:3,14:4,15:5,16:6,17:7,18:8,19:9,20:10,42:14,83:15,34:6,
#                35:7,55:9,82:14,53:7,33:15,31:13,32:4,Element['V'].Z:13, Element['Sb'].Z:15}

# This dict is complete
num_valence = {
    Element['H'].Z: 1,
    Element['He'].Z: 2,
    Element['Li'].Z: 3,
    Element['Be'].Z: 2,
    Element['B'].Z: 3,
    Element['C'].Z: 4,
    Element['N'].Z: 5,
    Element['O'].Z: 6,
    Element['F'].Z: 7,
    Element['Ne'].Z: 8,
    Element['Na'].Z: 9,
    Element['Mg'].Z: 8,
    Element['Al'].Z: 3,
    Element['Si'].Z: 4,
    Element['P'].Z: 5,
    Element['S'].Z: 6,
    Element['Cl'].Z: 7,
    Element['Ar'].Z: 8,
    Element['K'].Z: 9,
    Element['Ca'].Z: 10,
    Element['Sc'].Z: 11,
    Element['Ti'].Z: 12,
    Element['V'].Z: 13,
    Element['Cr'].Z: 14,
    Element['Mn'].Z: 15,
    Element['Fe'].Z: 16,
    Element['Co'].Z: 17,
    Element['Ni'].Z: 18,
    Element['Cu'].Z: 19,
    Element['Zn'].Z: 20,
    Element['Ga'].Z: 13,
    Element['Ge'].Z: 4,
    Element['As'].Z: 15,
    Element['Se'].Z: 6,
    Element['Br'].Z: 7,
    Element['Kr'].Z: 8,
    Element['Rb'].Z: 9,
    Element['Sr'].Z: 10,
    Element['Y'].Z: 11,
    Element['Zr'].Z: 12,
    Element['Nb'].Z: 13,
    Element['Mo'].Z: 14,
    Element['Tc'].Z: 15,
    Element['Ru'].Z: 14,
    Element['Rh'].Z: 15,
    Element['Pd'].Z: 16,
    Element['Ag'].Z: 17,
    Element['Cd'].Z: 12,
    Element['In'].Z: 13,
    Element['Sn'].Z: 14,
    Element['Sb'].Z: 15,
    Element['Te'].Z: 16,
    Element['I'].Z: 7,
    Element['Xe'].Z: 8,
    Element['Cs'].Z: 9,
    Element['Ba'].Z: 10,
    Element['La'].Z: 11,
    Element['Ce'].Z: 12,
    Element['Pr'].Z: 13,
    Element['Nd'].Z: 14,
    Element['Pm'].Z: 15,
    Element['Sm'].Z: 16,
    Element['Dy'].Z: 20,
    Element['Ho'].Z: 21,
    Element['Lu'].Z: 11,
    Element['Hf'].Z: 12,
    Element['Ta'].Z: 13,
    Element['W'].Z: 12,
    Element['Re'].Z: 15,
    Element['Os'].Z: 14,
    Element['Ir'].Z: 15,
    Element['Pt'].Z: 16,
    Element['Au'].Z: 17,
    Element['Hg'].Z: 18,
    Element['Tl'].Z: 19,
    Element['Pb'].Z: 14,
    Element['Bi'].Z: 15
}

num_val = np.zeros((99,), dtype=int)
for k in num_valence.keys():
    num_val[k] = num_valence[k]

au2ang = 0.5291772490000065
au2ev = 27.211324570273
pattern_eng = re.compile(r'Enpy  =(\W+)(\-\d+\.?\d*)')
pattern_md = re.compile(r'MD= 1  SCF=(\W*)(\d+)')
pattern_latt = re.compile(r'<Atoms.UnitVectors.+?\s+(\-?\d+\.?\d+)\s+(\-?\d+\.?\d+)\s+(\-?\d+\.?\d+)\s+(\-?\d+\.?\d+)\s+(\-?\d+\.?\d+)\s+(\-?\d+\.?\d+)\s+(\-?\d+\.?\d+)\s+(\-?\d+\.?\d+)\s+(\-?\d+\.?\d+)\s+Atoms.UnitVectors>')
pattern_coor = re.compile(r'\s+\d+\s+(\w+)\s+(\-?\d+\.?\d+)\s+(\-?\d+\.?\d+)\s+(\-?\d+\.?\d+)\s+\-?\d+\.?\d+\s+\-?\d+\.?\d+')
num = r'-?\d+\.?\d*'
wht = r'\s+'
pattern_eng_siesta = re.compile(r'siesta: Etot\s+=\s+(\-\d+\.?\d*)')
pattern_md_siesta = re.compile(r'scf:\s+(\d+)')
pattern_latt_siesta = re.compile(r'%block LatticeVectors.*' + f'{wht}({num}){wht}({num}){wht}({num}){wht}({num}){wht}({num}){wht}({num}){wht}({num}){wht}({num}){wht}({num})' + r'\s+%endblock LatticeVectors')
pattern_cblk_siesta = re.compile(r'%block AtomicCoordinatesAndAtomicSpecies(.+)%endblock AtomicCoordinatesAndAtomicSpecies', flags=re.S)
pattern_coor_siesta = re.compile(f'{wht}({num}){wht}({num}){wht}({num}){wht}(\d+)')
pattern_sblk_siesta = re.compile(r'%block ChemicalSpeciesLabel(.+)%endblock ChemicalSpeciesLabel', flags=re.S)
pattern_spec_siesta = re.compile(r'\s+(\d+)\s+(\d+)\s+(\w+)')

# default values
max_SCF_skip = 200
device = 'cpu'

def read_openmx_dat(filename: str = None):

    with open(filename,'r') as f:
        content = f.read()
        speciesAndCoordinates = pattern_coor.findall((content).strip())
        latt = pattern_latt.findall((content).strip())[0]
        latt = np.array([float(var) for var in latt]).reshape(-1, 3)/au2ang    
        species = []
        coordinates = []
        for item in speciesAndCoordinates:
            species.append(item[0])
            coordinates += item[1:]
        atomic_numbers = np.array([Element[s].Z for s in species])
        coordinates = np.array([float(pos) for pos in coordinates]).reshape(-1, 3)/au2ang
    
    return atomic_numbers, latt, coordinates
    
