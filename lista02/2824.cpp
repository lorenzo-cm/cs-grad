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

int main() { _
    string s1, s2;
    cin >> s1 >> s2;
    
    // dp[i, j] = maior substr que comeca em i na primeira string e j na segunda string
    // se s1[i] == s2[j], entao s[i,j] = 1 + dp[i+1, j+1]
    // caso forem diferentes, pelo menos 1 não participa da resposta
    // dp[i, j] = tentar colocar elemento i ou tentar colocar elemento j
    // dp[i, j] = max(dp[i+1, j], dp[i, j+1])
    //
    // Preciso do cara da frente
    // Ordem decrescente

    vector<vecint> dp(s1.size()+1, vecint(s2.size()+1, 0));

    for (int i = s1.size()-1; i >= 0; i--) {
        for (int j = s2.size()-1; j >= 0; j--) {

            if(s1[i] == s2[j]){
                dp[i][j] = dp[i+1][j + 1] + 1;
            }

            else{
                dp[i][j] = max(dp[i+1][j], dp[i][j + 1]);
            }
                
        }
    }

    cout << dp[0][0] << endl;

    return 0;
}
