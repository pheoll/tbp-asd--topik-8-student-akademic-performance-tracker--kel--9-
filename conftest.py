"""
conftest.py — letakkan file ini di ROOT repository
(sejajar dengan src/, tests/, README.md)
 
Berfungsi agar pytest bisa menemukan semua module dari tests/.
"""
import sys
import os
 
# ROOT = folder tempat conftest.py ini berada
ROOT = os.path.dirname(os.path.abspath(__file__))
 
sys.path.insert(0, os.path.join(ROOT, 'src'))
sys.path.insert(0, os.path.join(ROOT, 'src', 'data_structures'))
sys.path.insert(0, os.path.join(ROOT, 'src', 'modules'))
 
 