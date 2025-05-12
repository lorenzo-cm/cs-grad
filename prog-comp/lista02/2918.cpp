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
const ll MOD = 1e9 + 7;

string num;
vector<vector<vector<ll>>> dp;

ll dp_solve(int pos, bool tight, int sum) {
    // pos, tight, sum
    if(pos == num.size()) return sum;

    if(dp[pos][tight][sum] != -1) return dp[pos][tight][sum];

    int max_digit = tight ? num[pos] - '0' : 9;
    ll ans = 0;

    for (int d = 0; d <= max_digit; d++) {
        bool next_tight = tight && (d == max_digit);
        ans = (ans + dp_solve(pos + 1, next_tight, sum + d)) % MOD;
    }

    return dp[pos][tight][sum] = ans;
}

ll solve(ll n) {
    if (n == 0) return 0;
    num = to_string(n);

    int len = num.size();
    int sum_max = 9 * len + 1;
    dp = vector<vector<vector<ll>>>(len, vector<vector<ll>>(2, vector<ll>(sum_max, -1)));

    return dp_solve(0, 1, 0);
}

int main() { _
    ll L, R;
    while (cin >> L >> R) {
        ll result = (solve(R) - solve(L - 1) + MOD) % MOD;
        cout << result << endl;
    }
    return 0;
}
