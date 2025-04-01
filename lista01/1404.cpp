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

// void print_board(vector<vector<int>> tabuleiro){
//     for(int i = 0; i < tabuleiro.size(); i++){
//         for(int j = 0; j < tabuleiro[0].size(); j++){
//             cout << tabuleiro[i][j] << " ";
//         }
//         cout<<endl;
//     }
//     cout << endl;
// }

int dfs(vector<vector<int>>& tabuleiro, int n, int m, int start_x, int start_y){
    int max_depth = 0;

    int dx[4] = {-1, -1, +1, +1};
    int dy[4] = {-1, +1, -1, +1};

    int dx2[4] = {-2, -2, +2, +2};
    int dy2[4] = {-2, +2, -2, +2};

    for(int i=0; i<4; i++){
        int enemy_x = start_x + dx[i];
        int enemy_y = start_y + dy[i];

        int frente_x = start_x + dx2[i];
        int frente_y = start_y + dy2[i];

        if(enemy_x>=0 and enemy_y>=0 and frente_x>=0 and frente_y>=0 and enemy_x<n and enemy_y<m and frente_x<n and frente_y<m){
            if(tabuleiro[enemy_x][enemy_y]==2 and tabuleiro[frente_x][frente_y]==0){
                // cout << "Captura de (" << start_pos.f << ", " << start_pos.s << ") para (" << frente_x << ", " << frente_y << ")" << endl;
                // cout << "start = " << tabuleiro[start_pos.f][start_pos.s] << " | mid = " << tabuleiro[enemy_x][enemy_y] << " | frente = " << tabuleiro[frente_x][frente_y] << endl;

                // print_board(tabuleiro);
                
                tabuleiro[start_x][start_y] = 0;
                tabuleiro[enemy_x][enemy_y] = 0;
                tabuleiro[frente_x][frente_y] = 1;

                // print_board(tabuleiro);


                int depth = 1 + dfs(tabuleiro, n, m, frente_x, frente_y);

                tabuleiro[start_x][start_y] = 1;
                tabuleiro[enemy_x][enemy_y] = 2;
                tabuleiro[frente_x][frente_y] = 0;

                max_depth = max(max_depth, depth);
            }
        }
    }

    return max_depth;
}

int multiple_dfs(vector<vector<int>>& tabuleiro, int n, int m, int casas_um_x[20000], int casas_um_y[20000], int k){
    int max_val = 0;
    for(int i = 0; i<k; i++){
        max_val = max(max_val, dfs(tabuleiro, n, m, casas_um_x[i], casas_um_y[i]));
    }   
    return max_val;
}


int main(){ _
    int n, m; 
    while(cin >> n >> m){
        if(n == 0) break;

        vector<vector<int>> tabuleiro(n, vector<int>(m, 0));
        int casas_um_x[20000];
        int casas_um_y[20000];

        int temp;
        int k = 0;
        for(int i = 0; i < n; i++){
            for(int j = 0; j < m; j++){
                if( (i + j) % 2 == 0 ) {
                    cin >> temp;
                    tabuleiro[i][j] = temp;
                    if(temp == 1){
                        casas_um_x[k] = i;
                        casas_um_y[k] = j;
                        k++;
                    }
                }
            }
        }

        // print_board(tabuleiro);
        
        cout << multiple_dfs(tabuleiro, n, m, casas_um_x, casas_um_y, k) << endl;
    }
    
    return 0;
}