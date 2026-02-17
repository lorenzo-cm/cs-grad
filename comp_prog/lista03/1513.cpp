#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int INF  = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

struct Point{
    int r, c;
};

vecint dx{ -2, -1,  1,  2,  2,  1, -1, -2 };
vecint dy{  1,  2,  2,  1, -1, -2, -2, -1 };

bool valid(int r, int c, int rows, int cols, const vector<string>& grid){
    return r >= 0 && r < rows && c >= 0 && c < cols && grid[r][c] != '#';
}

int knight_dist(const vector<string>& grid, const Point& src, const Point& dst){
    // BFS para menor distância considerando movimentos de cavalo
    int rows = grid.size();
    int cols = grid[0].size();
    auto id = [cols](int r, int c){ return r * cols + c; };

    vecint dist(rows * cols, INF);
    queue<Point> q;

    dist[id(src.r, src.c)] = 0;
    q.push(src);

    while(!q.empty()){
        Point cur = q.front();
        q.pop();

        if(cur.r == dst.r && cur.c == dst.c) return dist[id(cur.r, cur.c)];

        for(int k = 0; k < 8; k++){
            int nr = cur.r + dx[k];
            int nc = cur.c + dy[k];
            if(valid(nr, nc, rows, cols, grid) && dist[id(nr, nc)] == INF){
                dist[id(nr, nc)] = dist[id(cur.r, cur.c)] + 1;
                q.push({ nr, nc });
            }
        }
    }
    return INF;
}

int main(){ _

    // dp[mask][u] = custo minimo para visitar os pontos no mask, terminando no ponto u
    // ir para peões não capturados
    // por fim, ir para o cavalo
    
    // para x peões, a dp tem x+1 colunas
    // e 2^x linhas

    // inicia td com INF
    // dp[0][0] = 0, não capturou nenhum peão, está no cavalo
    // 

    int n, m, k;
    while(cin >> n >> m >> k, n || m || k){
        vector<string> board(n);
        for(string& row : board) cin >> row;

        vector<Point> pts;
        for(int i = 0; i < n; i++){
            for(int j = 0; j < m; j++){
                if(board[i][j] == 'C'){
                    pts.pb({ i, j });
                }
            }
        }
        for(int i = 0; i < n; i++){
            for(int j = 0; j < m; j++){
                if(board[i][j] == 'P'){
                    pts.pb({ i, j });
                }
            }
        }

        int tot = k + 1;
        vector<vector<int>> dist(tot, vector<int>(tot, INF));
        for(int i = 0; i < tot; i++){
            for(int j = 0; j < tot; j++){
                dist[i][j] = knight_dist(board, pts[i], pts[j]);
            }
        }

        int lim = 1 << k;
        vector<vector<int>> dp(lim, vector<int>(tot, INF));
        dp[0][0] = 0;

        for(int mask = 0; mask < lim; mask++){
            for(int u = 0; u < tot; u++){
                if(dp[mask][u] == INF) continue;
                for(int v = 1; v <= k; v++){
                    if(mask & (1 << (v - 1))) continue;
                    int nxt = mask | (1 << (v - 1));
                    dp[nxt][v] = min(dp[nxt][v], dp[mask][u] + dist[u][v]);
                }
            }
        }

        int full = lim - 1;
        int best = INF;
        for(int u = 1; u <= k; u++){
            best = min(best, dp[full][u] + dist[u][0]);
        }

        cout << best << endl;
    }
    return 0;
}
