import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-hot-toast';
import MessageList from './MessageList';
import InputArea from './InputArea';
import Header from './Header';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (inputText) => {
    if (!inputText.trim()) return;

    try {
      setLoading(true);
      
      // Add user message
      const userMessage = {
        type: 'user',
        content: inputText,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, userMessage]);

      // Send request to backend
      const response = await axios.post('http://localhost:5000/chatbot', {
        query: inputText
      });

      // Add bot message
      const botMessage = {
        type: 'bot',
        content: response.data.response.content,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      toast.error(error.response?.data?.message || 'Failed to get response from server');
      
      // Add error message
      const errorMessage = {
        type: 'error',
        content: 'Sorry, there was an error processing your request.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } 
      setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto p-4 h-screen flex flex-col">
      <Header />
      <MessageList 
        messages={messages} 
        loading={loading} 
        messagesEndRef={messagesEndRef}
      />
      <InputArea 
        onSendMessage={handleSendMessage} 
        loading={loading} 
      />
    </div>
  );
};

export default ChatInterface;