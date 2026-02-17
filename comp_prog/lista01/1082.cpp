#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

vector<int> dfs(int start, vector<vector<int>>& adj_list, vector<int>& visited){
    stack<int> nexts;

    visited[start] = 1; 
    nexts.push(start);

    vector<int> component;

    while(!nexts.empty()){

        int node = nexts.top();
        nexts.pop();

        component.pb(node);

        for (int neighbor : adj_list[node]) {
            if (!visited[neighbor]) {
                nexts.push(neighbor);
                visited[neighbor] = 1;
            }
        }
    }

    sort(component.begin(), component.end());
    return component;
}


int dfs_connected_comp(vector<vector<int>> adj_list, vector<vector<int>>& components) {
    vector<int> visited(adj_list.size(), 0);
    int num_components = 0;

    for (int i = 0; i < adj_list.size(); i++) {
        if (!visited[i]) {
            vector<int> new_component = dfs(i, adj_list, visited);
            components.pb(new_component);
            num_components++;
        }
    }
    return num_components;
}

int main(){ _
    int n;
    cin >> n;

    int v,e;
    for(int i = 0; i < n; i++){
        cin >> v >> e;
        
        vector<vector<int>> adj_list(v);
        vector<vector<int>> components;
        
        for(int j = 0; j < e; j++){
            char v1, v2;
            cin >> v1 >> v2;

            int int_v1 = v1 - 'a';
            int int_v2 = v2 - 'a';

            adj_list[int_v1].pb(int_v2);
            adj_list[int_v2].pb(int_v1);
        }

        int num_components = dfs_connected_comp(adj_list, components);

        cout << "Case #" << i+1 << ":" << endl;
        
        for(int j = 0; j < num_components; j++){
            
            for(int l=0; l < components[j].size(); l++){
                cout << char(components[j][l] + 'a') << ',';
            }

            cout << endl;
        }

        cout << num_components << " connected components" << endl;

        cout << endl;

        adj_list.clear();
    }
    
    return 0;
}