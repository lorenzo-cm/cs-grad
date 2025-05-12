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

int calc_rect(vector<vecint> &dp, int x1, int y1, int x2, int y2){
    return dp[x2][y2] - dp[x1-1][y2] - dp[x2][y1-1] + dp[x1-1][y1-1];
}

int is_assento_vago(vector<string> &grid, int i, int j){
    return grid[i][j - 1] == '.'; // j-1 pq é uma string 0-based
}

int solve(int R, int C, int K, vector<string> &grid){
    // dp[i][j] = utilizando ate linha i e col j, quantas vagas tenho
    // vai ser one based, entao tem que ter linhas + 1 e cols + 1
    // dp[0][j] = 0
    // dp[i][0] = 0
    // dp[i][j] = dp[i-1][j] + dp[i][j-1] - dp[i-1][j-1] + is_assento_vago(i, j)
    // agora preciso saber quantos assentos vagos tem em um retangulo arbitrario
    // dado 4 pontos x1,y1, x2,y2: qtd_assentos_vagos = dp[x2, y2] - dp[x2-1,y1] - dp[x1, y2-1] + dp[x1-1, y1-1]
    // depois passo na matriz buscando a menor multiplicacao de i*j que tem a dp >= k

    vector<vecint> dp(R+1, vecint(C+1, 0));

    for (int i = 1; i <= R; i++){
        for (int j = 1; j <= C; j++){
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1] - dp[i - 1][j - 1] + is_assento_vago(grid, i, j); 
        }
    }


    // Como calcular os retangulos:
    // iterar sobre x1 e x2 definido as linhas de comeco e final -> altura
    // usar uma variavel para representar qnts assentos livres em cada col entre x1 e x2 -> largura
    // fazer 2 pointer
    
    // maior largura
    int best = R * C + 1;

    for (int top = 1; top <= R; top++)
        for (int bot = top; bot <= R; bot++) {

            // computar coluna
            vector<int> assentos_livres(C + 1);
            for (int col = 1; col <= C; col++){
                assentos_livres[col] = calc_rect(dp, top, col, bot, col);
            }

            int sum = 0, left = 1;
            for (int right = 1; right <= C; right++) {
                sum += assentos_livres[right];

                // condição atendida -> andar com left ate left==right
                while (sum >= K && left <= right) {
                    int area = (bot - top + 1) * (right - left + 1);
                    best = min(best, area);
                    sum -= assentos_livres[left];
                    left++;
                }
            }
        }

    return best; 
}

int main(){ _

    int R, C, K;
    while(cin >> R >> C >> K){
        if(R == 0) break;

        vector<string> grid(R + 1);
        for(int i = 1; i<=R; i++){
            cin >> grid[i];
        }

        cout << solve(R, C, K, grid) << endl;
    }
    
    return 0;
}