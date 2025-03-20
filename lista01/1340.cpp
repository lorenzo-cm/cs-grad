#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

int main(){ _

    int n;

    while(cin >> n){
        stack<int> p;
        priority_queue<int> pq;
        queue<int> q;
        int type, num;
        int is_p = 1, is_pq = 1, is_q = 1;

        for(int i = 0; i<n; i++){
            cin >> type;

            if(type == 1){
                cin >> num;

                p.push(num);
                pq.push(num);
                q.push(num);
            }

            // type 2
            else {

                cin >> num;

                if (!p.empty() && num != p.top()) {
                    is_p = 0;
                }
                p.pop();
        
                if (!pq.empty() && num != pq.top()) {
                    is_pq = 0;
                }
                pq.pop();
        
                if (!q.empty() && num != q.front()) {
                    is_q = 0;
                }
                q.pop();

            }
        }

        if(is_p + is_pq + is_q > 1) cout << "not sure" << endl;
        else if(is_p + is_pq + is_q == 0) cout << "impossible" << endl;
        else if(is_p) cout << "stack" << endl;
        else if(is_pq) cout << "priority queue" << endl;
        else if(is_q) cout << "queue" << endl;
    }
    
    return 0;
}