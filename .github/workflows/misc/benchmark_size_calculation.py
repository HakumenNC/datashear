"""
Benchmark pour comparer les différentes méthodes de calcul de taille de ligne CSV.
"""

import time
import csv
import io
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from datashear.util import Util

def method_1_original(row):
    """Méthode originale : nouveau buffer à chaque fois"""
    row_buffer = io.StringIO()
    row_writer = csv.writer(row_buffer)
    row_writer.writerow(row)
    return len(row_buffer.getvalue().encode('utf-8'))

def method_2_reused_buffer(row, buffer, writer):
    """Méthode optimisée : réutiliser le buffer"""
    buffer.seek(0)
    buffer.truncate(0)
    writer.writerow(row)
    return len(buffer.getvalue().encode('utf-8'))

def method_3_util_function(row, buffer, writer):
    """Méthode avec fonction utilitaire"""
    return Util.get_row_size(row, buffer, writer)

def method_4_approximation(row):
    """Méthode par approximation simple"""
    # Simple approximation - rapide mais moins précise
    return len(','.join(str(field) for field in row).encode('utf-8')) + 2

def benchmark_methods():
    # Données de test
    test_rows = [
        ['1', 'John', 'Doe', 'john@example.com'],
        ['2', 'Jane', 'Smith', 'jane@example.com'],
        ['3', 'Bob', 'Johnson', 'bob@example.com'],
        ['4', 'Alice', 'Williams', 'alice@example.com'],
        ['5', 'Charlie', 'Brown', 'charlie@example.com'],
        ['6', 'Diana', 'Davis', 'diana@example.com'],
        ['7', 'Edward', 'Miller', 'edward@example.com'],
        ['8', 'Fiona', 'Wilson', 'fiona@example.com'],
        ['9', 'George', 'Moore', 'george@example.com'],
        ['10', 'Helen', 'Taylor', 'helen@example.com']
    ]
    
    # Répéter les données pour avoir plus de lignes à traiter
    test_rows = test_rows * 1000  # 10,000 lignes
    
    print(f"Benchmark avec {len(test_rows)} lignes")
    print("=" * 50)
    
    # Buffer réutilisable pour les méthodes optimisées
    reused_buffer = io.StringIO()
    reused_writer = csv.writer(reused_buffer)
    
    # Méthode 1: Originale
    start_time = time.time()
    sizes_1 = [method_1_original(row) for row in test_rows]
    time_1 = time.time() - start_time
    print(f"Méthode 1 (originale):        {time_1:.4f}s")
    
    # Méthode 2: Buffer réutilisé
    start_time = time.time()
    sizes_2 = [method_2_reused_buffer(row, reused_buffer, reused_writer) for row in test_rows]
    time_2 = time.time() - start_time
    print(f"Méthode 2 (buffer réutilisé): {time_2:.4f}s")
    
    # Méthode 3: Fonction utilitaire
    start_time = time.time()
    sizes_3 = [method_3_util_function(row, reused_buffer, reused_writer) for row in test_rows]
    time_3 = time.time() - start_time
    print(f"Méthode 3 (fonction util):    {time_3:.4f}s")
    
    # Méthode 4: Approximation
    start_time = time.time()
    sizes_4 = [method_4_approximation(row) for row in test_rows]
    time_4 = time.time() - start_time
    print(f"Méthode 4 (approximation):    {time_4:.4f}s")
    
    print("\nAméliorations par rapport à la méthode originale:")
    print(f"Méthode 2: {time_1/time_2:.2f}x plus rapide")
    print(f"Méthode 3: {time_1/time_3:.2f}x plus rapide")
    print(f"Méthode 4: {time_1/time_4:.2f}x plus rapide")
    
    # Vérifier que toutes les méthodes donnent les mêmes résultats (sauf approximation)
    print(f"\nVérification de précision:")
    print(f"Méthode 1 vs 2: {'✓' if sizes_1 == sizes_2 else '✗'}")
    print(f"Méthode 1 vs 3: {'✓' if sizes_1 == sizes_3 else '✗'}")
    print(f"Méthode 1 vs 4: {'✓' if sizes_1 == sizes_4 else '✗ (approximation)'}")
    
    # Montrer quelques exemples de différence avec l'approximation
    print(f"\nExemples de tailles (premières lignes):")
    for i in range(min(3, len(test_rows))):
        print(f"Ligne {i+1}: Précise={sizes_1[i]}, Approximation={sizes_4[i]} (diff: {abs(sizes_1[i]-sizes_4[i])})")

if __name__ == "__main__":
    benchmark_methods()