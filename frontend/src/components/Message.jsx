import React from 'react';
import { User, Bot } from 'lucide-react';

const Message = ({ message }) => {
  const { type, content, timestamp } = message;
  const isUser = type === 'user';
  const isError = type === 'error';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div 
        className={`max-w-[80%] rounded-lg p-4 ${
          isUser 
            ? 'bg-[#04AA6D] text-white' 
            : isError 
            ? 'bg-red-100 text-red-700' 
            : 'bg-gray-100'
        }`}
      >
        <div className="flex items-center space-x-2 mb-2">
          {isUser ? <User size={20} /> : <Bot size={20} />}
          <span className="font-medium">
            {isUser ? 'You' : 'Assistant'}
          </span>
          <span className="text-xs opacity-70">
            {new Date(timestamp).toLocaleTimeString()}
          </span>
        </div>
        
        <p className="text-sm whitespace-pre-wrap" dangerouslySetInnerHTML={{__html:content}}></p>
        
      </div>
    </div>
  );
};

export default Message;