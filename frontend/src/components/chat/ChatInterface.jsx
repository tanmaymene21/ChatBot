import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import Chat from '../Chat';
import ChatSidebar from './ChatSidebar';

export default function ChatInterface() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const { logout } = useAuth();

  return (
    <div className="h-screen flex">
      <div
        className={`${
          isSidebarOpen ? 'w-64' : 'w-0'
        } bg-gray-900 transition-all duration-300 ease-in-out overflow-hidden`}
      >
        <ChatSidebar onNewChat={() => {}} onLogout={logout} />
      </div>

      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="text-gray-500 hover:text-gray-700"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
            <h1 className="text-xl font-semibold text-gray-900">
              AI Product Assistant
            </h1>
            <div className="w-6" /> 
          </div>
        </header>
        <main className="flex-1 bg-gray-50">
          <Chat />
        </main>
      </div>
    </div>
  );
} 