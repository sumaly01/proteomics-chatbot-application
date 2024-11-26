import React from 'react';
import ChatInterface from './components/ChatInterface';
import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Toaster position="top-right" />
      <ChatInterface />
    </div>
  );
}

export default App;