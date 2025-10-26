"""
Test avec des données CSV complexes contenant des caractères spéciaux.
"""

import csv
import io
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from datashear.util import Util

def compare_methods_complex_data():
    # Données complexes avec caractères spéciaux, virgules, guillemets
    complex_rows = [
        ['1', 'John "Johnny" Doe', 'CEO, Manager', 'john@company,com'],
        ['2', 'Jane\nSmith', 'Developer\nSenior', 'jane@example.com'],
        ['3', 'Bob,Johnson', 'Sales, Marketing', 'bob@test.org'],
        ['4', 'Alice "Wonder" Wilson', 'HR, "People Manager"', 'alice@hr.com'],
        ['5', 'Émile François', 'Développeur', 'emile@société.fr'],
        ['6', 'María José', 'Diseñadora', 'maria@empresa.es']
    ]
    
    # Buffer réutilisable
    reused_buffer = io.StringIO()
    reused_writer = csv.writer(reused_buffer)
    
    print("Comparaison avec données complexes:")
    print("=" * 60)
    
    for i, row in enumerate(complex_rows, 1):
        # Méthode précise (CSV writer)
        reused_buffer.seek(0)
        reused_buffer.truncate(0)
        reused_writer.writerow(row)
        precise_size = len(reused_buffer.getvalue().encode('utf-8'))
        
        # Méthode approximation
        approx_size = len(','.join(str(field) for field in row).encode('utf-8')) + 2
        
        # Fonction utilitaire
        util_size = Util.get_row_size(row, reused_buffer, reused_writer)
        
        print(f"Ligne {i}:")
        print(f"  Données: {row}")
        print(f"  Précise:      {precise_size} bytes")
        print(f"  Utilitaire:   {util_size} bytes")
        print(f"  Approximation: {approx_size} bytes")
        print(f"  Différence:   {abs(precise_size - approx_size)} bytes")
        
        # Montrer le CSV généré vs approximation
        reused_buffer.seek(0)
        reused_buffer.truncate(0)
        reused_writer.writerow(row)
        csv_output = reused_buffer.getvalue()
        approx_output = ','.join(str(field) for field in row) + '\r\n'
        
        print(f"  CSV réel:     {repr(csv_output)}")
        print(f"  Approximation: {repr(approx_output)}")
        print(f"  Identique:    {'✓' if csv_output == approx_output else '✗'}")
        print()

if __name__ == "__main__":
    compare_methods_complex_data()