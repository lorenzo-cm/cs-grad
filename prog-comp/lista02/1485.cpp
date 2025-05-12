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

int calculate_value(int bola, const vecint& roleta, int s, int pos) {
    return -(bola * roleta[pos] + bola * roleta[(pos + 1) % s]);
}

int solve(int s, int b, vecint &bolas, vecint &roleta) {
    vector<vector<vecint>> dp(b, vector<vecint>(s, vecint(s, -INF)));

    for(int i = 0; i < b; ++i) {
        for(int j = 0; j < s; ++j) {
            int left_space = j / 2;
            int right_space = (s - j) / 2;

            for(int p = 0; p < s; ++p) {
                if (i == 0) {
                    dp[i][j][p] = calculate_value(bolas[i], roleta, s, p);
                    continue;
                }

                if(left_space < i || right_space < b - i) {
                    dp[i][j][p] = -INF;
                    continue;
                }

                int current_value = calculate_value(bolas[i], roleta, s, (p + j) % s);
                int best_prev = -INF;

                for(int k = 2 * (i - 1); k <= j - 2; ++k) {
                    best_prev = max(best_prev, dp[i - 1][k][p]);
                }

                if(best_prev > -INF) {
                    dp[i][j][p] = current_value + best_prev;
                }
            }
        }
    }

    int max_result = -INF;
    for (int j = 0; j < s; ++j) {
        for (int p = 0; p < s; ++p) {
            max_result = max(max_result, dp[b - 1][j][p]);
        }
    }

    return max_result;
}

int main(){ _
    int s, b;
    while(cin >> s >> b) {
        if(s == 0) break;

        vecint roleta(s, 0), bolas(b, 0);
        for(int i = 0; i < s; ++i){
            cin >> roleta[i];
        }

        for(int i = 0; i < b; ++i){
            cin >> bolas[i];
        }

        cout << solve(s, b, bolas, roleta) << endl;
    }
    
    return 0;
}