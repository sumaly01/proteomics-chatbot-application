import React from 'react';
import { Database } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white p-4 rounded-t-lg shadow-sm">
      <div className="flex items-center space-x-2">
        <Database className="h-6 w-6 text-green-500" />
        <h1 className="text-2xl font-bold text-gray-800">
          Proteomics Expert
        </h1>
      </div>
      <p className="text-sm text-gray-600 mt-1">
        Ask questions about proteins
      </p>
    </header>
  );
};

export default Header;