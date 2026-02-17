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

struct Edge {
    int to;
    int flow;
    int cap;
    int rev;
};

class Graph {
    int v_count;
    vecint level;
    vector<vector<Edge>> adj;

public:
    Graph(int v_count_param):v_count(v_count_param),level(v_count_param),adj(v_count_param){}

    void add_edge(int u,int v,int cap){
        Edge a{v,0,cap,(int)adj[v].size()};
        Edge b{u,0,0,(int)adj[u].size()};
        adj[u].pb(a);
        adj[v].pb(b);
    }

    bool bfs(int s,int t){
        fill(level.begin(),level.end(),-1);
        level[s] = 0;
        queue<int> q;
        q.push(s);
        while(!q.empty()){
            int u = q.front();
            q.pop();
            for(size_t i=0;i<adj[u].size();i++){
                Edge &e=adj[u][i];
                if(level[e.to]<0 && e.flow<e.cap){
                    level[e.to]=level[u]+1;
                    q.push(e.to);
                }
            }
        }
        return level[t]>=0;
    }

    int send_flow(int u,int flow,int t,vecint &start){
        if(u == t){
            return flow;
        }
        for(; start[u]<(int)adj[u].size(); start[u]++){
            Edge &e=adj[u][start[u]];
            if(level[e.to] == level[u]+1 && e.flow < e.cap){
                int curr_flow = min(flow, e.cap-e.flow);
                int temp_flow = send_flow(e.to, curr_flow, t, start);
                if(temp_flow > 0){
                    e.flow += temp_flow;
                    adj[e.to][e.rev].flow -= temp_flow;
                    return temp_flow;
                }
            }
        }
        return 0;
    }

    int dinic_max_flow(int s,int t){
        if(s == t){
            return -1;
        }
        int total_flow = 0;
        while(bfs(s,t)){
            vecint start(v_count, 0);
            while(int flow = send_flow(s, INF, t, start)){
                total_flow += flow;
            }
        }
        return total_flow;
    }
};

int main(){ _
    int team_count;
    int points_per_game;
    int game_results;
    while(cin>>team_count>>points_per_game>>game_results && (team_count||points_per_game||game_results)){
        vector<vector<pair<int,int>>> games(team_count,vector<pair<int,int>>(team_count));
        for(int i=0; i<game_results; i++){
            int u;
            char result;
            int v;
            cin >> u >> result >> v;
            if(result=='='){
                games[u][v].f++;
                games[v][u].f++;
                games[u][v].s++;
                games[v][u].s++;
            }
            else{
                games[v][u].f+=2;
                games[u][v].s++;
                games[v][u].s++;
            }
        }

        int max_points_team0 = 0;
        for(int i=1; i<team_count; i++){
            max_points_team0 += games[0][i].f + (points_per_game-games[0][i].s) * 2;
        }

        int match_count = (team_count-1) * (team_count-2) /2;
        int source = 0;
        int sink = match_count + team_count;
        Graph graph(sink+1);
        int match_id=1;

        for(int i=1; i<team_count; i++){
            for(int j=i+1; j<team_count; j++){
                int cap = (points_per_game-games[i][j].s) * 2;
                graph.add_edge(source,match_id,cap);
                graph.add_edge(match_id, match_count+i, cap);
                graph.add_edge(match_id, match_count+j, cap);
                match_id++;
            }
        }

        bool possible = true;
        for(int i=1; i<team_count; i++){
            int cap_limit = max_points_team0-1;
            for(int j=0; j<team_count; j++){
                cap_limit -= games[i][j].f;
            }
            if(cap_limit < 0){
                possible = false;
                break;
            }
            graph.add_edge(match_count+i, sink, cap_limit);
        }

        int total_points = points_per_game * 2 * team_count * (team_count-1) / 2;
        int future_points_team0 = 0;
        for(int i = 1; i<team_count; i++){
            future_points_team0 += (points_per_game-games[0][i].s) * 2;
        }

        int flow = graph.dinic_max_flow(source, sink);
        if(flow + 2 * game_results+future_points_team0 != total_points){
            possible = false;
        }

        if(possible){
            cout << "Y" << endl;
        }
        else{
            cout << "N" << endl;
        }
    }

    return 0;
}
