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

int check_row(int target, unordered_map<int, int>& freq){
    // Tentar com mapa de frequencia para reduzir tamanho do vetor e ser mais rapido

    // uma tabua
    if (freq[target] > 0) {
        freq[target]--;
        return 1;
    }

    // tentar com duas tabuas
    for(auto pair : freq){
        int a = pair.f;
        int b = target - a;

        if (freq[a] > 0) {
            // se for mesmo elemento e tiver freq necessaria
            if (a == b && freq[a] >= 2) {
                freq[a] -= 2;
                return 2;

            // se n for mesmo elemento e tem freq necessaria
            } else if (a != b && freq[b] > 0) {
                freq[a]--;
                freq[b]--;
                return 2;
            }
        }
    }

    return 0;
}

int check_orientation(int tam1, int tam2, int l, unordered_map<int, int> freq){
    
    if(tam1 % l != 0){
        return 0;
    }

    int rows = tam1 / l;
    int row_size = tam2;

    int total_usado = 0;
    for(int i = 0; i < rows; i++){
        int tabuas_usadas = check_row(row_size, freq);

        // impossivel cobrir a linha
        if(!tabuas_usadas) return 0;

        total_usado += tabuas_usadas;
    }

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
            freq_comprimentos[temp*100]++; // passar para cm
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