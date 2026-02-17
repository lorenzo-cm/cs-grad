#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
// #define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

int main(){ _

    // dp?
    // dp[i][j] = na arvore de decisoes i, a prob do competidor j ganhar
    // se ta sozinho -> 1
    // caso contrario é a prob de ganhar com o adv
    //
    // tenho duas opcoes nesse caso, perder ou ganhar
    // como percorrer -> os que correm sozinho, dps 1x1, depois posso computar a partir disso
    // 
    // resposta estara em dp[final][1] -> 1 based

    int n;
    while(cin >> n){
        if(n == 0) break;

        vector<vector<double>> m(n+1, vector<double>(n+1));
        for(int i = 1; i <= n; i++) {
            for(int j = 1; j <= n; j++){
                cin >> m[i][j];
            }
        }

        int id_max = 2 * n - 1;
        vector<int> left_child(id_max+1), right_child(id_max+1);
        vector<bool> is_child(id_max+1, false);

        // arvore binaria
        for(int race_id = n + 1; race_id <= id_max; race_id++){
            int a, b;
            cin >> a >> b;
            left_child[race_id] = a;
            right_child[race_id] = b;
            is_child[a] = true;
            is_child[b] = true;
        }

        // final torneio
        int final = -1;
        for(int race_id = n + 1; race_id <= id_max; race_id++){
            if(!is_child[race_id]){
                final = race_id;
                break;
            }
        }

        vector<vector<double>> dp(id_max+1, vector<double>(n+1, 0.0));
        vector<bool> visited_dp(id_max+1, false);

        function<void(int)> compute_dp = [&](int u) {
            if(visited_dp[u]) return;
            visited_dp[u] = true;
        
            // sozinho
            if(u <= n){
                dp[u][u] = 1.0;
                return;
            }

            int l = left_child[u];
            int r = right_child[u];

            // perder e ganhar
            compute_dp(l);
            compute_dp(r);

            vector<double> s_right(n+1, 0.0), s_left(n+1, 0.0);

            for(int j = 1; j <= n; j++){
                double pr = dp[r][j];
                if(pr > 0.0) {
                    for(int i = 1; i <= n; i++) {
                        s_right[i] += pr * m[i][j];
                    }
                }
            }

            for(int j = 1; j <= n; j++){
                double pl = dp[l][j];
                if(pl > 0.0) {
                    for(int i = 1; i <= n; i++){
                        s_left[i] += pl * m[i][j];
                    }
                }
            }
            
            for(int i = 1; i <= n; i++){
                double from_left = dp[l][i] * s_right[i];
                double from_right = dp[r][i] * s_left[i];
                dp[u][i] = from_left + from_right;
            }
        };
        
        compute_dp(final);

        cout << fixed << setprecision(6) << dp[final][1] << endl;
    }
    return 0;
}
