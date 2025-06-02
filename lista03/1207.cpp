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

const int MAXV = 1200;

int bfs(vecint& parent, vector<vecint>& flow, vector<vecint>& capacity, vector<vecint>& adj, int s, int t) {
    fill(parent.begin(), parent.end(), -1);
    parent[s] = s;
    queue<pair<int, int>> q;
    q.push({s, INF});

    while(!q.empty()){
        int cur = q.front().first;
        int f = q.front().second;
        q.pop();

        for(int next : adj[cur]) {
            if(parent[next] == -1 && capacity[cur][next] - flow[cur][next] > 0){
                parent[next] = cur;
                int new_flow = min(f, capacity[cur][next] - flow[cur][next]);
                if(next == t){
                    return new_flow;
                }
                q.push({next, new_flow});
            }
        }
    }

    return 0;
}

int maxflow(vecint& parent, vector<vecint>& flow, vector<vecint>& capacity, vector<vecint>& adj, int s, int t) {
    int f = 0, new_flow;
    while((new_flow = bfs(parent, flow, capacity, adj, s, t))){
        f += new_flow;
        int cur = t;
        while(cur != s) {
            int prev = parent[cur];
            flow[prev][cur] += new_flow;
            flow[cur][prev] -= new_flow;
            cur = prev;
        }
    }
    return f;
}

int main(){ _

    int N, M;
    while(cin >> N >> M) {
        vector<vecint> adj(MAXV);
        vector<vecint> capacity(MAXV, vecint(MAXV, 0));
        vector<vecint> flow(MAXV, vecint(MAXV, 0));
        vecint parent(MAXV, -1);

        vector<int> cost(N);
        for(int i = 0; i<N; i++){
            cin >> cost[i];
        }

        vector<int> P(M);
        for(int i = 0; i<M; i++){
            cin >> P[i];
        }

        const int source = 0;
        const int sink = 1;
        const int vodka_offset = 2;
        const int category_offset = vodka_offset + N;

        int total_benefit = 0;

        for(int i = 0; i < M; i++){
            int B, x;
            cin >> B;
            total_benefit += B;

            int category_node = category_offset + i;

            capacity[source][category_node] = B;
            adj[source].push_back(category_node);
            adj[category_node].push_back(source);

            for(int j = 0; j < P[i]; j++){
                cin >> x;
                x--;
                int vodka_node = vodka_offset + x;

                capacity[category_node][vodka_node] = INF;
                adj[category_node].push_back(vodka_node);
                adj[vodka_node].push_back(category_node);
            }
        }

        for(int i = 0; i < N; i++){
            int vodka_node = vodka_offset + i;
            capacity[vodka_node][sink] = cost[i];
            adj[vodka_node].push_back(sink);
            adj[sink].push_back(vodka_node);
        }

        int total_flow = maxflow(parent, flow, capacity, adj, source, sink);
        cout << total_benefit - total_flow << '\n';
    }

    return 0;
}
