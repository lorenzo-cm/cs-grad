#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

int main(){ _

    int a, b;
    cin >> a >> b;

    // menor num de cortes p transformar retangulo de tamanho i, j em quadrados
    // 0, 0 -> 0
    // i == j -> 0
    // posso dividir de varias formas, mas quero a melhor
    // i,j corte que gera o melhor retangulo
    // se corto i, j em i/2, tenho dois retangulos de tamanho i/2 x j
    // nao necessariamente pq i n precisa ser par
    // entao seria i/2 e i-i/2
    // + 1 pois to fazendo mais um corte

    vector<vecint> dp(a+1, vecint(b+1, INF));

    for(int i = 1; i<=a; i++){
        for(int j = 1; j<=b; j++){
            
            if(i == j){
                dp[i][j] = 0;
                continue;
            }

            int best_corte = INF;

            // eixo 1
            for(int k = 1; k<=i/2; k++){
                best_corte = min(best_corte, 1 + dp[k][j] + dp[i-k][j]);
            }

            // eixo 2
            for(int k = 1; k<=j/2; k++){
                best_corte = min(best_corte, 1 + dp[i][k] + dp[i][j-k]);
            }

            dp[i][j] = best_corte;

        }
    }

    cout << dp[a][b] << endl;

    
    return 0;
}