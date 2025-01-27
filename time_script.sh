#!/bin/bash

# Output bestand
output_file="results_table.txt"
echo "Generating results, this may take some time..."

# Header van de tabel
echo -e "Sorting method\tNetlist\tLowest cost\tTime (s)\t%" > $output_file

# Parameterwaarden
netlists=(1 2 3 4 5 6 7 8 9)
algorithms=("m" "d" "l" "a")
sorting_methods=("r" "b" "d" "q")

# Itereer over alle combinaties
for netlist in "${netlists[@]}"; do
    for algorithm in "${algorithms[@]}"; do
        for sorting_method in "${sorting_methods[@]}"; do

            # Prompt gebruiker voor aantal iteraties
            iterations=250
            
            # Start het Python-script en sla de output op
            echo "Running: Netlit $netlist | Algorithm $algorithm | Sorting $sorting_method"
            python3 main.py << EOF > temp_output.txt
$iterations
$netlist
$algorithm
$sorting_method
EOF

            # Verwerk de output
            best_cost=$(grep "The grid with minimal cost costs:" temp_output.txt | awk '{print $7}')
            total_time=$(grep "Total time for" temp_output.txt | awk '{print $6}')
            success_rate=$(grep "% of the grids were successful" temp_output.txt | awk '{print $1}')

            # Voeg resultaten toe aan de tabel
            echo -e "$sorting_method\t$netlist\t$best_cost\t$total_time\t$success_rate" >> $output_file

        done
    done
done

# Opruimen
rm temp_output.txt

echo "Results saved to $output_file"
