#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int INF = 1e9;
const int MAXN = 205;

int num_horses, num_soldiers, num_affinities;
vector<vecint> capacity(MAXN, vecint(MAXN));
vector<vecint> graph(MAXN);

int bfs(int source, int sink, vecint &parent) {
    fill(parent.begin(), parent.end(), -1);
    parent[source] = -2;
    queue<pair<int, int>> q;
    q.push({source, INF});

    while(!q.empty()) {
        int current = q.front().f;
        int flow = q.front().s;
        q.pop();

        for(int neighbor : graph[current]) {
            if(parent[neighbor] == -1 && capacity[current][neighbor] > 0) {
                parent[neighbor] = current;
                int new_flow = min(flow, capacity[current][neighbor]);

                if(neighbor == sink)
                    return new_flow;

                q.push({neighbor, new_flow});
            }
        }
    }

    return 0;
}

int maxflow(int source, int sink) {
    int total_flow = 0;
    vecint parent(MAXN);

    int new_flow;
    while((new_flow = bfs(source, sink, parent))) {
        total_flow += new_flow;
        int current = sink;

        while(current != source) {
            int previous = parent[current];
            capacity[previous][current] -= new_flow;
            capacity[current][previous] += new_flow;
            current = previous;
        }
    }

    return total_flow;
}

int main(){ _
    int instance = 1;

    while(cin >> num_horses >> num_soldiers >> num_affinities) {
        graph = vector<vecint>(MAXN);
        capacity = vector<vecint>(MAXN, vecint(MAXN, 0));

        int source = 0;
        int sink = num_horses + num_soldiers + 1;

        for(int i = 1; i <= num_horses; i++) {
            int horse_capacity;
            cin >> horse_capacity;
            int horse_node = i;

            capacity[horse_node][sink] = horse_capacity;
            graph[horse_node].pb(sink);
            graph[sink].pb(horse_node);
        }

        for(int i = 1; i <= num_soldiers; i++) {
            int soldier_node = num_horses + i;

            capacity[source][soldier_node] = 1;
            graph[source].pb(soldier_node);
            graph[soldier_node].pb(source);
        }

        for(int i = 0; i < num_affinities; i++) {
            int horse_id, soldier_id;
            cin >> horse_id >> soldier_id;

            int horse_node = horse_id;
            int soldier_node = num_horses + soldier_id;

            capacity[soldier_node][horse_node] = 1;
            graph[soldier_node].pb(horse_node);
            graph[horse_node].pb(soldier_node);
        }

        int result = maxflow(source, sink);

        cout << "Instancia " << instance++ << endl;
        cout << result << endl << endl;
    }

    return 0;
}
