import React, { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';

import Message from '../models/message';

import { createMessage, getMessages, sendMessageAPI, sendMessageAPINoUsername } from '../utils/messageHandler';

let idFake = 0;

function formatTime() {
  var now = new Date();
  var hours = now.getHours();
  var minutes = now.getMinutes();

  var formattedHours = hours < 10 ? "0" + hours : hours;
  var formattedMinutes = minutes < 10 ? "0" + minutes : minutes;

  return formattedHours + ':' + formattedMinutes;
}

function formatMessagesTimes(messages: Message[]): Message[] {
  return messages.map(message => {
    const date = new Date(message.sent_at);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const formattedTime = `${hours}:${minutes}`;
    return {
      ...message,
      sent_at: formattedTime
    };
  });
}

function resetMessagesId(messages: Message[]): Message[] {
  const ret = messages.map(message => {

    idFake = idFake + 1;

    return {
      ...message,
      id: idFake
    };
  });

  idFake = idFake + 1;

  return ret;
}


const ChatArea: React.FC = () => {

  let { username = 'test' } = useParams<{ username?: string }>();

  // const [idFake, setIdFake] = useState(1);

  const firstBotMessage: Message = {
    id: 0,
    text: "Olá, como posso te ajudar?",
    is_bot: true,
    sent_at: String(formatTime())
  }

  const [messages, setMessages] = useState<Message[]>([
    firstBotMessage,
  ]);
  
  const [newText, setnewText] = useState('');

  const [errorMessageStatus, seterrorMessageStatus] = useState('');

  const [loading, setLoading] = useState(true);

  useEffect(() => {

    if(username != 'test'){
      getMessages(username)
      .then(data => {

        if(data.length === 0){
          setMessages([firstBotMessage])
        }

        else{
          setMessages(resetMessagesId(formatMessagesTimes(data)));
        }
        setLoading(false);
      })
      .catch(err => {
        seterrorMessageStatus(err);
        setLoading(false);
      });
    }

    else {

      setMessages([firstBotMessage]);
      setLoading(false);

    }
    
  }, [username]);


  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newText.trim()) return;
    
    let newMessage: Message = {
      id: idFake,
      text: newText,
      is_bot: false,
      sent_at: String(formatTime()),
      status: 'pending'
    }

    idFake = idFake + 1;

    setMessages([...messages, newMessage]);

    setnewText('');

    if(username != 'test'){

      const response_bool = await createMessage(newText, false, username)

      if(response_bool){
        newMessage.status = 'sent'
        setMessages([...messages, newMessage]);
      }

      else{
        seterrorMessageStatus('Failed to send the message, try again')
        newMessage.status = 'failed'
      }

      const responseApi  = await sendMessageAPI(newMessage.text, username)

      const newBotMessage : Message = {
        id: idFake,
        text: responseApi['response'],
        is_bot: true,
        sent_at: String(formatTime()),
        status: 'sent'
      }

      idFake = idFake + 1;

      setMessages([...messages, newMessage, newBotMessage]);

      const response_bool_bot = await createMessage(responseApi['response'], true, username)
      
      if(!response_bool_bot){
        seterrorMessageStatus('Failed to retrieve bot message, send your message again')
      }

    }

    else{
      newMessage.status = 'sent'
      setMessages([...messages, newMessage]);

      const responseApi  = await sendMessageAPINoUsername(newMessage.text)

      // have to check the error bot msg to make it
      // if(!response_bool_bot){
      //   seterrorMessageStatus('Failed to retrieve bot message, send your message again')
      // }
      // exit funct

      const newBotMessage : Message = {
        id: idFake,
        text: responseApi['response'],
        is_bot: true,
        sent_at: String(formatTime()),
        status: 'sent'
      }

      idFake = idFake + 1;

      setMessages([...messages, newMessage, newBotMessage]);
    }


  };

  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex flex-col items-center justify-center h-screen overflow-hidden">

      {/* Outermost container with flex layout centered */}
      <div className="w-full max-w-4xl h-full max-h-[80vh] my-4 p-4 border rounded-lg shadow-lg bg-white flex flex-col">


      {loading ? (
        <div className='flex-grow overflow-auto custom-scrollbar pr-4 font-bold text-xl'> . . . </div>
      ) : (
        <>
          {/* Container for messages with a custom scrollbar */}
          <div className="flex-grow overflow-auto custom-scrollbar pr-4">
    
            {/* Container for the individual messages */}
            <div className="space-y-2 mb-4">
              {messages.map((message) => (

                <div key={message.id} className={`flex ${message.is_bot ? 'justify-start' : 'justify-end'}`}>

                  {/* Message bubble with dynamic background based on message status */}
                  <div className={`max-w-[75%] px-4 py-2 rounded-lg break-words ${
                    message.is_bot ? 'bg-blue-950 text-white' :
                    message.status === 'pending' ? 'bg-green-300 text-white' :
                    message.status === 'sent' ? 'bg-green-500 text-white' :
                    message.status === 'failed' ? 'bg-red-500 text-white' :
                    'bg-green-500 text-white' // Default to green if no status is recognized
                    }`}>

                    {/* content that is going to be showed */}
                    <p>{message.text}</p>
                    <p className="text-xs opacity-75 mt-2 text-white">{message.sent_at}</p>

                  </div>

                </div>
              ))}
            </div>
    
            {/* Invisible div for automatic scrolling reference */}
            <div ref={messagesEndRef} />
          </div>
        </>
      )}

        
        
  
        {/* Form for sending a message */}
        <form onSubmit={handleSendMessage} className="flex mt-4">
          <input
            type="text"
            className="flex-1 p-2 border rounded-l-lg focus:outline-none focus:ring-0.5 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Type your message here..."
            value={newText}
            onChange={(e) => setnewText(e.target.value)}
          />
          <button type="submit" className="bg-blue-500 text-white p-2 rounded-r-lg hover:bg-blue-600">Send</button>
        </form>
      </div>
  
      {/* Error message display, if there is an error */}
      {errorMessageStatus && (
        <span className='p-2 bg-red-300 rounded min-w-40 flex justify-center content-center text-center'>
          {errorMessageStatus}
        </span>
      )}
    </div>
  );
  
};

export default ChatArea;
