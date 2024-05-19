kriteria = [
    ["Kode", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"],
    ["A1", 1.10, 3.12, 3.89, 4.20, 2.21, 1.03, 3.00, 5.00],
    ["A2", 3.05, 3.98, 2.96, 3.02, 4.10, 2.99, 1.10, 4.03],
    ["A3", 1.90, 4.95, 3.01, 2.90, 4.95, 4.06, 5.00, 1.10],
    ["A4", 2.85, 3.87, 3.12, 1.05, 2.93, 4.89, 3.30, 4.90],
    ["A5", 4.77, 3.00, 4.87, 3.01, 1.97, 3.99, 2.04, 4.00]
]

alternative_names = {
    "A1": "Bahtiar, SH",
    "A2": "Kasim Pohan, SH",
    "A3": "Nur Ainun",
    "A4": "Rocky Sirait, SH",
    "A5": "Uock Yontha, SH"
}

bobot = [
    ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"],
    [0.178, 0.284, 0.207, 0.100, 0.057, 0.064, 0.044, 0.066]
]
print()
print("Penentu pemilihan jaksa terbaik di Pengadilan Negeri Medan")
print()
# Tahap 1: Pembentukan matriks keputusan (X)
def print_matrix(matrix):
    col_widths = [max(len(str(item)) for item in col) for col in zip(*matrix)]
    total_width = sum(col_widths) + len(matrix[0]) * 3 + 1  

    print("┌" + "─" * total_width + "┐")

    for row in matrix:
        print("│", end="")
        for i, item in enumerate(row):
            if i < len(col_widths):
                print(f" {str(item):<{col_widths[i]}} │", end="")
            else:
                print(f" {str(item):<10} │", end="")
        print()

        print("├" + "─" * total_width + "┤")
    
    print("└" + "─" * total_width + "┘")

print("Tahap 1: Pembentukan matriks keputusan (X)")
print_matrix(kriteria)
print()


# Tahap 2: Normalisasi matriks keputusan (X)
min_values = [min(row[i] for row in kriteria[1:]) for i in range(1, len(kriteria[0]))]
max_values = [max(row[i] for row in kriteria[1:]) for i in range(1, len(kriteria[0]))]

normalized_kriteria = [kriteria[0]]  
for row in kriteria[1:]:
    normalized_row = [row[0]] + [round((row[i] - min_values[i - 1]) / (max_values[i - 1] - min_values[i - 1]), 3) for i in range(1, len(row))]
    normalized_kriteria.append(normalized_row)

print("Tahap 2: Matriks Keputusan (X) Setelah Normalisasi:")
print_matrix(normalized_kriteria)
print()


# Tahap 3: Perhitungan elemen matriks tertimbang (V)
weighted_matrix = [kriteria[0]] 
for row in normalized_kriteria[1:]:
    weighted_row = [row[0]] + [round(row[i] * bobot[1][i-1] + bobot[1][i-1], 3) for i in range(1, len(row))]  
    weighted_matrix.append(weighted_row)

print("Tahap 3: Perhitungan Elemen Matriks Tertimbang (V):")
print_matrix(weighted_matrix)
print()


# Tahap 4: Matriks Area Perkiraan Batas (G)
G = ["G"]
for i in range(1, len(weighted_matrix[0])):
    column_values = [row[i] for row in weighted_matrix[1:]]
    product = 1
    for value in column_values:
        product *= value
    result = round((product ** (1/5)), 3) 
    G.append(result)

print("Tahap 4: Matriks Area Perkiraan Batas (G):")
print("┌" + "─" * 68 + "┐")
print("│", end="")
for i, val in enumerate(G[1:], start=1):
    print(f" {'C'+str(i):<8}", end="")
print("│")
print("├" + "─" * 68 + "┤")
print("│", end="")
for val in G[1:]:
    print(f" {val:<8.3f}", end="")
print("│")
print("└" + "─" * 68 + "┘")


# Tahap 5: Perhitungan matriks jarak elemen alternatif dari batas perkiraan daerah (Q)
Q = [["Alternatif"] + weighted_matrix[0][1:]]  

for i in range(1, len(weighted_matrix)):
    Q_row = [weighted_matrix[i][0]]  
    for j in range(1, len(weighted_matrix[i])):
        Q_value = round((weighted_matrix[i][j] - G[j]), 3) 
        Q_row.append(Q_value)
    Q.append(Q_row)

print()
print("Tahap 5: Matriks Jarak (Q):")
print("┌" + "─" * (11 + 8 * (len(weighted_matrix[0])-1)) + "┐")
print("│", end="")
for i, val in enumerate(Q[0][1:], start=1):
    print(f" {'C'+str(i):<8}│", end="")
print("\n├" + "─" * (11 + 8 * (len(weighted_matrix[0])-1)) + "┤")
for row in Q[1:]:
    print("│", end="")
    for val in row[1:]:
        print(f" {val:<8.3f}│", end="")
    print("\n├" + "─" * (11 + 8 * (len(weighted_matrix[0])-1)) + "┤")
print("└" + "─" * (11 + 8 * (len(weighted_matrix[0])-1)) + "┘")


# Tahap 6: Perangkingan alternatif
ranking_scores = {}  
S_scores = []  

for row in Q[1:]:
    alternative = row[0]
    score = sum(row[1:])  
    ranking_scores[alternative] = score
    S_scores.append(score)

print("Sebelum Perangkingan")
print("┌─────────────┬──────────────────────┬──────────┐")
print("│ Kode        │ Nama Alternatif      │ S        │")
print("├─────────────┼──────────────────────┼──────────┤")
sorted_ranking = sorted(ranking_scores.items(), key=lambda x: x[0])  
for alternative, score in sorted_ranking:
    name = alternative_names.get(alternative, "N/A")
    print(f"│ {alternative:<11} │ {name:<20} │ {score:<8.3f} │")  
print("└─────────────┴──────────────────────┴──────────┘")

sorted_S = sorted(ranking_scores.items(), key=lambda x: x[1], reverse=True)

print("\nTabel Perangkingan Alternatif:")
print("┌─────────────┬──────────────────────┬──────────┐")
print("│ Alternatif  │  Nama Alternatif     │  Score   │")
print("├─────────────┼──────────────────────┼──────────┤")
for rank, (alternative, score) in enumerate(sorted_S, start=1):
    name = alternative_names.get(alternative, "N/A")
    print(f"│ {alternative:<11} │ {name:<20} │ {score:<8.3f} │")
print("└─────────────┴──────────────────────┴──────────┘")

best_alternative = sorted_S[0][0]
worst_alternative = sorted_S[-1][0]
print()
print(f"Kesimpulan:")
print(f"Rank pertama: {best_alternative} atas nama {alternative_names[best_alternative]}")
print(f"Rank terakhir: {worst_alternative} atas nama {alternative_names[worst_alternative]}")
print(f"Jadi, pemilihan jaksa terbaik adalah alternatif {best_alternative}.")