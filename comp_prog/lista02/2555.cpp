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

double solve(int N, int K, const vector<double>& P, const vector<double>& prob) {
    vector<double> next(K + 1, 0.0), cur(K + 1, 0.0);
    for (int i = N - 1; i >= 0; --i) {
        for (int k = 0; k <= K; ++k) {
            double best = prob[i] * (P[i] + next[k]);
            if (k > 0) best = max(best, P[i] + next[k - 1]);
            cur[k] = best;
        }
        next.swap(cur);
    }
    return next[K];
}

int main(){ _
    int N, K;
    while (cin >> N >> K) {
        vector<double> P(N), prob(N);
        for (int i = 0; i < N; ++i) cin >> P[i];
        for (int i = 0; i < N; ++i) { int c; cin >> c; prob[i] = c / 100.0; }
        cout << fixed << setprecision(2) << solve(N, K, P, prob) + 1e-9 << endl;
    }
    return 0;
}
