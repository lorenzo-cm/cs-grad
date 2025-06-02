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

const int MAXN = 55;


int bfs(int s, int t, vector<vecint>& adj, vector<int>& parent, vector<vecint>& cap) {
    fill(parent.begin(), parent.end(), -1);
    parent[s] = s;
    queue<pair<int, int>> q;
    q.push({s, INF});

    while (!q.empty()) {
        int u = q.front().first;
        int flow = q.front().second;
        q.pop();

        for (int v : adj[u]) {
            if (parent[v] == -1 && cap[u][v] > 0) {
                parent[v] = u;
                int new_flow = min(flow, cap[u][v]);
                if (v == t){
                    return new_flow;
                }
                q.push({v, new_flow});
            }
        }
    }
    return 0;
}

int maxflow(int s, int t, vector<vecint>& adj, vector<vecint>& cap) {
    int flow = 0;
    vector<int> parent(t + 1);

    int new_flow;
    while ((new_flow = bfs(s, t, adj, parent, cap)) != 0) {
        flow += new_flow;
        int cur = t;
        while (cur != s) {
            int prev = parent[cur];
            cap[prev][cur] -= new_flow;
            cap[cur][prev] += new_flow;
            cur = prev;
        }
    }
    return flow;
}

int main(){ _
    int N, M, A;

    while (cin >> N >> M >> A) {
        if (N == 0){
            break;
        }

        vector<vecint> capacity(MAXN, vecint(MAXN, 0));
        vector<vecint> adj(MAXN);
        vector<tuple<int, int, int>> flights;

        for (int i = 0; i < M; i++) {
            int u, v, c;
            cin >> u >> v >> c;
            capacity[u][v] += c; // o contario é 0 por default
            adj[u].push_back(v);
            adj[v].push_back(u);
            flights.push_back({u, v, c});
        }

        int l = 1, r = A, result = A;

        while (l <= r) {
            int mid = (l + r) / 2;

            vector<vecint> temp_cap(MAXN, vecint(MAXN, 0));

            for (auto [u, v, c] : flights) {
                temp_cap[u][v] = c * mid;
            }

            int flow = maxflow(1, N, adj, temp_cap);

            if (flow >= A) {
                result = mid;
                r = mid - 1;
            } 
            
            else {
                l = mid + 1;
            }
        }

        cout << result << "\n";
    }

    return 0;
}
