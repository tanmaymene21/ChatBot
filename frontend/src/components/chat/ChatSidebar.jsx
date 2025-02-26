import { useEffect, useState, useCallback } from 'react';
import { useChat } from '../../context/ChatContext';
import { useNavigate } from 'react-router-dom';
import api from '../../utils/axios';

export default function ChatSidebar({ onNewChat, onLogout }) {
  const navigate = useNavigate();
  const { dispatch, state } = useChat();
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadChatHistory = useCallback(async () => {
    try {
      const response = await api.get('/chatbot/history');
      setChatHistory(response.data);
    } catch (error) {
      console.error('Failed to load chat history:', error);
      if (error.response?.status !== 401) {
        setError('Failed to load chat history');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadChatHistory();
  }, [loadChatHistory]);

  function handleNewChat() {
    dispatch({ type: 'CLEAR_MESSAGES' });
    navigate('/chat');
    onNewChat();
  }

  function handleChatSelect(chatId) {
    navigate(`/chat/${chatId}`);
  }

  function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
  }

  return (
    <div className="h-full flex flex-col text-gray-300">
      <div className="p-4">
        <button
          onClick={handleNewChat}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg border border-gray-700 hover:bg-gray-700 transition-colors"
        >
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="flex justify-center p-4">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-300" />
          </div>
        ) : (
          <div className="space-y-1 p-2">
            {chatHistory.map((chat) => (
              <button
                key={chat.chat_id}
                className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-700 transition-colors text-sm"
                onClick={() => handleChatSelect(chat.chat_id)}
              >
                <div className="truncate">
                  {chat.title || chat.user_message}
                </div>
                <div className="text-xs text-gray-500">
                  {formatDate(chat.timestamp)}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="p-4 border-t border-gray-700">
        <button
          onClick={onLogout}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-700 transition-colors text-red-400 hover:text-red-300"
        >
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
          Sign Out
        </button>
      </div>
    </div>
  );
}
