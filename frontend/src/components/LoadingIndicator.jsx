import React from 'react';

const LoadingIndicator = () => {
  return (
    <div className="flex justify-center p-4">
      <div className="space-x-2 flex items-center">
        <div className="w-2 h-2 bg-[#04AA6D] rounded-full animate-bounce" />
        <div className="w-2 h-2 bg-[#04AA6D] rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
        <div className="w-2 h-2 bg-[#04AA6D] rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
      </div>
    </div>
  );
};

export default LoadingIndicator;