import React from 'react';
import Message from './Message';
import LoadingIndicator from './LoadingIndicator';

const MessageList = ({ messages, loading, messagesEndRef }) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-white rounded-lg my-4">
      {messages.length === 0 && (
        <div className="text-center text-gray-500">
          Start by asking a question about proteins!
        </div>
      )}
      {messages.map((message, index) => (
        <Message key={index} message={message} />
      ))}
      {loading && <LoadingIndicator />}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;