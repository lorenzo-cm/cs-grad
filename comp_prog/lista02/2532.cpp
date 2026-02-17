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


int solve(vecint dano, vecint mana, int p, int n){

    // dp[i] menor qntd de mana para qualquer dano >= i
    vecint dp(p+1, INF);
    dp[0] = 0;

    for (int i = 0; i < n; i++) {
        for (int j = p; j >= 0; j--) 
            if (dp[j] != INF) {
                int dano_aplicado = min(p, j + dano[i]); // dano maior do que p vai ser capado para p
                dp[dano_aplicado] = min(dp[dano_aplicado], dp[j] + mana[i]); // Escolher entre o valor de mana que ja tinha p dar o dano e o valor de dano atual + a mana do feitico de agora
            }
    }

    return dp[p] == INF ? -1 : dp[p];

}


int main(){

    int n, p; 
    while(cin >> n >> p){

        vecint dano(n);
        vecint mana(n);
        
        int sum_mana = 0;
        for(int i = 0; i<n; i++){
            cin >> dano[i] >> mana[i];
            sum_mana += mana[i];
        }

        cout << solve(dano, mana, p, n) << endl;

    }

    return 0;
}