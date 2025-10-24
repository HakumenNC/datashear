"""
Script de test manuel pour la méthode by_rows
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from datashear.core import Splitter


def test_manual():
    """Test manuel de la méthode by_rows"""
    
    # Chemin vers le fichier de test
    input_file = os.path.join(os.path.dirname(__file__), 'input/MOCK_DATA_sm.csv')
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    
    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    # Nettoyer le répertoire de sortie
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    print(f"📁 Fichier d'entrée: {input_file}")
    print(f"📁 Répertoire de sortie: {output_dir}")
    
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(input_file):
        print(f"❌ Le fichier d'entrée n'existe pas: {input_file}")
        return
    
    # Afficher des informations sur le fichier d'entrée
    with open(input_file, 'r') as f:
        lines = f.readlines()
        total_lines = len(lines)
        data_lines = total_lines - 1  # Moins l'en-tête
    print(f"📊 Fichier d'entrée: {total_lines} lignes totales ({data_lines} lignes de données)")
    
    # Test 1: Division en fichiers de 5 lignes avec en-têtes
    print("\n🔧 Test 1: Division en fichiers de 5 lignes (avec en-têtes)")
    splitter1 = Splitter(
        input_file=input_file,
        output_dir=output_dir,
        output_prefix="test1",
        output_sufix="with_header"
    )
    
    try:
        splitter1.by_rows(5, repeat_header=True)
        print("✅ Test 1 réussi!")
        
        # Lister les fichiers créés
        files = [f for f in os.listdir(output_dir) if f.startswith("test1")]
        print(f"📄 Fichiers créés: {len(files)}")
        for file in sorted(files):
            file_path = os.path.join(output_dir, file)
            with open(file_path, 'r') as f:
                line_count = len(f.readlines())
            print(f"   - {file} ({line_count} lignes)")
            
    except Exception as e:
        print(f"❌ Test 1 échoué: {e}")
    
    # Test 2: Division en fichiers de 3 lignes sans en-têtes
    print("\n🔧 Test 2: Division en fichiers de 3 lignes (sans en-têtes)")
    splitter2 = Splitter(
        input_file=input_file,
        output_dir=output_dir,
        output_prefix="test2",
        output_sufix="no_header"
    )
    
    try:
        splitter2.by_rows(3, repeat_header=False)
        print("✅ Test 2 réussi!")
        
        files = [f for f in os.listdir(output_dir) if f.startswith("test2")]
        print(f"📄 Fichiers créés: {len(files)}")
        for file in sorted(files):
            file_path = os.path.join(output_dir, file)
            with open(file_path, 'r') as f:
                line_count = len(f.readlines())
            print(f"   - {file} ({line_count} lignes)")
            
    except Exception as e:
        print(f"❌ Test 2 échoué: {e}")
    
    # Test 3: Test avec erreur (0 lignes)
    print("\n🔧 Test 3: Test de gestion d'erreur (0 lignes)")
    splitter3 = Splitter(input_file, output_dir)
    
    try:
        splitter3.by_rows(0)
        print("❌ Test 3 échoué: devrait lever une exception!")
    except ValueError as e:
        print(f"✅ Test 3 réussi: {e}")
    except Exception as e:
        print(f"❌ Test 3 échoué avec erreur inattendue: {e}")
    
    print("\n📊 Résumé des fichiers dans le répertoire de sortie:")
    all_files = os.listdir(output_dir)
    for file in sorted(all_files):
        file_path = os.path.join(output_dir, file)
        size = os.path.getsize(file_path)
        print(f"   📄 {file} ({size} bytes)")


if __name__ == "__main__":
    print("🚀 Démarrage des tests manuels pour by_rows()")
    test_manual()
    print("\n✨ Tests terminés!")