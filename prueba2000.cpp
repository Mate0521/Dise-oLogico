#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <cmath>

using namespace std;

int main() {
    string vec[5000], num;
    stringstream ss;
    int base, cont = 0, co;
    long long valorDecimal = 0;

    // Generar tabla de caracteres hasta 5000
    for (int i = 0; i < 5000; i++) {
        if (i <= 9) {
            vec[i] = '0' + i;
        } else if (i < 68) {
            vec[i] = 'A' + (i - 10);
        } else {
            for (int j = 0; j < 68 && i < 5000; j++, i++) {
                ss.str("");
                ss.clear();
                ss << (i - 68);
                vec[i] = string(1, 'A' + j) + ss.str();
            }
        }
    }

    // Preguntar por un caracter en la tabla
    int caracter;
    cout << "Digite cual caracter quieres saber: ";
    cin >> caracter;
    if (caracter >= 0 && caracter < 5000) {
        cout << "Caracter en la tabla [" << caracter << "]: " << vec[caracter] << endl;
    } else {
        cout << "Numero fuera de rango (0-4999)" << endl;
    }

    // Entrada de número y base
    cout << "Digite el numero a describir y en que base se encuentra:" << endl;
    cout << "Numero: ";
    cin >> num;
    cout << "Base en que se encuentra: ";
    cin >> base;

    // Guardar cada dígito en el vector `tec`
    vector<string> tec;
    for (int i = 0; i < num.length(); i++) {
        tec.push_back(string(1, num[i]));
        cont++;
    }

    // Mostrar los dígitos almacenados
    cout << "Digitos almacenados en el vector:" << endl;
    for (int i = 0; i < tec.size(); i++) {
        cout << "Posición " << i << " -> " << tec[i] << endl;
    }

    // Convertir el número a base 10
    vector<long long> bases(cont, -1);
    for (int i = 0; i < cont; i++) {
        for (int j = 0; j < base; j++) {
            if (tec[i] == vec[j]) {
                bases[i] = j;
                cout << "base[" << i << "]: " << bases[i] << endl;
                break;
            }
        }
    }

    co = cont;
    long long sumaTotal = 0;
    for (int i = 0; i < cont; i++) {
        co--;
        long long sumaParcial = bases[i] * static_cast<long long>(powl(base, co));
        cout << "Suma parcial: " << sumaParcial << endl;
        sumaTotal += sumaParcial;
    }

    cout << "Suma en base 10: " << sumaTotal << endl;

    // Convertir a otra base
    long long nuevaBase;
    vector<string> resultado;

    cout << "Base a convertir: ";
    cin >> nuevaBase;

    long long temp = sumaTotal;
    if (temp == 0) {
        resultado.push_back("0");
    } else {
        while (temp > 0) {
            int residuo = temp % nuevaBase;
            resultado.push_back(vec[residuo]);
            temp /= nuevaBase;
        }
    }

    // Mostrar los residuos almacenados en el vector
    cout << "Residuos almacenados en el vector:" << endl;
    for (int i = resultado.size() - 1; i >= 0; i--) {
        cout << resultado[i] << " ";
    }
    cout << endl;

    return 0;
}


