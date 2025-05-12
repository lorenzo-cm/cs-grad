#include <iostream>

using namespace std;

struct Message{
    string content;
    unsigned priority;

    Message(string _content, unsigned _priority);
    Message();

};