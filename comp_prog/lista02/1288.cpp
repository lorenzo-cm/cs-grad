#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back
#define veci vector<int>

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;


int solve(veci p, veci w, int k){

    int dp[p.size()+1][k+1];

    for(int i = 0; i<=p.size(); i++){
        for(int j = 0; j<=k; j++){

            if(j == 0){
                dp[i][j] = 0;
                continue;
            }

            if(i == 0){
                dp[i][j] = 0;
                continue;
            }
            
            if(w[i-1] <= j){

                dp[i][j] = max( 
                            dp[i-1][j-w[i-1]] + p[i-1], // w[i-1] e p[i-1] pq o w e p sao 0 based
                            dp[i-1][j]
                        );
            }
            else{
                dp[i][j] = dp[i-1][j];
            }
        }
    }

    // cout << dp[p.size()][k] << endl;
    return dp[p.size()][k];
}



int main(){ _

    int casos; cin >> casos;
    
    for(int it =0; it<casos; it++){
        int n; cin >> n;

        vector<int> p(n);
        vector<int> w(n);

        int x, y;
        for(int i = 0; i<n; i++){
            cin >> x >> y;
            p[i] = x;
            w[i] = y;
        }

        int k;
        cin >> k;

        int r;
        cin >> r;

        if(solve(p, w, k) >= r)
            cout << "Missao completada com sucesso" << endl;

        else
            cout << "Falha na missao" << endl;

    }
    
    return 0;
}