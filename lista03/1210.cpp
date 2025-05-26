#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int LINF = 0x3f3f3f3f;
const ll LLINF = 0x3f3f3f3f3f3f3f3fll;

int main(){ _
    int N, I, M, P;
    while (cin >> N >> I >> M >> P) {
        vector<ll> C(M);
        for (int i = 0; i < M; i++){
            cin >> C[i];
        } 

        vector<ll> V(M + 1, 0);
        for (int i = 1; i <= M; i++){
            cin >> V[i];
        }

        vector<vector<ll>> dp(N + 2, vector<ll>(M + 1, LINF));
        vector<vector<int>> came_from(N + 2, vector<int>(M + 1, 0));


        // dp[ano][idade] = custo min iniciano de ano e destilador tem idade
        // escolher menor custo entre manter e trocar
        // manter -> C(idade) + dp[ano + 1][idade + 1], idade < M
        // trocar -> p - V(idade) + C(0) + dp[ano + 1][1], idade != 0
        //
        // trackear escolhas -> came_from

        for (int idade = 0; idade <= M; idade++){
            dp[N + 1][idade] = 0;
        }
        
        for (int ano = N; ano >= 1; ano--) {
            for (int idade = 0; idade <= M; idade++) {

                ll manter = LINF;
                if (idade < M)
                    manter = C[idade] + dp[ano + 1][idade + 1];

                ll trocar = LINF;
                if (idade != 0){
                    trocar = P - V[idade] + C[0] + dp[ano + 1][1];
                }

                if (trocar < manter || (trocar == manter && idade != 0)) {
                    dp[ano][idade] = trocar;
                    came_from[ano][idade] = 1;
                } else {
                    dp[ano][idade] = manter;
                    came_from[ano][idade] = 0;
                }
            }
        }

        // reconstruir
        vecint trocas;
        int ano = 1, idade = I;
        while (ano <= N) {
            if (came_from[ano][idade]) {
                trocas.pb(ano);
                idade = 1;
            } 
            
            else {
                idade++;
            }

            ano++;
        }

        cout << dp[1][I] << endl;

        if (trocas.empty()) {
            cout << 0 << endl;
        } 
        
        else {
            for (int i = 0; i < trocas.size(); i++) {
                if (i) cout << ' ';
                cout << trocas[i];
            }
            cout << endl;
        }
    }
    return 0;
}
