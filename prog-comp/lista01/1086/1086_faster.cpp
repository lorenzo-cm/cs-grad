#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

int check_orientation(int tam1, int tam2, int l, unordered_map<int, int> freq){
    // Tentar com mapa de frequencia para reduzir tamanho do vetor e ser mais rapido
    // Ainda nao foi, tentarei fazer da seguinte forma para chamar menos funcoes:
    // Tento todos as tabuas que enfileiram exatamente
    // Depois itero sobre o resto
    
    if(tam1 % l != 0){
        return 0;
    }

    int rows = tam1 / l;
    int row_size = tam2;
    int total_usado = 0;


    int tabuas_exatas = freq[row_size];
    int tabuas_exatas_usadas = min(rows, tabuas_exatas);
    
    total_usado += tabuas_exatas_usadas;

    freq[row_size] -= tabuas_exatas_usadas;
    rows -= tabuas_exatas_usadas;


    // Itero sobre as linhas restantes que nao puderam ser resolvidas com uma tabua exatamente

    // Filtrar novamente por tabuas menores que o tamanho do salao, mas agora consigo filtrar por uma dimensao somente
    // Reduz quantidade de tabuas
    int pares_count = 0;
    vector<int> keys;
    for(auto &p : freq) {
        int key = p.first;
        if(key <= row_size) {
            keys.push_back(key);
        }
    }
    
    for (int a : keys) {
        int b = row_size - a;
        if (b < a) continue; // evitar contar duas vezes
        if(freq.find(b) == freq.end()) continue; // elemento b nao existe

        if(a < b) {
            pares_count += min(freq[a], freq[b]); // aproveitar o par que deu certo
        } else { 
            // caso em que sao iguais
            pares_count += freq[a] / 2;
        }
    }
    
    // n deu
    if(pares_count < rows) return 0;
    
    // Acrescentar o par de tabuas utilizadas
    total_usado += 2 * rows;

    return total_usado;
}

int check_fit(int m, int n, int l, unordered_map<int, int> freq){
    // primeira orientacao
    int result1 = INF;
    if (m % l == 0){
        result1 = check_orientation(m, n, l, freq);
        if(result1 == 0){
            result1 = INF;
        }
    }

    // segunda orientacao
    int result2 = INF;
    if (n % l == 0){
        result2 = check_orientation(n, m, l, freq);
        if(result2 == 0){
            result2 = INF;
        }
    }

    int min_tabuas = min(result1, result2);
    return min_tabuas;
}


int main(){ _

    while(1){
        // Dimensoes salao MxN
        int m, n;
        cin >> m >> n;

        // passar para cm
        m *= 100;
        n *= 100;

        if(m == 0 and n == 0){
            break;
        }

        // Largura em cm
        int l;
        cin >> l;

        // Tabuas
        int k;
        cin >> k;

        int temp;
        unordered_map<int, int> freq_comprimentos;
        for(int i = 0; i < k; i++){
            cin >> temp;
            temp *= 100;
            if(temp > m and temp > n) continue; // nao precisa armazenar tabuas maiores que o salao 
            freq_comprimentos[temp]++; // passar para cm
        }

        int num_tabuas = check_fit(m, n, l, freq_comprimentos);

        if(num_tabuas < INF){
            cout << num_tabuas << endl;
        }
        else{
            cout << "impossivel" << endl;
        }

    }
    
    return 0;
}