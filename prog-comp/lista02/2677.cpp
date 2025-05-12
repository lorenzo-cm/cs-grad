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


int solve(int N, vecint nums, vecint par){

    // dp[i, j] = maior score do jogador 1 considerando o nums[i:j]
    // Supondo o segmento i:j a escolha do adversário após a minha pode ser (i+1,j) ou (i, j-1)
    // Pego o valor da ponta - o melhor que ele pode pegar com a nova particao
    // dp[i, i] = se nums[i] é par, 1, caso contrário 0
    // dependo dos valores futuros de i
    // dependo dos valores anteriores de j
    // Fazer por diagonal
    // A resposta estará em (0, 2N-1)
    // (0, 2N-1) depende de (1, 2N-1)  e (0, 2N-2) 

    vector<vecint> dp(2*N, vecint(2*N, 0));

    for(int i = 0; i<2*N; i++){
        for(int j = 0; j + i < 2*N; j++){
            int l = j;
            int r = j + i;

            if(l==r){
                dp[l][r] = par[l];
            }

            else{
                int left_end = par[l] - dp[l+1][r];
                int right_end = par[r] - dp[l][r-1];
                dp[l][r] = max(left_end, right_end);
            }
        }
    }

    int max_diff = dp[0][2*N - 1];

    // Diff = Pares_j1 - Pares_j2
    // Como tem N pares, se o j1 pega X o j2 pega 2*N - X
    // Diff = J1 - (N - J1)
    return (max_diff + N)/2;
}


int main(){ _

    int N;
    while(cin >> N){
        if(N == 0) break;
        vecint nums(2 * N);
        vecint par(2*N);

        for(int i = 0; i < 2*N; i++){
            cin >> nums[i];
            par[i] = nums[i] % 2 == 0;
        }

        cout << solve(N, nums, par) << endl;

    }
    
    return 0;
}