#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'

int main() { _

    double v;
    cin >> v;

    // Problema de arredondamento, entao multiplicar por 100 e tirar float
    int valor = round(v * 100);

    int notas[] = {10000, 5000, 2000, 1000, 500, 200};
    int moedas[] = {100, 50, 25, 10, 5, 1};

    cout << "NOTAS:" << endl;
    for (int i = 0; i < 6; i++) {
        int qtd = valor / notas[i];
        cout << qtd << " nota(s) de R$ " << notas[i] / 100 << ".00" << endl;
        valor %= notas[i];
    }

    cout << "MOEDAS:" << endl;
    for (int i = 0; i < 6; i++) {
        int qtd = valor / moedas[i];
        cout << qtd << " moeda(s) de R$ " << fixed << setprecision(2) << moedas[i] / 100.0 << endl;
        valor %= moedas[i];
    }

    return 0;
}
