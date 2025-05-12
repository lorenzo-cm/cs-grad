#include "message.h"

Message::Message(string _content, unsigned _priority){
    content = _content;
    priority = _priority;
}

Message::Message(){
    content = "";
    priority = 0;
}