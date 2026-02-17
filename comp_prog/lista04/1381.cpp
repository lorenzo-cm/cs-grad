#include <bits/stdc++.h>
using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

int MOD = 1300031;
int MAX = MOD;

ll mod_pow(ll a, ll b, ll m){
    ll res = 1;
    while(b){
        // impar
        if(b & 1){
            res = (res * a) % m;
        }

        a = (a * a) % m;
        b >>= 1;
    }
    return res;
}

void precompute(vector<ll>& fat, vector<ll>& inv_fat){
    fat[0] = 1;
    for(int i = 1; i < MAX; i++){
        fat[i] = (fat[i - 1] * i) % MOD;
    }

    inv_fat[MAX - 1] = mod_pow(fat[MAX - 1], MOD - 2, MOD);

    for(int i = MAX - 2; i >= 0; i--){
        inv_fat[i] = (inv_fat[i + 1] * (i + 1)) % MOD;
    }
}

ll binom(vector<ll>& fat, vector<ll>& inv_fat, int a, int b){
    if(b < 0 || b > a){
        return 0;
    }
    return (((fat[a] * inv_fat[b]) % MOD) * inv_fat[a - b]) % MOD;
}

ll lucas(long long n, long long k, vector<ll>& fat, vector<ll>& inv_fat){

    if(k < 0 || k > n){
        return 0;
    }

    if(k == 0){
        return 1;
    }

    int ni = n % MOD;
    int ki = k % MOD;

    return ( lucas(n / MOD, k / MOD, fat, inv_fat) *
             binom(fat, inv_fat, ni, ki) ) % MOD;
}

int main(){ _
    // num de solucoes é combinacao (C+N-1, N-1)
    // a ideia é aquela do ensino medio de trabalhar com divisorias
    // ex) dividir 4 X para 3 crianças
    //     preciso de 2 divisórias, pois 2 divisórias delimitam 3 grupos
    //     X X X X | |
    //     Possivel agregação: X X | X | X

    // (a⋅b) mod m = ( (a mod m) * (b mod m)) mod m
    // fazer fatorial com mod m

    // calcular fatorial com mod

    // calcular inverso modular para a divisão
    // pequeno teorema de fermat -> a^p-1 = 1  mod p
    // logo a^p-2 = a mod p
    // aplicando inverso modular a * a^-1 = 1 mod p
    // entao a^p-2 = a^-1 mod p 

    // assim  3^(1300031-2) = 3^-1 mod 1300031
    // 3^(1300031-2) deve ser calculado via exponenciacao rapida

    vector<ll> fat(MAX), inv_fat(MAX);

    precompute(fat, inv_fat);

    int T;
    cin >> T;
    for(int i=0; i<T; i++){
        long long N, C;
        cin >> N >> C;
        cout << lucas(C + N - 1, N - 1, fat, inv_fat) << endl;
    }

    return 0;
}
