#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;


vector<vector<string>> brailles = {
    {".*", "**", ".."}, // 0
    {"*.", "..", ".."}, // 1
    {"*.", "*.", ".."}, // 2
    {"**", "..", ".."}, // 3
    {"**", ".*", ".."}, // 4
    {"*.", ".*", ".."}, // 5
    {"**", "*.", ".."}, // 6
    {"**", "**", ".."}, // 7
    {"*.", "**", ".."}, // 8
    {".*", "*.", ".."}, // 9
};

void print_nums_to_braille(vector<int> nums){
    for(int i = 0; i<3; i++){
        for(int j = 0; j < nums.size(); j++){
            cout << brailles[nums[j]][i];
            if(j != nums.size() - 1) cout << ' ';
        }
        cout << endl;
    }
}

vector<vector<string>> read_braille_seq(int quantity_num){

    vector<vector<string>> brailles_read(quantity_num);

    for(int i=0; i<3; i++){

        for(int j=0; j<quantity_num; j++){
            string temp;
            cin >> temp;
            brailles_read[j].push_back(temp);
        }
    }

    return brailles_read;
}

void print_braille_to_num(vector<vector<string>> b){
    vector<int> numbers;
    for(int i = 0; i<b.size(); i++){
        for(int j = 0; j<10; j++){
            if(b[i] == brailles[j]){
                numbers.push_back(j);
                break;
            }
        }
    }
    for(int i : numbers){
        cout << i;
    }
    cout << endl;
}

int main(){ _

    int d;

    while(1){
        cin >> d;
        
        if(d == 0) break;

        string s;
        cin >> s; // S or B

        if(s == "S"){
            string texto;
            cin >> texto;

            vector<int> numeros;
            for (char c : texto) {
                numeros.push_back(c - '0');
            }

            print_nums_to_braille(numeros);
        }

        if(s == "B") {
            vector<vector<string>> braille_read = read_braille_seq(d);
            print_braille_to_num(braille_read);
        }

    }
    
    return 0;
}