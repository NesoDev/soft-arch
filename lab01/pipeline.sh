#!/bin/bash

DATA_FILE="profiles.csv"

echo "Cantidad de varones y mujeres:"
awk -F, '{if ($4 == "Male") varones++ ; else if ($4 == "Female") mujeres++} END {print "Varones -> ", varones, "Mujeres -> ", mujeres}' "$DATA_FILE"

echo -e "\nCantidad de alumnos por Escuela Profesional:"
awk -F, '{escuelas[$9]++} END {for (escuela in escuelas) print escuela " -> " escuelas[escuela]}' "$DATA_FILE"

echo -e "\nPromedio de edad:"
awk -F, '{total += $3; count++} END {if (count > 0) print "Promedio de edad -> ", total/count; else print "No hay datos"}' "$DATA_FILE"

echo -e "\nCantidad de personas que ingresaron a la Universidad desde el 1/1/2021:"
awk -F, '{if ($10 >= "2021-01-01") count++} END {print "Cantidad de ingresantes -> ", count}' "$DATA_FILE"